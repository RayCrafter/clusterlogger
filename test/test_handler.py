"""
Tests for the `handler` module.
"""
import json
import logging
import logging.handlers
import sys
import uuid
import zlib

import pytest

from clusterlogger import handler

if sys.version_info[0] == 2:
    import SocketServer as socketserver
else:
    import socketserver


class TimeoutError(Exception):
    pass


class TCPHandler(socketserver.BaseRequestHandler):
    """Stores the data"""

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.server.data += self.request.recv(1024).strip()
        return


class TCPServer(socketserver.TCPServer):
    def __init__(self, *args, **kwargs):
        self.data = b''
        if sys.version_info[0] == 2:
            socketserver.TCPServer.__init__(self, *args, **kwargs)
        else:
            super(TCPServer, self).__init__(*args, **kwargs)

    def handle_timeout(self):
        raise TimeoutError('No (more) data was sent.')


@pytest.fixture(scope='function')
def tcpserver(request):
    server = TCPServer(('localhost', 0), TCPHandler, bind_and_activate=False)
    server.timeout = 0
    server.allow_reuse_address = True
    try:
        server.server_bind()
        server.server_activate()
    except:
        server.server_close()
        raise

    def close():
        server.server_close()
    request.addfinalizer(close)
    return server


def create_tcplogger(server, level, *args, **kwargs):
    h = handler.GELFTCPHandler(server.server_address[0], server.server_address[1], *args, **kwargs)
    log = logging.getLogger(str(uuid.uuid4()))
    log.addHandler(h)
    log.setLevel(level)
    return log


def handle_data(server):
    while True:
        try:
            server.handle_request()
        except TimeoutError:
            break
    return json.loads(zlib.decompress(server.data).decode('utf-8'))


def test_send(tcpserver):
    log = create_tcplogger(tcpserver, logging.INFO,)
    msg = "This is awesome"
    log.info(msg)
    data = handle_data(tcpserver)
    assert data['full_message'] == msg
    assert data['level'] == 6
