from urllib.request import urlopen


def check_servers() -> list[str]:
    errors = []

    response = urlopen('http://127.0.0.1:8888')
    if response.status != 200:
        errors.append(f'nginx stub status failed: {response.status}')

    return errors
