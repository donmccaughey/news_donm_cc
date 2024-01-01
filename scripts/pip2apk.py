import argparse
import stat
from dataclasses import dataclass
from pathlib import Path


def parse_options():
    arg_parser = argparse.ArgumentParser(description='Fill in variables.')
    arg_parser.add_argument('-i', '--input', dest='input', type=Path,
                            required=True, metavar='REQUIREMENTS',
                            help='the pip requirements.txt file')
    arg_parser.add_argument('-o', '--output', dest='output', type=Path,
                            required=True, metavar='APK_SCRIPT',
                            help='the generated apk script')
    return arg_parser.parse_args()


PIP_TO_APK = {
    'Flask': 'py3-flask',
}


@dataclass
class Dependency:
    name: str
    version: str

    def to_apk_package(self) -> str:
        if self.name in PIP_TO_APK:
            return PIP_TO_APK[self.name]
        else:
            return 'py3-' + self.name


def parse_requirements(requirements: list[str]) -> list[Dependency]:
    dependencies: list[Dependency] = []
    for line in requirements:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith('#'):
            continue
        if '==' not in line:
            raise RuntimeError(f'Cannot parse requirement: {line}')
        name, version = line.split('==')
        dependencies.append(Dependency(name.strip(), version.strip()))
    return dependencies


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
        requirements = input.readlines()
        dependencies = parse_requirements(requirements)

    with options.output.open('w') as output:
        apk_script = make_apk_script(dependencies)
        output.write(apk_script)
    make_executable(options.output)


if __name__ == '__main__':
    main()
