import socket
import threading
import json
import queue

class NetClient:
    def __init__(self, host="127.0.0.1", port=8765):
        self.host = host
        self.port = port
        self.sock = None
        self.recv_thread = None
        self.inbox = queue.Queue()
        self.alive = False
        self.client_id = None
        self.room = None

    def connect(self, timeout=5.0):
        self.sock = socket.create_connection((self.host, self.port), timeout=timeout)
        # Switch to blocking mode after connectt timeout tab
        try:
            self.sock.settimeout(None)
        except Exception:
            pass
        self.alive = True
        self.recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
        self.recv_thread.start()

    def close(self):
        self.alive = False
        try:
            if self.sock:
                self.sock.close()
        except OSError:
            pass

    def _send(self, obj):
        try:
            data = (json.dumps(obj, separators=(",", ":")) + "\n").encode("utf-8")
            self.sock.sendall(data)
        except OSError:
            self.close()

    def join(self, room, name, ch):
        self._send({"type": "join", "room": room, "name": name, "ch": ch})

    def send_state(self, x, y, hp):
        self._send({"type": "state", "x": x, "y": y, "hp": hp})

    def send_attack(self, x, y, dir):
        self._send({"type": "attack", "x": x, "y": y, "dir": dir})

    def leave(self):
        self._send({"type": "leave"})

    def _recv_loop(self):
        buffer = b""
        try:
            while self.alive:
                try:
                    data = self.sock.recv(4096)
                except (socket.timeout, TimeoutError):
                    continue
                if not data:
                    break
                buffer += data
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    if not line:
                        continue
                    try:
                        msg = json.loads(line.decode("utf-8"))
                    except json.JSONDecodeError:
                        continue
                    self.inbox.put(msg)
        finally:
            self.alive = False
            try:
                self.sock.close()
            except OSError:
                pass
