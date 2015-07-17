import logging
import os
import socket

__all__ = ['HazelHenFilter']


class HazelHenFilter(logging.Filter):
    """Filter for adding contextual information on ``Hazel Hen``

    `Hazel Hen <http://www.hlrs.de/systems/platforms/cray-xc40-hazel-hen/>`_
    is the Cray XC40 system at HLRS in Stuttgart.

    This filter adds information about the currently running job.
    """
    def __init__(self):
        """Initialize a new HazelHenFilter

        :raises: None
        """
        self.jobid = os.environ.get('PBS_JOBID', -1)
        """The job identifier assigned to the job by the batch system.
        This is the same number you see when you do qstat.
        -1 if logging when not running in a job.
        """
        self.logname = os.environ.get('PBS_O_LOGNAME')
        """Value of the LOGNAME variable in the environment in which qsub was executed"""
        self.jobname = os.environ.get('PBS_JOBNAME')
        """The job name supplied by the user"""
        self.queue = os.environ.get('PBS_QUEUE')
        """The name of the queue from which the job is executed"""
        self.fqdn = socket.getfqdn()
        """The fully qualified domain name."""
        self.sitename = os.environ.get('SITE_NAME')
        """The site name of the cluster"""
        self.platform = os.environ.get('SITE_PLATFORM_NAME')
        """The cluster platform on the site. E.g. ``hazelhen``."""

    def filter(self, record):
        """Add contextual information to the log record

        :param record: the log record
        :type record: :class:`logging.LogRecord`
        :returns: True, if log should get sent
        :rtype: :class:`bool`
        :raises: None
        """
        record.sitename = self.sitename
        record.platform = self.platform
        record.jobid = self.jobid
        record.submitter = self.logname
        record.jobname = self.jobname
        record.queue = self.queue
        record.fqdn = self.fqdn
        return True
