from typing import Mapping, Sequence


type JSONDict = Mapping[str, JSONType]

type JSONList = Sequence[JSONType]

type JSONType = JSONDict | JSONList | str | int | float | bool | None
