from pydantic import BaseModel
from logger import get_logger

logger = get_logger("post_ideas")


class PostIdea(BaseModel):
    caption: str
    image_generation_prompt: str


class PostIdeas(BaseModel):
    number_of_posts: int
    post_ideas: list[PostIdea]

    @classmethod
    def from_llm(cls, llm: str, number_of_posts: int) -> "PostIdeas":
        pass
