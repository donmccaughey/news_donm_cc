import sys

import health


def main():
    errors = []

    errors += health.check_processes()
    errors += health.check_servers()
    errors += health.check_jobs()

    if errors:
        sys.stderr.write('\n'.join(errors) + '\n')
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
