import os
import queue
import socket


class SelectQueue(queue.Queue):
    def __init__(self):
        super().__init__()
        if os.name == "posix":
            self._put_socket, self._get_socket = socket.socketpair()
        else:
            # Emulate socketpair() syscall on Windows
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(("127.0.0.1", 0))
            server.listen(1)
            self._put_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._put_socket.connect(server.getsockname())
            self._get_socket, _ = server.accept()
            server.close()

    def fileno(self):
        return self._get_socket.fileno()

    def close(self):
        self._put_socket.close()
        self._get_socket.close()

    def put(self, item):
        super().put(item)
        self._put_socket.send(b"\x00")

    def get(self):
        self._get_socket.recv(1)
        return super().get()
