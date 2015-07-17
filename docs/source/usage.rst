========
Usage
========

Logfilters in this case provide contextual information about the cluster platform.

To use a filter on a logger::

    import logging
    import clusterlogger

    logger = logging.getLogger(__name__)
    logger.addFilter(clusterlogger.HazelHenFilter)

Now logs are sent with contextual information of the specific cluster platform.
