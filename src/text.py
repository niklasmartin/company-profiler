from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
import html2text

from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.base_language import BaseLanguageModel
from logger import get_logger

logger = get_logger("text")


class Text(BaseModel):
    company_name: str = Field(..., description="Name of the company.")
    value_proposition: str = Field(
        ...,
        description="Core marketing message explaining what value the company offers.",
    )
    industry: str = Field(
        ..., description="Industry sector to which the company belongs."
    )
    website_url: str | None = Field(
        default=None, description="URL of the company's official website, optional."
    )
    location: str | None = Field(
        default=None,
        description="Physical location or headquarters of the company, optional.",
    )
    clients: str = Field(
        ...,
        description="Type of clients the company serves. Options: 'businesses', 'customers', 'both'.",
    )
    professionalism: str = Field(
        ...,
        description="Expected level of formality in communication. Options: 'very formal', 'formal', 'moderate', 'casual', 'very casual'.",
    )
    language_tone: str = Field(
        ...,
        description="Desired tone of the language to use. Options: 'friendly', 'assertive', 'professional', 'informative', 'enthusiastic'.",
    )

    @classmethod
    def from_url(cls, url: str, llm: BaseLanguageModel) -> "Text":
        markdown_text = url_to_markdown(url)
        attributes = extract_attributes(markdown_text, llm)
        return cls(**attributes.model_dump())


def url_to_markdown(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    converter = html2text.HTML2Text()
    converter.ignore_links = False  # Keep the links
    markdown = converter.handle(str(soup))

    logger.debug(f"Converted URL to markdown:\n{markdown}")

    return markdown


def extract_attributes(markdown_text: str, llm: BaseLanguageModel) -> Text:
    introduction = "This is the text I got from a website. Please help me extract information from it."
    query = "Extract the information according to the desired format. If not sure, take your best guess."

    parser = PydanticOutputParser(pydantic_object=Text)

    prompt = PromptTemplate(
        template="{introduction}\n{markdown_text}\n{format_instructions}\n{query}\n",
        input_variables=["introduction", "markdown_text", "query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    logger.debug(
        f"Extracting attributes from markdown text with this prompt:\n{prompt}"
    )

    chain = prompt | llm | parser

    text = chain.invoke(
        {"introduction": introduction, "markdown_text": markdown_text, "query": query}
    )

    logger.debug(f"Extracted attributes from markdown text:\n{text}")

    return text
