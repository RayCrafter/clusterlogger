import sys
import logging
import json
import zlib
import logging.handlers

import graypy
import graypy.handler

__all__ = ['GELFTCPHandler']


class GELFTCPHandler(logging.handlers.SocketHandler):
    """Graylog Extended Log Format handler

    This handler uses TCP Sockets.
    """

    def __init__(self, host, port=12201, debugging_fields=True,
                 extra_fields=True, fqdn=False, localname=None,
                 facility=None):
        """Initialize a new GELF TCP Handler

        :param host: The host of the graylog server.
        :type host: :class:`str`
        :param port: The port of the graylog server (default 12201).
        :type port: :class:`int`
        :param debugging_fields: Send debug fields if true (the default).
        :type debugging_fields: :class:`bool`
        :param extra_fields: Send extra fields on the log record to graylog
            if true (the default).
        :type extra_fields: :class:`bool`
        :param fqdn: Use fully qualified domain name of localhost as source
            host (socket.getfqdn()).
        :type fqdn: :class:`str`
        :param localname: Use specified hostname as source host.
        :type localname: :class:`str`
        :param facility: Replace facility with specified value. If specified,
            record.name will be passed as `logger` parameter.
        :type facility: :class:`str`
        """
        self.debugging_fields = debugging_fields
        self.extra_fields = extra_fields
        self.fqdn = fqdn
        self.localname = localname
        self.facility = facility
        if sys.version_info[0] == 2:
            logging.handlers.SocketHandler.__init__(self, host, port)
        else:
            super(GELFTCPHandler, self).__init__(host, port)

    def makePickle(self, record):
        message_dict = graypy.handler.make_message_dict(
            record, self.debugging_fields, self.extra_fields, self.fqdn,
            self.localname, self.facility)
        return zlib.compress(json.dumps(message_dict).encode('utf-8'))
