from pydantic import BaseModel as BaseSchema
from pydantic import ConfigDict


class ForbidSchema(BaseSchema):
    model_config = ConfigDict(extra="forbid")
