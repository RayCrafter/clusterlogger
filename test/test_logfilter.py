"""
Tests for `logfilter` module.
"""
import os
import socket

import pytest

from clusterlogger import logfilter


class DummyRecord(object):
    pass


@pytest.fixture(scope='module')
def hazelhen_environ(request):
    envvars = {'PBS_JOBID': '28572',
               'PBS_O_LOGNAME': 'hpcmscuser',
               'PBS_JOBNAME': 'loggingtest',
               'PBS_QUEUE': 'test',
               'SITE_NAME': 'HLRS',
               'SITE_PLATFORM_NAME': 'hazelhen'}
    oldvars = {}
    for k, v in envvars.items():
        oldvars[k] = os.environ.get(k, '')
        os.environ[k] = v

    def restore():
        os.environ.update(oldvars)
    request.addfinalizer(restore)


@pytest.mark.parametrize('attr,envvar',
                         [('jobid', 'PBS_JOBID'),
                          ('submitter', 'PBS_O_LOGNAME'),
                          ('jobname', 'PBS_JOBNAME'),
                          ('queue', 'PBS_QUEUE'),
                          ('sitename', 'SITE_NAME'),
                          ('platform', 'SITE_PLATFORM_NAME')])
def test_hazelhen_filter_envvar(hazelhen_environ, attr, envvar):
    hhf = logfilter.HazelHenFilter()
    record = DummyRecord()
    hhf.filter(record)
    assert getattr(record, attr) == os.environ[envvar],\
        'Filter did not add envvar %s to the logrecord attribute %s.' % (envvar, attr)


def test_hazelhen_filter_fqdn(hazelhen_environ):
    hhf = logfilter.HazelHenFilter()
    record = DummyRecord()
    hhf.filter(record)
    assert record.fqdn == socket.getfqdn()
