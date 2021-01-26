"""Socket capable client extension implementation."""
import socket

from paho.mqtt import client as _client


class Client(_client.Client):
    """UNIX socket capable paho mqtt client."""

    # pylint: disable=redefined-outer-name,too-many-instance-attributes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._socket = None

    def sock_connect(
        self,
        socket,
        keepalive=60,
        clean_start=_client.MQTT_CLEAN_START_FIRST_ONLY,
        properties=None,
    ):
        """Connect to a remote broker via UNIX socket.

        socket is the path to broker unix socket.
        keepalive: Maximum period in seconds between communications with the
        broker. If no other messages are being exchanged, this controls the
        rate at which the client will send ping messages to the broker.
        clean_start: (MQTT v5.0 only) True, False or MQTT_CLEAN_START_FIRST_ONLY.
        Sets the MQTT v5.0 clean_start flag always, never or on the first successful connect only,
        respectively.  MQTT session data (such as outstanding messages and subscriptions)
        is cleared on successful connect when the clean_start flag is set.
        properties: (MQTT v5.0 only) the MQTT v5.0 properties to be sent in the
        MQTT"""

        if self._protocol == _client.MQTTv5:  # pragma: no cover
            self._mqttv5_first_connect = True
        else:  # pragma: no cover
            if clean_start != _client.MQTT_CLEAN_START_FIRST_ONLY:
                raise ValueError("Clean start only applies to MQTT V5")
            if properties is not None:
                raise ValueError("Properties only apply to MQTT V5")

        self.sock_connect_async(socket, keepalive, clean_start, properties)
        return self.reconnect()

    def sock_connect_async(
        self,
        socket,
        keepalive=60,
        clean_start=_client.MQTT_CLEAN_START_FIRST_ONLY,
        properties=None,
    ):
        """Connect to a remote broker asynchronously using UNIX domain socket. This is a
        non-blocking connect call that can be used with loop_start() to provide very quick
        start.
        socket is the path to broker unix socket.
        keepalive: Maximum period in seconds between communications with the
        broker. If no other messages are being exchanged, this controls the
        rate at which the client will send ping messages to the broker.
        clean_start: (MQTT v5.0 only) True, False or MQTT_CLEAN_START_FIRST_ONLY.
        Sets the MQTT v5.0 clean_start flag always, never or on the first successful connect only,
        respectively.  MQTT session data (such as outstanding messages and subscriptions)
        is cleared on successful connect when the clean_start flag is set.
        properties: (MQTT v5.0 only) the MQTT v5.0 properties to be sent in the
        MQTT connect packet.  Use the Properties class.
        """
        if keepalive < 0:  # pragma: no cover
            raise ValueError("Keepalive must be >=0.")
        if self._ssl:
            raise NotImplementedError(
                "TLS support for AF_UNIX sockets is not implemented."
            )
        if self._transport != "tcp":
            raise NotImplementedError(
                "Only tcp transport is supported for UNIX socket connections."
            )

        self._socket = socket
        self._keepalive = keepalive
        self._clean_start = (  # pylint: disable=attribute-defined-outside-init
            clean_start
        )
        self._connect_properties = properties
        self._state = _client.mqtt_cs_connect_async

        # We need to pas some junk data here, since for some unknown reason reconnect checks
        # validity of those field on each reconnect, even though they are already validated by
        # connect_async.
        self._host = "undefined"
        self._port = 9

    def _create_socket_connection(self):
        if self._socket is None:
            return super()._create_socket_connection()

        # Proxy servers are not applicable in AF_UNIX, so we silently ignore them.

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.connect(self._socket)
        except OSError as ex:
            # UNIX socket exceptions are much richer than TCP/IP ones - we will narrow it down to
            # ConnectionError for better compatibility with clients prepared just for TCP/IP.
            raise ConnectionError("Socket connection failed.") from ex
        return sock
