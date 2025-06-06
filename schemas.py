from pydantic import BaseModel, validator
from typing import List

class CurriculumRequest(BaseModel):
    topic: str

class Resource(BaseModel):
    url: str
    description: str

class QuizQuestion(BaseModel):
    question: str
    answers: List[str]
    correct_answer_index: int

class CurriculumModule(BaseModel):
    module_number: int
    title: str
    description: str
    resources: List[Resource]
    exercise: str
    quiz: List[QuizQuestion]

class CurriculumResponse(BaseModel):
    topic: str
    curriculum: List[CurriculumModule]
