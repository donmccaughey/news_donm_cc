from .health import Health


def test_health_good():
    health = Health()

    assert health
    assert bool(health)
    assert health.details() == '\n'
    assert health.status() == 0

    assert repr(health) == 'Health()'
    assert str(health) == 'healthy'


def test_health_bad():
    health = Health()
    health.errors.append('A process is missing')
    health.errors.append('An HTTP request failed')

    assert not health
    assert not bool(health)
    assert health.details() == 'A process is missing\nAn HTTP request failed\n'
    assert health.status() == 1

    assert repr(health) == 'Health()'
    assert str(health) == 'unhealthy'
