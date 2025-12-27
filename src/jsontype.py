from __future__ import annotations

from typing import Union


JSONDict = dict[str, 'JSONType']

JSONList = list['JSONType'] | tuple['JSONType', ...]

JSONType = Union[
    JSONDict,
    JSONList,
    str,
    int,
    float,
    bool,
    None,
]
