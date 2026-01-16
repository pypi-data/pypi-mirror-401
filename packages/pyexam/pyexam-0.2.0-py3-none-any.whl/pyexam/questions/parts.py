from typing import Annotated, Literal, Union

from pydantic import Field

from .fill_in import FillIn
from .long_answer import LongAnswer
from .multiple_choice import MultipleChoice
from .question import Question, QuestionType

PartsQuestionType = Annotated[Union[LongAnswer, MultipleChoice, FillIn], Field(discriminator="type")]


class Parts(Question):
    type: Literal[QuestionType.PARTS] = QuestionType.PARTS
    parts: Annotated[list[PartsQuestionType], Field(min_length=1)]
