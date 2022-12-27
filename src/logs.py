import argparse
import json
import subprocess
import sys

from datetime import datetime, timedelta, timezone


def parse_options():
    arg_parser = argparse.ArgumentParser(description='Read logs.')
    arg_parser.add_argument('--hours', dest='hours',
                            default=1, type=int,
                            help='number of hours of events to print')
    return arg_parser.parse_args()


def main():
    options = parse_options()

    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=options.hours)
    end = now + timedelta(minutes=1)

    base_args = [
        'aws', 'lightsail', 'get-container-log',
        '--container-name', 'news',
        '--end-time', str(int(end.timestamp())),
        '--output', 'json',
        '--region', 'us-west-2',
        '--service-name', 'news',
        '--start-time', str(int(start.timestamp())),
    ]

    next_page_token = None
    while True:
        args = base_args[:]
        if next_page_token:
            args += ['--page-token', next_page_token]

        results = subprocess.run(args, capture_output=True, text=True)
        if results.returncode:
            sys.stderr.write(results.stderr)
            sys.stderr.write('\n')
            sys.exit(results.returncode)

        logs = json.loads(results.stdout)
        log_events = logs['logEvents']
        for log_event in log_events:
            created_at = log_event['createdAt']
            message = log_event['message']
            print(f'{created_at}: {message}')
        if 'nextPageToken' in logs:
            next_page_token = logs['nextPageToken']
        else:
            break


if __name__ == '__main__':
    main()
