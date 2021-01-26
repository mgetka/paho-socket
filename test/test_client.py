from unittest.mock import patch

import pytest

import paho_socket
import paho_socket.client


class TestSockConnectAsync:
    def test_on_tls(self):
        client = paho_socket.Client()
        client.tls_set()

        with pytest.raises(NotImplementedError):
            client.sock_connect_async("socket_path")

    def test_websocket(self):
        client = paho_socket.Client(transport="websockets")

        with pytest.raises(NotImplementedError):
            client.sock_connect_async("socket_path")

    def test_success(self):
        client = paho_socket.Client()
        client.sock_connect_async("socket_path")
        assert client._socket == "socket_path"


@patch("paho_socket.client.socket")
class TestCreateSocketConnection:
    def test_fallback_to_super_on_tcpip(self, _):
        client = paho_socket.Client()
        with patch.object(
            paho_socket.client._client.Client, "_create_socket_connection"
        ) as super_create_socket_connection:
            assert (
                client._create_socket_connection()
                is super_create_socket_connection.return_value
            )

    def test_on_socket(self, socket):
        client = paho_socket.Client()
        client.sock_connect_async("socket_path")
        assert client._create_socket_connection() is socket.socket.return_value
        socket.socket.assert_called_with(socket.AF_UNIX, socket.SOCK_STREAM)
        socket.socket.return_value.connect.assert_called_with("socket_path")

    def test_on_socket_error(self, socket):
        client = paho_socket.Client()
        client.sock_connect_async("socket_path")
        socket.socket.return_value.connect.side_effect = OSError()

        with pytest.raises(ConnectionError):
            client._create_socket_connection()


def test_sock_connect():
    client = paho_socket.Client()
    with patch.object(
        paho_socket.client._client.Client, "reconnect"
    ) as super_reconnect:
        client.sock_connect("socket_path")
    assert client._socket == "socket_path"
    super_reconnect.assert_called()
