import httpx
import asyncio
from dotenv import load_dotenv
import os
from io import BytesIO
import requests
import pymupdf4llm
import tempfile

load_dotenv()
OPEN_ALEX_API_KEY = os.getenv("OPEN_ALEX_API_KEY")

async def get_relevant_papers(query: str) -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.openalex.org/works?api_key={OPEN_ALEX_API_KEY}&filter=has_pdf_url:true&search={query}&per_page=25")
        return response.json()

def get_pdf_file(link: str) -> BytesIO:
    response = requests.get(link, timeout=30)
    response.raise_for_status()

    return response.content

def get_text_from_pdf_url(link: str) -> str:
    """Gives you full text from the pdf that you send it link for. Gives it in .md format."""
    pdf_file = get_pdf_file(link)
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(pdf_file)
            tmp.flush()
            tmp_path = tmp.name
            text = pymupdf4llm.to_markdown(tmp_path)
            return text
    except Exception as e:
        return "Couldn't extract text from the url."
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    
async def main(query: str):
    response = await get_relevant_papers(query)
    for result in response["results"]:
        pdf_url = result["best_oa_location"]["pdf_url"]
        if pdf_url:
            try:
                print(get_text_from_pdf_url(pdf_url))
            except:
                continue

