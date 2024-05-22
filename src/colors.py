from pydantic import BaseModel
from logger import get_logger

logger = get_logger("colors")


class Colors(BaseModel):
    main_colors: list[str] | None = None
    background_colors: list[str] | None = None

    @classmethod
    def from_url(cls, url: str) -> "Colors":
        return cls(main_colors=["blue"], background_colors=["white"])
