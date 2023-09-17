from pathlib import Path


class CachedFile:
    def __init__(self, path: Path):
        self.path = path
        self.temp_path = path.with_suffix('.temp' + path.suffix)
        self.mtime = None
        self.contents = ''

    def __repr__(self) -> str:
        return f"CachedFile(Path('{self.path}'))"

    def is_invalid(self) -> bool:
        return self.path.is_file() and self.path.stat().st_mtime != self.mtime

    def read(self) -> str:
        if self.path.is_file():
            mtime = self.path.stat().st_mtime
            if mtime != self.mtime:
                with self.path.open('r', encoding='utf-8') as f:
                    self.contents = f.read()
                self.mtime = mtime
        return self.contents

    def write(self, contents: str):
        with self.temp_path.open('w', encoding='utf-8') as f:
            f.write(contents)
        self.temp_path.rename(self.path)
        self.mtime = self.path.stat().st_mtime
        self.contents = contents
