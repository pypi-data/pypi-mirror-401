from docker.models.containers import Container

from .config import get_logger

log = get_logger()


def c2port(c: Container) -> int:
    try:
        return int(c.labels['ingress.port'])
    except (KeyError, TypeError):
        try:
            ports = list(c.ports.keys())
            # ['443/tcp', '5555/tcp'] --> 443
            port = ports[0].split('/')[0]
            log.debug(
                'missing ingress.port label; falling back to first exposed port',
                extra={'name': c.name},
                port=port,
            )
        except (AttributeError, IndexError):
            port = 80
            log.debug(
                'neither ingress.port label set nor ports exposed. defaulting',
                extra={'name': c.name},
                port=port,
            )
        return port
