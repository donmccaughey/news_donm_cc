import argparse
import json
import subprocess


def parse_options():
    arg_parser = argparse.ArgumentParser(description='Read logs.')
    arg_parser.add_argument('-c', '--count', dest='count',
                            default=100, type=int,
                            help='number of log events to print')
    return arg_parser.parse_args()


def main():
    options = parse_options()
    base_args = [
        'aws', 'lightsail', 'get-container-log',
        '--service-name', 'news',
        '--container-name', 'news',
        '--region', 'us-west-2',
        '--output', 'json',
    ]

    event_count = 0
    next_page_token = None
    while event_count < options.count:
        args = base_args[:]
        if next_page_token:
            args += ['--page-token', next_page_token]
        print(args)
        results = subprocess.run(args, capture_output=True, text=True)
        results.check_returncode()
        logs = json.loads(results.stdout)
        log_events = logs['logEvents']
        for log_event in log_events:
            created_at = log_event['createdAt']
            message = log_event['message']
            print(f'{created_at}: {message}')
        event_count += len(log_events)
        if 'nextPageToken' not in logs:
            print('No next page')
            break
        next_page_token = logs['nextPageToken']
        print(f'next_page_token = {next_page_token}')


if __name__ == '__main__':
    main()
