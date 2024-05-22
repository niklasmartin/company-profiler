from pydantic import BaseModel
from post_ideas import PostIdea
from logger import get_logger

logger = get_logger("image_post")


class ImagePost(BaseModel):
    image_url: str
    caption: str

    @classmethod
    def from_idea(cls, idea: PostIdea) -> "ImagePost":
        pass
