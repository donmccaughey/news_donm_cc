from typing import Mapping, Sequence


type JSONArray = Sequence[JSONType]

type JSONObject = Mapping[str, JSONType]

type JSONType = bool | float | int | JSONArray | JSONObject | None | str
