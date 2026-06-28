from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.graph.message import MessagesState
import app.ai.models as models
import app.ai.promts as prompts

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def identify_user_topic(state: models.UserTopic) -> models.UserTopic:
    prompt = prompts.user_topic_prompt.format(topic=state.topic)
    response = llm.invoke(prompt)
    return {"topic": response.content}

def validate_user_topic(state: models.UserTopic):
    if state.topic == "":
        return "unclear_topic"
    return "plan_user_study"

def create_study_plan(state: models.StudyPlanCreteation):
    prompt = prompts.study_plan_creation_prompt.format(topic=state.topic)
    response = llm.with_structured_output(list[models.PointModel]).invoke(prompt)
    return {"points": response}

def get_sources(state: models.StudyPlanCreteation):
    pass
