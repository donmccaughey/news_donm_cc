import subprocess


def check_processes() -> list[str]:
    """
    Expects Alpine Linux ``ps`` output like::

        PID   USER     TIME  COMMAND
           28 root      0:00 {nginx} /usr/bin/qemu-x86_64 /usr/sbin/nginx nginx
           30 root      0:00 {crond} /usr/bin/qemu-x86_64 /usr/sbin/crond crond -f -l 10 -L /dev/stdout
           35 root      0:00 {gunicorn} /usr/bin/qemu-x86_64 /usr/bin/python3 /usr/bin/python3 /usr/bin/gunicorn
           ...

    :return: an empty list on success or a list of errors on failure
    """
    errors = []

    results = subprocess.run('ps', capture_output=True, text=True)
    if results.returncode:
        errors.append(f'ps failed with status {results.returncode}')
        errors.append(results.stderr)
    else:
        processes = ['crond', 'nginx', 'gunicorn']
        ps_output = results.stdout
        for process in processes:
            if process not in ps_output:
                errors.append(f'{process} is not running')

    return errors
