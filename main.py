import curses
import time
import random
import math
import queue

from utils import (
    FPS, DT, KEY_LEFT, KEY_RIGHT, KEY_JUMP, KEY_ATTACK, 
    KEY_SPECIAL, KEY_QUIT, setup_colors, get_random_position
)
from models import Entity, Projectile, PowerUp, Particle
from ai import AIController, create_ai_entities
from renderer import Renderer
from game_logic import GameLogic
from net_client import NetClient
from lobby_screen import LobbyScreen
from simple_char_select import SimpleCharacterSelect
from characters import get_character, get_character_display_name, get_character_char


def prompt_text(stdscr, y, x, prompt, default=""):
    curses.echo()
    stdscr.move(y, x)
    stdscr.clrtoeol()
    stdscr.addstr(y, x, f"{prompt} [{default}]: ")
    stdscr.refresh()
    s = stdscr.getstr(y, x + len(prompt) + 3 + len(str(default)), 60)
    curses.noecho()
    txt = s.decode("utf-8").strip() if s else ""
    return txt if txt else str(default)


def choose_menu(stdscr):
    stdscr.clear()
    stdscr.addstr(2, 4, "TermEmoji")
    stdscr.addstr(4, 4, "1) Singleplayer")
    stdscr.addstr(5, 4, "2) Multiplayer: Join Room")
    stdscr.addstr(6, 4, "3) Multiplayer: Create Room")
    stdscr.addstr(7, 4, "4) Character Selection")
    stdscr.addstr(9, 4, "Q) Quit")
    stdscr.refresh()
    while True:
        ch = stdscr.getch()
        if ch in (ord('1'), ord('2'), ord('3'), ord('4'), ord('q'), ord('Q')):
            stdscr.clear()
            stdscr.refresh()
            return chr(ch)


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)
    max_y, max_x = stdscr.getmaxyx()

    ground_row = max_y - 6

    renderer = Renderer(stdscr)
    game_logic = GameLogic(max_x, max_y, ground_row)
    ai_controller = AIController()

    mode = choose_menu(stdscr)
    if mode in ('q', 'Q'):
        return
    elif mode == '4':
        char_select = SimpleCharacterSelect(stdscr)
        selected_char = char_select.run()
        if selected_char:
            stdscr.clear()
            stdscr.addstr(10, 4, f"Selected: {get_character_display_name(selected_char)}")
            stdscr.refresh()
            time.sleep(2)
        stdscr.clear()
        return

    multiplayer = mode in ('2', '3')
    
    char_select = SimpleCharacterSelect(stdscr)
    selected_char = char_select.run()
    if not selected_char:
        stdscr.clear()
        return
    
    stdscr.clear()
    stdscr.refresh()
    time.sleep(0.1)

    entities = []
    projectiles = []
    particles = []
    power_ups = [] if not multiplayer else []
    messages = []
    combo_messages = []
    
    def push_msg(txt, ttl=2.0, color=0):
        messages.append([ttl, txt, color])

    def push_combo_msg(txt, x, y, ttl=1.0):
        combo_messages.append([ttl, txt, x, y])

    def get_deterministic_spawn_position(player_index, total_players):
        spacing = (max_x - 10) / max(1, total_players - 1)
        x = 5 + (player_index * spacing)
        y = ground_row - 0.5  # Match physics ground level
        return x, y

    net = None
    remote_entities = {}
    remote_by_id = {}
    client_id = None

    if multiplayer:
        stdscr.nodelay(False)
        host = prompt_text(stdscr, 12, 4, "Server host", "127.0.0.1")
        try:
            port = int(prompt_text(stdscr, 13, 4, "Server port", "8765"))
        except ValueError:
            port = 8765
        room = prompt_text(stdscr, 14, 4, "Room", "lobby")
        name = prompt_text(stdscr, 15, 4, "Name", "Player")
        stdscr.nodelay(True)
        stdscr.erase()
        stdscr.addstr(10, 4, f"Connecting to {host}:{port}...")
        stdscr.refresh()
        net = NetClient(host, port)
        try:
            net.connect()
            char_data = get_character(selected_char)
            char_emoji = get_character_char(selected_char, use_ascii=False)
            net.join(room, name, char_emoji)
            
            lobby = LobbyScreen(stdscr, net)
            if not lobby.run():
                return
                
            lobby_players = net.lobby_state.get("players", [])
            push_msg(f"Starting battle with {len(lobby_players)} players!", ttl=3.0)
            
            sorted_players = sorted(lobby_players, key=lambda p: p.get("id", ""))
            
            for i, info in enumerate(sorted_players):
                rid = info.get("id")
                if rid != net.client_id:
                    x, y = get_deterministic_spawn_position(i, len(sorted_players))
                    e = Entity(x, y, info.get("ch") or '🙂', name=info.get("name") or "Remote", ai=False, character_id=None)
                    remote_entities[rid] = e
                    remote_by_id[e] = rid
                    entities.append(e)
                    push_msg(f"{e.name} joined the battle!", ttl=2.0)
                
        except Exception as e:
            stdscr.addstr(12, 4, f"Connect failed: {e}")
            stdscr.refresh()
            time.sleep(2)
            return

    char_data = get_character(selected_char)
    char_emoji = get_character_char(selected_char, use_ascii=False)
    player = Entity(4, ground_row - 0.5, char_emoji, name=char_data.name, ai=False, character_id=selected_char)
    player.was_alive = True
    entities.append(player)
    
    if not multiplayer:
        ai_entities = create_ai_entities(max_x, ground_row, count=2)
        entities.extend(ai_entities)

    last = time.time()
    game_time = 0.0
    state_timer = 0.0

    push_msg("🔥 IMMORTAL COOL PRO BATTLE ROYALE 🔥", ttl=4.0, color=curses.COLOR_RED)
    push_msg("Controls: A/D move, W jump, S attack, F special, Q quit", ttl=3.0)

    running = True
    while running:
        t0 = time.time()
        elapsed = t0 - last
        last = t0
        game_time += elapsed
        state_timer += elapsed

        ch = stdscr.getch()
        keys = {}
        while ch != -1:
            keys[ch] = True
            ch = stdscr.getch()

        if KEY_QUIT in keys:
            break

        if not multiplayer:
            game_logic.spawn_power_ups(power_ups, elapsed)

        did_attack, attack_dir = game_logic.handle_player_input(player, keys, projectiles, combo_messages)

        if not multiplayer:
            for entity in entities:
                ai_controller.update_ai_entity(entity, entities, projectiles, messages, elapsed)

        if multiplayer and net:
            try:
                while True:
                    msg = net.inbox.get_nowait()
                    mtype = msg.get("type")
                    if mtype == "welcome":
                        client_id = msg.get("id")
                        players = msg.get("players", [])
                        sorted_players = sorted(players, key=lambda p: p.get("id", ""))
                        
                        for i, info in enumerate(sorted_players):
                            rid = info.get("id")
                            if rid in remote_entities:
                                continue
                            x, y = get_deterministic_spawn_position(i, len(sorted_players) + 1)  # +1 for self
                            e = Entity(x, y, info.get("ch") or '🙂', name=info.get("name") or "Remote", ai=False, character_id=None)
                            remote_entities[rid] = e
                            remote_by_id[e] = rid
                            entities.append(e)
                        push_msg(f"Joined room {msg.get('room')}", ttl=2.0)
                    elif mtype == "player_joined":
                        rid = msg.get("id")
                        if rid and rid not in remote_entities:
                            total_players = len(remote_entities) + 2  # +2 for self and new player
                            player_index = len(remote_entities) + 1  # +1 because we are 0-indexed
                            x, y = get_deterministic_spawn_position(player_index, total_players)
                            e = Entity(x, y, msg.get("ch") or '🙂', name=msg.get("name") or "Remote", ai=False, character_id=None)
                            remote_entities[rid] = e
                            remote_by_id[e] = rid
                            entities.append(e)
                            push_msg(f"{e.name} joined", ttl=1.5)
                    elif mtype == "player_left":
                        rid = msg.get("id")
                        e = remote_entities.pop(rid, None)
                        if e and e in entities:
                            entities.remove(e)
                            remote_by_id.pop(e, None)
                    elif mtype == "lobby_state":
                        players = msg.get("players", [])
                        sorted_players = sorted(players, key=lambda p: p.get("id", ""))
                        
                        for i, info in enumerate(sorted_players):
                            rid = info.get("id")
                            if rid != client_id and rid not in remote_entities:
                                x, y = get_deterministic_spawn_position(i, len(sorted_players))
                                e = Entity(x, y, info.get("ch") or '🙂', name=info.get("name") or "Remote", ai=False, character_id=None)
                                remote_entities[rid] = e
                                remote_by_id[e] = rid
                                entities.append(e)
                    elif mtype == "state":
                        rid = msg.get("id")
                        if rid == client_id:
                            continue
                        e = remote_entities.get(rid)
                        if e:
                            e.x = float(msg.get("x", e.x))
                            e.y = float(msg.get("y", e.y))
                            e.hp = int(msg.get("hp", e.hp))
                    elif mtype == "attack":
                        rid = msg.get("id")
                        e = remote_entities.get(rid)
                        if e:
                            dir = int(msg.get("dir", 1) or 1)
                            atk_speed = 25.0
                            pvx = atk_speed * dir
                            proj = Projectile(e.x + dir*1.1, e.y-0.5, pvx, 0, '⚡', e, 20)
                            projectiles.append(proj)
                    elif mtype == "respawn":
                        rid = msg.get("id")
                        e = remote_entities.get(rid)
                        if e:
                            x = float(msg.get("x", e.x))
                            y = float(msg.get("y", e.y))
                            e.respawn(x, y)
                            push_msg(f"{e.name} respawned!", ttl=2.0)
                            push_msg(f"Remote respawn at ({x:.1f}, {y:.1f})", ttl=1.0)
            except queue.Empty:
                pass
            except Exception:
                pass

        skip_set = set(remote_entities.values()) if multiplayer else set()
        game_logic.update_entities(entities, elapsed, skip=skip_set)
        
        if multiplayer:
            for e in remote_entities.values():
                e.animation_frame += elapsed * 10
                if e.invulnerable:
                    e.invulnerable_timer -= elapsed
                    if e.invulnerable_timer <= 0:
                        e.invulnerable = False
        game_logic.handle_entity_collisions(entities)

        def collision_filter(p, e):
            if not multiplayer:
                return True
            is_remote_owner = p.owner in remote_by_id
            is_remote_target = e in remote_by_id
            if not is_remote_owner and is_remote_target:
                return True
            if is_remote_owner and (not is_remote_target):
                return True
            return False

        game_logic.handle_projectile_collisions(projectiles, entities, particles, messages, collision_filter=collision_filter)
        game_logic.update_projectiles(projectiles, elapsed)
        game_logic.update_particles(particles, elapsed)
        game_logic.update_messages(messages, elapsed)
        game_logic.update_combo_messages(combo_messages, elapsed)

        if multiplayer and net:
            if state_timer >= 0.1:
                state_timer = 0.0
                net.send_state(player.x, player.y, player.hp)
            if did_attack:
                net.send_attack(player.x, player.y, attack_dir)
            
            if not player.was_alive and player.is_alive:
                net.send_respawn(player.x, player.y)
                push_msg("You respawned!", ttl=2.0)
                push_msg(f"Sent respawn at ({player.x:.1f}, {player.y:.1f})", ttl=1.0)
            player.was_alive = player.is_alive

        if not multiplayer:
            power_ups = game_logic.handle_power_up_collection(power_ups, entities, particles, messages)

        renderer.clear_screen()
        renderer.draw_stage(ground_row)
        if not multiplayer:
            renderer.draw_power_ups(power_ups)
        renderer.draw_particles(particles)
        renderer.draw_projectiles(projectiles)
        renderer.draw_entities(entities)
        renderer.draw_combo_messages(combo_messages)
        renderer.draw_messages(messages)
        renderer.draw_stats_panel(game_time, power_ups, particles, player)
        renderer.draw_controls()
        renderer.refresh()

        t1 = time.time()
        frame_time = t1 - t0
        to_sleep = DT - frame_time
        if to_sleep > 0:
            time.sleep(to_sleep)

    if multiplayer and net:
        try:
            net.leave()
        except Exception:
            pass
        net.close()

if __name__ == '__main__':
    curses.wrapper(main)
