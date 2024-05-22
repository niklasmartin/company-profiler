from pydantic import BaseModel
from text import Text
from colors import Colors
from langchain.base_language import BaseLanguageModel
from logger import get_logger

logger = get_logger("company_profile")


class CompanyProfile(BaseModel):
    company_name: str
    value_proposition: str
    industry: str
    website_url: str | None = None
    location: str | None = None
    main_colors: list[str] | None = None
    background_colors: list[str] | None = None
    clients: str
    professionalism: str
    language_tone: str
    testimonials: list[str] | None = None
    achievements: list[str] | None = None

    @classmethod
    def from_url(cls, url: str, llm: BaseLanguageModel) -> "CompanyProfile":
        text = Text.from_url(url, llm)
        colors = Colors.from_url(url)
        return cls(
            company_name=text.company_name,
            value_proposition=text.value_proposition,
            industry=text.industry,
            website_url=text.website_url,
            location=text.location,
            main_colors=colors.main_colors,
            background_colors=colors.background_colors,
            clients=text.clients,
            professionalism=text.professionalism,
            language_tone=text.language_tone,
        )
