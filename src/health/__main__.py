import sys
from datetime import datetime, timezone

from health import Health, parse_options
from utility import iso


options = parse_options()

health = Health()
if not options.startup:
    health.check()

health_path = options.cache_dir / 'healthy.txt'
if health:
    now = datetime.now(timezone.utc)
    health_path.write_text(f'{iso(now)} Healthy.\n')
else:
    health_path.unlink(missing_ok=True)
    sys.stderr.write(health.details())

sys.exit(health.status())
