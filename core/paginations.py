from core.db import BaseModel


class Pagination(BaseModel):
    page: int
    size: int
    total: int = None

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size
