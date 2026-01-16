from typing import Literal

from pydantic import model_validator

from .question import Question, QuestionType


class FillIn(Question):
    type: Literal[QuestionType.FILL_IN] = QuestionType.FILL_IN

    @model_validator(mode="after")
    def check_text_separator(self):
        count = self.text.count("\\fillin[")
        if count == 0:
            raise ValueError("unused separator")
        return self
