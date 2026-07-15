class RankingService:
    def __init__(self, repository):
        self._repo = repository

    def track_ranking(self, keyword: str, position: int, url: str) -> dict:
        if not keyword.strip():
            raise ValueError("keyword must not be empty")
        if position < 1:
            raise ValueError("position must be 1 or greater")
        return self._repo.add(keyword.strip().lower(), position, url)

    def list_rankings(self) -> list[dict]:
        return self._repo.get_all()

    def get_ranking(self, ranking_id: int) -> dict | None:
        return self._repo.get_by_id(ranking_id)