from urllib.error import URLError
from urllib.request import urlopen


def check_servers() -> list[str]:
    errors = []

    try:
        response = urlopen('http://127.0.0.1:8888')
        if response.status != 200:
            errors.append(f'nginx stub status failed: {response.status}')
    except URLError as e:
        errors.append(f'nginx stub status failed: {e}')

    return errors
