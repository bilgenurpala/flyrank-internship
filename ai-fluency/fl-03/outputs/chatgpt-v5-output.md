# FastAPI + SQLite Security Code Review

## Step 1 — Intended behavior

The API retrieves a task by ID and creates a task containing a title and completion status in SQLite.

## Step 2 — Security pass

1. **SQL injection in `get_task` — Critical**

   `task_id` is interpolated directly into SQL:

   ```python
   f"SELECT * FROM tasks WHERE id = {task_id}"
   ```

   An attacker can supply SQL expressions or a `UNION` query to read unintended database data.

2. **SQL injection in `create_task` — Critical**

   Both `title` and `done` are interpolated directly into an `INSERT`. A malicious title can escape the quoted value and manipulate the statement. SQLite's `execute()` normally prevents multiple statements, but that does not make interpolation safe.

3. **No input constraints — High**

   `title` has no length limit and `done` accepts arbitrary input. This enables malformed records and resource-exhaustion attempts using very large values.

4. **No authentication or ownership checks — High if tasks are private**

   Every caller can request any task ID, and anyone can create tasks. If tasks belong to individual users, this is an insecure direct object reference/broken access-control problem. If the service is deliberately a global anonymous task board, this behavior should be explicitly documented.

5. **No abuse protection — High**

   A public anonymous caller can create unlimited tasks, growing the database until storage or service capacity is exhausted. Use rate limits, quotas, payload limits, and operational monitoring.

6. **Predictable direct identifiers — Medium if data is private**

   Sequential IDs make task enumeration trivial. Unpredictable IDs are helpful, but they do not replace authorization checks.

7. **Database details may reach logs — Low**

   Malformed queries and values can generate SQLite exceptions containing SQL fragments or attacker-controlled content. Ensure production error responses remain generic and logs are access-controlled and sanitized.

## Step 3 — Correctness pass

1. **Database connections are never closed**

   Both handlers leak connections until garbage collection. Under load, this can exhaust file descriptors and worsen SQLite locking.

2. **`task_id` has no type annotation**

   FastAPI therefore does not enforce an integer path parameter. Invalid values reach the database instead of producing an automatic `422 Unprocessable Entity` response.

3. **`title` and `done` are query parameters, not a JSON body**

   Untyped function arguments default to query parameters. A likely request such as the following will not work as expected:

   ```json
   {
     "title": "Buy milk",
     "done": false
   }
   ```

   Query strings may also be recorded in access logs and browser history.

4. **No structured request validation**

   There is no model enforcing a nonempty title, maximum length, or Boolean `done` value.

5. **Missing tasks return `200 OK`**

   A nonexistent ID produces `{"task": null}` rather than `404 Not Found`.

6. **Creation returns the wrong status and incomplete response**

   Successful creation should normally return `201 Created`, ideally with the newly generated ID and a representation or location of the resource.

7. **Database exceptions are not handled**

   Lock contention, a missing table, constraint violations, or disk errors become uncontrolled `500 Internal Server Error` responses. Expected database failures should be translated into suitable API responses, while unexpected failures should be logged safely.

8. **No guaranteed rollback or cleanup on failure**

   If insertion or commit fails, cleanup and rollback depend on connection destruction rather than explicit transaction management.

9. **`SELECT *` creates an unstable response**

   The response changes when columns are added or reordered, and it may expose columns that were not intended for clients.

10. **Raw database rows define the API response**

    The retrieved tuple is returned without field names or a declared response schema. Clients receive a positional array whose meaning is unclear and tightly coupled to column order.

11. **Boolean persistence is unspecified**

    `done` should be normalized to a known SQLite representation, normally `0` or `1`, and protected with a database constraint.

12. **Relative database path is environment-dependent**

    `"tasks.db"` resolves against the process working directory. Starting the application from another directory can silently create or access a different database.

13. **No concurrency strategy for SQLite**

    Concurrent writes can produce `database is locked` errors. A busy timeout, short transactions, appropriate journal settings, and production-load testing are needed.

## Step 4 — Maintainability pass

1. Request and response models are absent, so the API contract is undocumented and weakly typed.
2. Database creation, querying, transaction handling, and HTTP behavior are mixed inside route handlers.
3. Connection-management code is duplicated.
4. Raw SQL is assembled inline instead of using parameterized queries through a small repository or data-access layer.
5. Magic values such as `"tasks.db"` and `"ok"` are embedded in the implementation.
6. Routes lack explicit response models and documented status codes.
7. Schema assumptions—including column names, types, constraints, and migrations—are not represented in the code.
8. There is no consistent mapping between database records and named API objects.

## Step 5 — Combined findings

| Location | Issue | Severity | Why it matters | Suggested fix |
|---|---|---|---|---|
| `get_task` | SQL injection via f-string | Critical | An attacker can alter the query and potentially extract unintended database data | Annotate `task_id: int` and use `WHERE id = ?` with `(task_id,)` |
| `create_task` | SQL injection through `title` and `done` | Critical | Anonymous input can alter the `INSERT` statement | Use placeholders: `VALUES (?, ?)` |
| Entire API | No authorization or ownership checks | High if private | Callers can access arbitrary tasks and create records without identity checks | Authenticate callers and query by both task ID and owner ID |
| `create_task` | Unlimited anonymous writes | High | Attackers can fill the database or degrade availability | Add rate limits, quotas, request-size limits, monitoring, and capacity controls |
| `create_task` | No input size or value constraints | High | Oversized or malformed input can waste resources and corrupt data quality | Use a Pydantic body model with strict Boolean and bounded nonempty title |
| Task identifiers | Easily enumerable IDs | Medium if private | Sequential IDs make bulk discovery easy | Enforce authorization first; optionally expose UUIDs |
| Both handlers | Connections are never closed | High | Sustained traffic can exhaust resources and increase locking | Use a dependency or `with sqlite3.connect(...) as conn`, with explicit cleanup |
| `create_task` | Inputs unexpectedly come from the query string | Medium | JSON clients fail, and values can appear in URL logs | Accept a Pydantic request-body model |
| `get_task` | Missing task returns `200` with null | Medium | Clients cannot distinguish absence from a successful empty result | Raise `HTTPException(status_code=404)` |
| `create_task` | Returns `200` instead of `201` | Low | Violates normal REST semantics and weakens the contract | Set `status_code=201` |
| `create_task` | Does not return the created task or ID | Low | Clients cannot reliably identify the new resource | Return `lastrowid` and the created representation |
| Both handlers | Database exceptions are uncontrolled | Medium | Expected failures become generic server errors and cleanup is unreliable | Catch expected SQLite errors, safely log them, rollback, and map responses |
| `create_task` | No guaranteed rollback on failure | Medium | Failed transactions can retain locks until cleanup | Use explicit transaction and connection lifecycle management |
| `get_task` | `task_id` lacks an integer annotation | Medium | Invalid path values reach SQL and validation is bypassed | Declare `task_id: int`, optionally with a positive-value constraint |
| `get_task` | Uses `SELECT *` | Medium | Schema changes can break or expose the API unexpectedly | Select only `id`, `title`, and `done` |
| `get_task` | Returns a positional database row | Medium | Response fields are ambiguous and tied to column order | Map the row to a response model with named fields |
| Database schema | `done` representation and constraint are unspecified | Medium | Invalid completion values may be stored | Normalize to `0` or `1` and add `CHECK (done IN (0, 1))` |
| Database configuration | Relative `"tasks.db"` path | Medium | Different launch directories can use different databases | Resolve a configured absolute path |
| SQLite access | No write-concurrency strategy | Medium | Concurrent requests can fail with locking errors | Set a busy timeout, keep transactions short, consider WAL, and test load |
| Logging/error boundary | Attacker-controlled SQL fragments may appear in logs | Low | Logs can leak details or be polluted with malicious content | Return generic errors and sanitize or restrict logs |
| Both handlers | Database and HTTP logic are tightly coupled and duplicated | Low | Fixes become inconsistent and testing becomes harder | Extract connection and repository functions |
| Entire API | No request/response models | Medium | Validation and generated API documentation are incomplete | Define Pydantic `TaskCreate` and `TaskResponse` models |
| Project structure | Configuration and schema management are implicit | Low | Deployments can drift and schema changes become risky | Centralize settings and use migrations |

## Fix order

1. Replace every interpolated SQL statement with parameterized SQL.
2. Add typed Pydantic request and response models with strict, bounded validation.
3. Guarantee connection closure, transaction rollback, and safe exception handling.
4. Add authentication and per-task authorization if tasks are not intentionally public.
5. Add anonymous-write rate limiting, quotas, and request or storage limits.
6. Correct API behavior: JSON body, `404 Not Found`, `201 Created`, and return the created ID or resource.
7. Stabilize queries and storage: explicit columns, named response fields, and a Boolean constraint.
8. Configure an absolute database path and a tested SQLite concurrency strategy.
9. Extract database access and configuration into reusable components and add migrations.
