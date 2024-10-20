import argparse
import stat
import tomllib
from dataclasses import dataclass
from pathlib import Path


def parse_options():
    arg_parser = argparse.ArgumentParser(description='Generate apk script to add `py3-` packages.')
    arg_parser.add_argument('-i', '--input', dest='input', type=Path,
                            required=True, metavar='PYPROJECT',
                            help='the `pyproject.toml` file')
    arg_parser.add_argument('-o', '--output', dest='output', type=Path,
                            required=True, metavar='APK_SCRIPT',
                            help='the generated apk script')
    return arg_parser.parse_args()


PYPI_TO_APK_MAP = {
    'Flask': 'py3-flask',
}


@dataclass
class Dependency:
    name: str
    version: str

    @classmethod
    def from_pyproject(cls, dependency: str) -> 'Dependency':
        if '==' in dependency:
            name, version = dependency.split('==', 1)
        else:
            name = dependency
            version = ''
        return Dependency(name.strip(), version.strip())


    def to_apk_package(self) -> str:
        if self.name in PYPI_TO_APK_MAP:
            return PYPI_TO_APK_MAP[self.name]
        else:
            return 'py3-' + self.name


def parse_pyproject(pyproject_toml: str) -> list[Dependency]:
    pyproject = tomllib.loads(pyproject_toml)
    dependencies = pyproject['project']['dependencies']
    return [Dependency.from_pyproject(dep) for dep in dependencies]


def make_apk_script(dependencies: list[Dependency]) -> str:
    lines = [
        '#!/bin/sh',
        'apk add --no-cache \\',
    ]
    for i, dependency in enumerate(dependencies):
        line = '    ' + dependency.to_apk_package()
        if i != len(dependencies) - 1:
            line += ' \\'
        lines.append(line)
    lines.append('')
    return '\n'.join(lines)


def make_executable(path: Path):
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main():
    options = parse_options()
    with options.input.open('r') as input:
        pyproject_toml = input.read()
        dependencies = parse_pyproject(pyproject_toml)

    with options.output.open('w') as output:
        apk_script = make_apk_script(dependencies)
        output.write(apk_script)
    make_executable(options.output)


if __name__ == '__main__':
    main()
