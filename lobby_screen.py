import curses
import time

class LobbyScreen:
    def __init__(self, stdscr, net_client):
        self.stdscr = stdscr
        self.net_client = net_client
        self.ready = False
        self.game_started = False
        
    def run(self):
        self.stdscr.clear()
        self.stdscr.nodelay(True)
        
        while not self.game_started:
            self._handle_input()
            self._process_network_messages()
            self._draw_lobby()
            time.sleep(0.1)
            
        return True
        
    def _handle_input(self):
        ch = self.stdscr.getch()
        if ch == ord('r') or ch == ord('R'):
            self.ready = not self.ready
            self.net_client.set_ready(self.ready)
        elif ch == ord('q') or ch == ord('Q'):
            return False
            
    def _process_network_messages(self):
        try:
            while True:
                msg = self.net_client.inbox.get_nowait()
                mtype = msg.get("type")
                
                if mtype == "welcome":
                    self.net_client.client_id = msg.get("id")
                    self.net_client.lobby_state["players"] = msg.get("players", [])
                    
                elif mtype == "player_joined":
                    player_info = {
                        "id": msg.get("id"),
                        "name": msg.get("name"),
                        "ch": msg.get("ch"),
                        "ready": False
                    }
                    self.net_client.lobby_state["players"].append(player_info)
                    
                elif mtype == "player_left":
                    player_id = msg.get("id")
                    self.net_client.lobby_state["players"] = [
                        p for p in self.net_client.lobby_state["players"] 
                        if p.get("id") != player_id
                    ]
                    
                elif mtype == "lobby_state":
                    self.net_client.lobby_state = {
                        "players": msg.get("players", []),
                        "game_state": msg.get("game_state", "lobby"),
                        "countdown": msg.get("countdown", 0.0)
                    }
                    
                elif mtype == "game_start":
                    self.game_started = True
                    break
                    
        except Exception:
            pass
            
    def _draw_lobby(self):
        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()
        
        # Title
        title = "🎮 TERMEMOJI LOBBY 🎮"
        self.stdscr.addstr(1, (max_x - len(title)) // 2, title, curses.A_BOLD)
        
        # Room info
        room_info = f"Room: {self.net_client.room}"
        self.stdscr.addstr(3, 2, room_info)
        
        # Player list
        self.stdscr.addstr(5, 2, "Players:", curses.A_BOLD)
        players = self.net_client.lobby_state["players"]
        
        if not players:
            self.stdscr.addstr(6, 4, "No players yet...")
        else:
            for i, player in enumerate(players):
                y_pos = 6 + i
                if y_pos >= max_y - 10:
                    break
                    
                status = "✅ READY" if player.get("ready", False) else "⏳ WAITING"
                if player.get("id") == self.net_client.client_id:
                    status += " (YOU)"
                    
                player_line = f"{player.get('ch', '🙂')} {player.get('name', 'Unknown')} - {status}"
                self.stdscr.addstr(y_pos, 4, player_line)
        
        # Game state
        game_state = self.net_client.lobby_state["game_state"]
        countdown = self.net_client.lobby_state["countdown"]
        
        if game_state == "countdown" and countdown > 0:
            countdown_msg = f"🎯 GAME STARTING IN {int(countdown)} SECONDS! 🎯"
            self.stdscr.addstr(max_y - 8, (max_x - len(countdown_msg)) // 2, countdown_msg, curses.A_BOLD | curses.color_pair(2))
        elif game_state == "playing":
            start_msg = "🚀 GAME STARTED! 🚀"
            self.stdscr.addstr(max_y - 8, (max_x - len(start_msg)) // 2, start_msg, curses.A_BOLD | curses.color_pair(3))
        
        # Ready status
        ready_status = "✅ READY" if self.ready else "⏳ NOT READY"
        self.stdscr.addstr(max_y - 6, 2, f"Your status: {ready_status}")
        
        # Instructions
        instructions = [
            "Controls:",
            "R - Toggle Ready",
            "Q - Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            self.stdscr.addstr(max_y - 4 + i, 2, instruction)
        
        # Requirements
        ready_count = sum(1 for p in players if p.get("ready", False))
        total_count = len(players)
        if total_count >= 2:
            req_msg = f"Ready: {ready_count}/{total_count} players"
            if ready_count == total_count:
                req_msg += " - All ready!"
            else:
                req_msg += f" - Need {total_count - ready_count} more"
        else:
            req_msg = f"Need at least 2 players (currently {total_count})"
            
        self.stdscr.addstr(max_y - 1, 2, req_msg)
        
        self.stdscr.refresh()
