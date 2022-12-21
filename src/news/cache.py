from pathlib import Path


class Cache:
    def __init__(self, path: Path):
        self.path = path
        self.mtime = None
        self.contents = ''

    def get(self) -> str:
        if self.path.is_file():
            mtime = self.path.stat().st_mtime
            if mtime != self.mtime:
                with self.path.open('r', encoding='utf-8') as f:
                    self.contents = f.read()
                self.mtime = mtime
        return self.contents

    def put(self, json: str):
        with self.path.open('w', encoding='utf-8') as f:
            f.write(json)
        self.mtime = self.path.stat().st_mtime
        self.contents = json
