`paho-socket`
=================================================

This package features a thin layer built on top of
[paho-mqtt](https://github.com/eclipse/paho.mqtt.python) allowing for connections with unix socket
brokers. The package was built with my other projects in mind, and at the moment it only has
features I've found useful so far. To be more precise, it allows:

 - Connecting to unix socket based brokers supporting plaintext MQTT protocol.

Following features are not supported:

 - TLS over unix socket,
 - MQTT over websocket over unix socket.

All the base features of paho-mqtt are still available using the package provided class.

The package is based on paho-mqtt 1.5.1, and since it utilizes non public methods and attributes of
the original client it may not work with other versions.

## Installation

Package can be installed from PyPI:
```
pip install paho-socket
```

## Connection establishing

The package provides a class that inherits from the paho-mqtt `Client`. It's interface is extended
with `sock_connect` and `sock_connect_async` methods, which should be used in the similar manner as
those intended for creation of TCP/IP based connections. Once the connection is established, all the
paho-mqtt feature work as in the original package, including reconnects.

## Tests

To perform test activities, it is necessary to install dependencies contained in
`requirements-dev.txt`.

```
python setup.py develop
pip install -e '.[dev]'
```

To run automatic tests, run the following command

```
pytest --cov=paho_socket
```

## License

This code is released under the [EPL](LICENSE).
