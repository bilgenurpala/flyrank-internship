import psycopg
from psycopg.rows import dict_row

class InMemoryRankingRepository:
    def __init__(self):
        self._rows = {}
        self._next_id = 1

    def add(self, keyword: str, position: int, url: str) -> dict:
        row = {"id": self._next_id, "keyword": keyword, "position": position, "url": url}
        self._rows[self._next_id] = row
        self._next_id += 1
        return row

    def get_all(self) -> list[dict]:
        return list(self._rows.values())

    def get_by_id(self, ranking_id: int) -> dict | None:
        return self._rows.get(ranking_id)

class PostgresRankingRepository:
    def __init__(self, dsn: str):
        self._dsn = dsn

    def add(self, keyword: str, position: int, url: str) -> dict:
        with psycopg.connect(self._dsn, row_factory=dict_row) as conn:
            return conn.execute(
                "INSERT INTO rankings (keyword, position, url) VALUES (%s, %s, %s) RETURNING id, keyword, position, url",
                (keyword, position, url),
            ).fetchone()

    def get_all(self) -> list[dict]:
        with psycopg.connect(self._dsn, row_factory=dict_row) as conn:
            return conn.execute(
                "SELECT id, keyword, position, url FROM rankings ORDER BY id"
            ).fetchall()

    def get_by_id(self, ranking_id: int) -> dict | None:
        with psycopg.connect(self._dsn, row_factory=dict_row) as conn:
            return conn.execute(
                "SELECT id, keyword, position, url FROM rankings WHERE id = %s",
                (ranking_id,),
            ).fetchone()