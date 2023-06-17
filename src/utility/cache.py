from pathlib import Path


class Cache:
    def __init__(self, path: Path):
        self.path = path
        self.temp_path = path.with_suffix('.temp' + path.suffix)
        self.mtime = None
        self.json = ''

    def __repr__(self) -> str:
        return f"Cache(Path('{self.path}'))"

    def get(self) -> str:
        if self.path.is_file():
            mtime = self.path.stat().st_mtime
            if mtime != self.mtime:
                with self.path.open('r', encoding='utf-8') as f:
                    self.json = f.read()
                self.mtime = mtime
        return self.json

    def put(self, json: str):
        with self.temp_path.open('w', encoding='utf-8') as f:
            f.write(json)
        self.temp_path.rename(self.path)
        self.mtime = self.path.stat().st_mtime
        self.json = json
