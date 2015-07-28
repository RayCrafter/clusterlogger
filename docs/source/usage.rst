========
Usage
========

------
Filter
------

Logfilters in this case provide contextual information about the cluster platform.

To use a filter on a logger::

    import logging
    import clusterlogger

    logger = logging.getLogger(__name__)
    logger.addFilter(clusterlogger.HazelHenFilter)

Now logs are sent with contextual information of the specific cluster platform.

-------
Handler
-------

Messages are sent to Graylog using a custom handler for the builtin logging library in GELF format via TCP. For UDP use the `graypy package <https://github.com/severb/graypy>`_. Some clusters might not allow outgoing UDP connections.::

  import logging
  import clusterlogger
  
  my_logger = logging.getLogger('test_logger')
  my_logger.setLevel(logging.DEBUG)
  
  handler = clusterlogger.GELFTCPHandler('localhost', 12201)
  my_logger.addHandler(handler)
  
  my_logger.debug('Hello Graylog2.')
