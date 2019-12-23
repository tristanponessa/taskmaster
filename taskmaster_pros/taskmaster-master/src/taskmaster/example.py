"""
taskmaster.example
~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""


def get_jobs(last=0, **kwargs):
    # last_job would be sent if state was resumed
    # from a previous run
    print 'Running with options: %r' % kwargs
    for i in xrange(last, 20000):
        yield i


def handle_job(i):
    pass
    # print "Got %r!" % i
