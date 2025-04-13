from typing import List, Optional, Annotated
from pydantic import BaseModel, Field, BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class OnboardTopic(BaseModel):
    name: str
    text: str | None = None
    question: str | None = None
    answer: str | None = None

class OnboardSection(BaseModel):
    name: str
    callback_data: str
    topics: List[OnboardTopic]

class OnboardCourse(BaseModel):
    name: str
    is_main: bool = False
    is_active: bool = True
    sections: List[OnboardSection]
    
    
class FAQ(BaseModel):
    question: str
    answer: str

class FAQTopic(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    faqs: list[FAQ] = []