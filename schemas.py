from typing import List
from pydantic import BaseModel

class Resource(BaseModel):
    """Represents an external resource link."""
    url: str
    description: str

class QuizQuestion(BaseModel):
    """Represents a question in the quiz."""
    question: str
    answers: List[str]
    correct_answer_index: int

class CurriculumModule(BaseModel):
    """A single module in the curriculum."""
    module_number: int
    title: str
    description: str
    resources: List[Resource]
    exercise: str
    quiz: List[QuizQuestion]

class CurriculumResponse(BaseModel):
    """Response model for the generated curriculum."""
    topic: str
    curriculum: List[CurriculumModule]

class CurriculumRequest(BaseModel):
    """Request model containing the desired topic."""
    topic: str
