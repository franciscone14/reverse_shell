## Python Reverse Shell - Server Side

Python application that allows to receive multiples connection in a host. The script uses pure python3 and does not require any 3th party libraries.

## Usage

```sh
sudo ./reverse_tcp.py 0.0.0.0 80
```

## Client side connection
```sh
nc localhost 80
```

## Common commands
- session list: list all the sessions available
- session start \<id>\: start a session for a given id
- session kill \<id>\: Ends the connection for a given id
- exit: Finishes the current opened session