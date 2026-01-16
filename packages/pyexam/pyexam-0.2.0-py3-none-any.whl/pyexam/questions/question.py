from enum import Enum
from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class QuestionType(str, Enum):
    LONG_ANSWER = "long-answer"
    MULTIPLE_CHOICE = "multiple-choice"
    FILL_IN = "fill-in"
    PARTS = "parts"


class Question(BaseModel):
    type: Literal[QuestionType.LONG_ANSWER, QuestionType.MULTIPLE_CHOICE, QuestionType.FILL_IN, QuestionType.PARTS]
    text: Annotated[str, Field(min_length=1)]
    points: Annotated[Optional[int], Field(ge=0)] = None

    model_config = ConfigDict(use_enum_values=True)
