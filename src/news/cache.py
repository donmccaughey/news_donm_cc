from pathlib import Path


class Cache:
    def __init__(self, path: Path):
        self.path = path

    def get(self) -> str:
        if self.path.is_file():
            with self.path.open('r', encoding='utf-8') as f:
                return f.read()
        else:
            return ''

    def put(self, json: str):
        with self.path.open('w', encoding='utf-8') as f:
            f.write(json)
