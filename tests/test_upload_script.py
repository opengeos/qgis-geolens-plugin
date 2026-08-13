"""Regression tests for the QGIS plugin repository uploader."""

import socket
import time

import pytest

from scripts.upload_to_qgis_plugin_repo import DEFAULT_TIMEOUT, TimeoutTransport


def test_connection_carries_a_finite_timeout():
    connection = TimeoutTransport(7).make_connection("plugins.qgis.org")
    assert connection.timeout == 7


def test_default_timeout_is_finite():
    connection = TimeoutTransport().make_connection("plugins.qgis.org")
    assert connection.timeout == DEFAULT_TIMEOUT
    assert 0 < DEFAULT_TIMEOUT < 3600


def test_stalled_server_raises_instead_of_hanging():
    """A server that accepts but never answers must not block forever."""
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    host, port = listener.getsockname()
    try:
        connection = TimeoutTransport(0.5).make_connection(f"{host}:{port}")
        started = time.monotonic()
        # The TCP connect completes from the listen backlog; the TLS handshake
        # then waits on a server that never speaks.
        with pytest.raises(OSError):
            connection.connect()
        assert time.monotonic() - started < 10
    finally:
        listener.close()
