from time import sleep

import paho.mqtt.client
import pytest

import paho_socket


@pytest.mark.slow
def test_communication(broker):

    recv_socket_message = False
    recv_tcp_message = False

    def socket_message(mqttc, obj, msg):
        nonlocal recv_tcp_message
        if msg.payload == b"tcp_message":
            recv_tcp_message = True

    def tcp_message(mqttc, obj, msg):
        nonlocal recv_socket_message
        if msg.payload == b"socket_message":
            recv_socket_message = True

    tcp = paho.mqtt.client.Client()
    tcp.on_message = tcp_message
    tcp.connect("127.0.0.1", 8520)

    socket = paho_socket.Client()
    socket.on_message = socket_message
    socket.sock_connect("/tmp/paho_socket_test.sock")

    tcp.subscribe("tcp")
    tcp.loop()

    socket.subscribe("socket")
    socket.loop()

    tcp.publish("socket", b"tcp_message")
    tcp.loop()
    socket.loop()
    socket.publish("tcp", b"socket_message")
    socket.loop()
    tcp.loop()

    assert recv_socket_message
    assert recv_tcp_message
