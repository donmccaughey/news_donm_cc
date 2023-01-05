from .jobs import check_jobs
from .processes import check_processes
from .servers import check_servers


class Health:
    def __init__(self):
        self.errors = []

    def __bool__(self) -> bool:
        return False if self.errors else True

    def __repr__(self) -> str:
        return 'Health()'

    def __str__(self) -> str:
        return 'healthy' if self else 'unhealthy'

    def check(self):
        self.errors += check_processes()
        self.errors += check_servers()
        self.errors += check_jobs()

    def details(self) -> str:
        return '\n'.join(self.errors) + '\n'

    def status(self) -> int:
        return 0 if self else 1
