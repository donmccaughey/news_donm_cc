# News

A service that finds things I'm interested in.

[![Build and Deploy][1]][2]

[1]: https://github.com/donmccaughey/news_donm_cc/actions/workflows/build-and-deploy.yaml/badge.svg
[2]: https://github.com/donmccaughey/news_donm_cc/actions/workflows/build-and-deploy.yaml


## Development Setup

1. Install `pyenv` and `pyenv-virtualenv`
2. Create the `news-venv` virtual environment using Python 3.10.9.
3. Install requirements:
   - `python3 -m pip install -r requirements.txt` 
   - `python3 -m pip install -r dev-requirements.txt`
4. Run tests: `make check`
5. Run locally for ad hoc testing: `make debug`
6. Run the container locally and shell into it: `make shell`
7. Deploy a new version from the current machine: `make deploy`
