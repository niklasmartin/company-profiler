from flask import Request
from flask.typing import ResponseReturnValue
import functions_framework
from langchain_openai import ChatOpenAI

from company_profile import CompanyProfile
from logger import get_logger

logger = get_logger("main")


@functions_framework.http
def main(request: Request) -> ResponseReturnValue:
    url = request.args.get("url")
    if not url:
        return "Missing required parameter 'url'", 400
    url = sanitize_url(url)
    logger.info("New request received", extra={"request": url})
    model = ChatOpenAI(temperature=0)
    company_profile = CompanyProfile.from_url(url, model)

    return company_profile.model_dump_json(), 200


def sanitize_url(url: str) -> str:
    if not url.startswith("http"):
        return f"https://{url}"
    return url
