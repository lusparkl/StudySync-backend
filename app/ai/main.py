from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
import os
from io import BytesIO
import requests
import pymupdf4llm
from langchain.tools import tool
import tempfile

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_pdf_file(link: str) -> BytesIO:
    response = requests.get(link, timeout=30)
    response.raise_for_status()
    
    return response.content

@tool
def get_text_from_pdf_url(link: str) -> str:
    """Gives you full text from the pdf that you send it link for. Gives it in .md format."""
    pdf_file = get_pdf_file(link)
    try:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
            tmp.write(pdf_file)
            tmp.flush()
            tmp_path = tmp.name
            text = pymupdf4llm.to_markdown(tmp.name)
            return text
    except Exception as e:
        return "Couldn't extract text from the url."
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


SYSTEM_PROMPT = """
You're a data researcher.

You work with data that user gives you and your task is to be as much useful as you can.
You are able to fetch pdf texts with your "get_text_from_pdf_url" by giving it valid pdf url.
Don't ever halucinate, if you're not sure in something better just tell that youre not sure, don't make up facts.
"""

USER_MESSAGE = """
Please read this pdf and give me all information that I must know about it. I don't know what's inside and what it's about. https://www.irs.gov/pub/irs-pdf/fw9.pdf
"""


chat_model = init_chat_model(
    "openai:gpt-4.1-mini",
    max_tokens=5000,    
)

checkpointer = InMemorySaver()

agent = create_agent(
    model=chat_model,
    tools=[get_text_from_pdf_url],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer
)

response = agent.invoke({"messages": [{"role": "user", "content": USER_MESSAGE}]},
                        config={"configurable": {"thread_id": "pdf_reading"}})
print(response["messages"][-1].content_blocks)
