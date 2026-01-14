from typing import Callable

from pydantic import BaseModel, computed_field

from ..fields import FieldRepository
from ..schemas import FieldResponse

ActionHandler = Callable[
    ["FieldResponse", FieldRepository],
    None,
]


class Action(BaseModel):
    handler: ActionHandler
    description: str

    @computed_field
    @property
    def name(self) -> str:
        return self.handler.__qualname__
