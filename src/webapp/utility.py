from pathlib import Path


def get_version() -> str:
    version_path = Path('version.txt')
    if version_path.exists():
        with version_path.open() as f:
            return f.read().strip()
    else:
        return 'unknown'
