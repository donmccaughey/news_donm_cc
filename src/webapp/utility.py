from pathlib import Path


def get_version() -> str:
    version_path = Path('version.txt')
    if version_path.exists():
        try:
            with version_path.open() as f:
                version = f.read().strip()
                if version:
                    return version
        except OSError:
            pass
    return 'unknown'
