from pydantic import BaseModel
from langgraph.graph.message import MessagesState

class UserTopic(BaseModel):
    topic: str

class Source(BaseModel):
    link: str
    description: str
    score: float

class Point(BaseModel):
    title: str
    description: str
    search_query: str
    sources: list[Source]

class StudyPlanCreteation(MessagesState):
    topic: str
    points: list[Point]

class PointModel(BaseModel):
    id: int
    title: str
    description: str
    search_query: str

class DescriptionModel(BaseModel):
    source_description: str

class ScoreModel(BaseModel):
    source_score: float