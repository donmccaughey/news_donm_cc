from collections.abc import Buffer
from dataclasses import dataclass
from typing import BinaryIO


type Body = Buffer | BinaryIO


@dataclass(frozen=True, kw_only=True, slots=True)
class Entity:
    headers: dict[str, str]
    body: Body
