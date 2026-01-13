from typing_extensions import Literal

from _hydrogenlib_core.network import parse_remote_addr
from .base import SocketBase
from .global_registry import register_socket_protocol
from .socket_consts import *
from .methods import *

Options = TCPOptions


class ConnectedTcpSocket(SocketBase):
    def __init__(self, sock):
        self._sock = sock

    def send(self, data: bytes):
        return self._sock.send(data)

    def recv(self, size: int = None):
        return self._sock.recv(size if size is not None else -1)


@register_socket_protocol('tcp')
class TcpSocket(SocketBase):
    def __init__(self, sock):
        self._sock = sock

    @classmethod
    def new(cls, ip_type: Literal['v4', 'v6'] = 'v4'):
        return cls(
            socket.socket(
                AddressFamily.Inet if ip_type == 'v4' else AddressFamily.Inet6,
                SocketKind.TCP
            )
        )

    @classmethod
    def connect(cls, remote_addr, timeout=5):
        host, port = parse_remote_addr(remote_addr)
        if port is None:
            port = 80

        results = getaddrinfo(host, port, type=SocketKind.TCP, proto=IPProtocol.TCP)
        


