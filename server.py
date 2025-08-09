import socket
import socketserver
import threading
import json
import uuid

rooms_lock = threading.Lock()
rooms = {}
# rooms: {room_id: {"clients": set(ClientHandler), "names": {handler: {"id": str, "name": str, "ch": str}}}}

class ClientHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.buffer = b""
        self.room_id = None
        self.client_id = None
        self.name = None
        self.ch = None

    def handle(self):
        try:
            for msg in self._iter_messages():
                self._handle_message(msg)
        except ConnectionError:
            pass
        finally:
            self._leave_room()

    def _iter_messages(self):
        while True:
            data = self.request.recv(4096)
            if not data:
                raise ConnectionError
            self.buffer += data
            while b"\n" in self.buffer:
                line, self.buffer = self.buffer.split(b"\n", 1)
                if not line:
                    continue
                try:
                    msg = json.loads(line.decode("utf-8"))
                    yield msg
                except json.JSONDecodeError:
                    continue

    def _handle_message(self, msg):
        mtype = msg.get("type")
        if mtype == "join":
            room = str(msg.get("room") or "lobby")
            name = str(msg.get("name") or "anonymous")
            ch = str(msg.get("ch") or "🙂")
            self._join_room(room, name, ch)
        elif mtype in ("state", "attack", "leave"):
            self._relay_to_room(msg)
        else:
            pass

    def _send(self, obj):
        try:
            data = (json.dumps(obj, separators=(",", ":")) + "\n").encode("utf-8")
            self.request.sendall(data)
        except OSError:
            pass

    def _join_room(self, room_id, name, ch):
        if self.room_id:
            self._leave_room()
        self.room_id = room_id
        self.client_id = uuid.uuid4().hex[:8]
        self.name = name
        self.ch = ch
        with rooms_lock:
            room = rooms.setdefault(room_id, {"clients": set(), "names": {}})
            room["clients"].add(self)
            room["names"][self] = {"id": self.client_id, "name": name, "ch": ch}
            # Send existing players to this client
            existing = [v for h, v in room["names"].items() if h is not self]
        self._send({"type": "welcome", "id": self.client_id, "room": room_id, "players": existing})
        # Notify others about this join
        self._broadcast_to_room({"type": "player_joined", "id": self.client_id, "name": name, "ch": ch}, exclude_self=True)

    def _leave_room(self):
        if not self.room_id:
            return
        with rooms_lock:
            room = rooms.get(self.room_id)
            if room:
                if self in room["clients"]:
                    room["clients"].remove(self)
                if self in room["names"]:
                    info = room["names"].pop(self)
                else:
                    info = {"id": self.client_id}
                if not room["clients"]:
                    rooms.pop(self.room_id, None)
            else:
                info = {"id": self.client_id}
        self._broadcast_to_room({"type": "player_left", "id": info.get("id")}, exclude_self=True)
        self.room_id = None

    def _broadcast_to_room(self, obj, exclude_self=False):
        room_id = self.room_id
        if not room_id:
            return
        with rooms_lock:
            room = rooms.get(room_id)
            if not room:
                return
            clients = list(room["clients"])
        data = (json.dumps(obj, separators=(",", ":")) + "\n").encode("utf-8")
        for h in clients:
            if exclude_self and h is self:
                continue
            try:
                h.request.sendall(data)
            except OSError:
                pass

    def _relay_to_room(self, msg):
        if not self.room_id:
            return
        msg = dict(msg)
        if "id" not in msg and self.client_id:
            msg["id"] = self.client_id
        self._broadcast_to_room(msg, exclude_self=True)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    with ThreadedTCPServer((args.host, args.port), ClientHandler) as server:
        print(f"Server listening on {args.host}:{args.port}")
        server.serve_forever()
