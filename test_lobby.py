import socket
import json
import threading
import time

def test_server_connection():
    try:
        sock = socket.create_connection(("127.0.0.1", 8765), timeout=5)
        print("Connected to server")
        
        join_msg = {"type": "join", "room": "test_room", "name": "TestPlayer", "ch": "😎"}
        data = (json.dumps(join_msg) + "\n").encode("utf-8")
        sock.sendall(data)
        print("Sent join msg")
        
        buffer = b""
        while b"\n" not in buffer:
            data = sock.recv(4096)
            if not data:
                break
            buffer += data
            
        line, buffer = buffer.split(b"\n", 1)
        msg = json.loads(line.decode("utf-8"))
        print(f"Rec: {msg.get('type')}")
        
        ready_msg = {"type": "ready", "ready": True}
        data = (json.dumps(ready_msg) + "\n").encode("utf-8")
        sock.sendall(data)
        print("Sent ready msg")
        
        sock.close()
        print("Test completed successfully")
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing lobby sys...")
    success = test_server_connection()
    if success:
        print("\nLobby sys is working!")
    else:
        print("\nLobby sys has issues!")
