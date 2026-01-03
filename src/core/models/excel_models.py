from pydantic import Field

from .base.from_attributes import FromAttributesModel

FILENAME_MAX_LEN = 1024


class RawExcelModel(FromAttributesModel):
    id: int
    filename: str = Field(max_length=FILENAME_MAX_LEN)
    data: dict
