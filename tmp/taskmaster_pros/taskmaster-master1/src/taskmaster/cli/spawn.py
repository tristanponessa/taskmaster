"""
taskmaster.cli.spawn
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

from multiprocessing import Process
from taskmaster.cli.slave import run as run_slave
from taskmaster.constants import (
    DEFAULT_ADDRESS,
    DEFAULT_LOG_LEVEL,
    DEFAULT_RETRIES,
    DEFAULT_TIMEOUT,
)


def run(target, procs, **kwargs):
    pool = []
    for n in xrange(procs):
        pool.append(Process(target=run_slave, args=[target], kwargs=kwargs))

    for p in pool:
        p.start()

    for p in (p for p in pool if p.is_alive()):
        p.join(0)


def main():
    import optparse
    import sys
    parser = optparse.OptionParser()
    parser.add_option("--address", dest="address", default=DEFAULT_ADDRESS)
    parser.add_option("--log-level", dest="log_level", default=DEFAULT_LOG_LEVEL)
    parser.add_option("--retries", dest="retries", default=DEFAULT_RETRIES, type=int)
    parser.add_option("--timeout", dest="timeout", default=DEFAULT_TIMEOUT, type=int)
    (options, args) = parser.parse_args()
    if len(args) != 2:
        print 'Usage: tm-spawn <callback> <processes>'
        sys.exit(1)
    sys.exit(run(args[0], procs=int(args[1]), progressbar=False, **options.__dict__))

if __name__ == '__main__':
    main()
