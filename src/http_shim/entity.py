from dataclasses import dataclass

from .body import Body
from .headers import Headers


@dataclass(frozen=True, kw_only=True, slots=True)
class Entity:
    headers: Headers
    body: Body
