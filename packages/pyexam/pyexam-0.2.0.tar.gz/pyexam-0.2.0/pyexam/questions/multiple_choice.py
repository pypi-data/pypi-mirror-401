from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator

from .question import Question, QuestionType


class MultipleChoiceOption(BaseModel):
    text: Annotated[str, Field(min_length=1)]
    correct: bool = False


class MultipleChoice(Question):
    type: Literal[QuestionType.MULTIPLE_CHOICE] = QuestionType.MULTIPLE_CHOICE
    options: Annotated[list[MultipleChoiceOption], Field(min_length=2)]

    @property
    def correct_choices(self) -> list[str]:
        return [x.text for x in self.options if x.correct]

    @model_validator(mode="after")
    def check_correct_option(self):
        if not any(x.correct for x in self.options):
            raise ValueError("at least 1 option must be correct")
        return self
