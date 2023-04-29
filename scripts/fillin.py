import argparse
from pathlib import Path


def parse_options():
    arg_parser = argparse.ArgumentParser(description='Fill in variables.')
    arg_parser.add_argument('-i', '--input', dest='input', type=Path,
                            required=True, metavar='TEMPLATE',
                            help='the template file')
    arg_parser.add_argument('-o', '--output', dest='output', type=Path,
                            required=True, metavar='GENERATED',
                            help='the generated file')
    arg_parser.add_argument('-n', '--name', dest='names', type=str,
                            action='append', metavar='NAME',
                            help='the name of the variable')
    arg_parser.add_argument('-v', '--value', dest='values', type=str,
                            action='append', metavar='VALUE',
                            help='the value of the variable')
    return arg_parser.parse_args()


def main():
    options = parse_options()
    text = ''
    with options.input.open() as f:
        text = f.read()
    for name, value in zip(options.names, options.values):
        text = text.replace('{{' + name + '}}', value)
    with options.output.open('w') as f:
        f.write(text)


if __name__ == '__main__':
    main()
