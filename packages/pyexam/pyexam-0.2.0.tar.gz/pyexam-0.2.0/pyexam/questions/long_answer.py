from typing import Annotated, Literal

from pydantic import Field, field_validator, model_validator

from .question import Question, QuestionType


def norm_size(size: str) -> str:
    if not (size.endswith("in") or size.endswith("cm")):
        raise ValueError("height must be cm/in")
    try:
        float(size[:-2])
    except ValueError:
        raise ValueError("invalid numeric height")
    return size


class LongAnswer(Question):
    type: Literal[QuestionType.LONG_ANSWER] = QuestionType.LONG_ANSWER
    answer: Annotated[str, Field(min_length=1)]
    lines: str = ""
    spaces: str = ""

    @field_validator("lines", "spaces", mode="before")
    def _normalize_sizes(cls, v):
        if v == "":
            return v
        return norm_size(v)

    @model_validator(mode="after")
    def check_height_sizes(self):
        lines, spaces = self.lines, self.spaces
        if (lines == "" and spaces == "") or (lines != "" and spaces != ""):
            raise ValueError("a single key lines or spaces required")
        return self
