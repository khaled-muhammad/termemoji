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
    stdscr.erase()
    stdscr.addstr(2, 4, "TermEmoji")
    stdscr.addstr(4, 4, "1) Singleplayer")
    stdscr.addstr(5, 4, "2) Multiplayer: Join Room")
    stdscr.addstr(6, 4, "3) Multiplayer: Create Room")
    stdscr.addstr(8, 4, "Q) Quit")
    stdscr.refresh()
    while True:
        ch = stdscr.getch()
        if ch in (ord('1'), ord('2'), ord('3'), ord('q'), ord('Q')):
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

    multiplayer = mode in ('2', '3')

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
            net.join(room, name, '😎')
        except Exception as e:
            stdscr.addstr(12, 4, f"Connect failed: {e}")
            stdscr.refresh()
            time.sleep(2)
            return

    entities = []
    
    player = Entity(4, ground_row - 1, '😎', name="You", ai=False)
    entities.append(player)
    
    if not multiplayer:
        ai_entities = create_ai_entities(max_x, ground_row, count=2)
        entities.extend(ai_entities)

    projectiles = []
    particles = []
    power_ups = [] if not multiplayer else []
    messages = []
    combo_messages = []

    last = time.time()
    game_time = 0.0
    state_timer = 0.0

    def push_msg(txt, ttl=2.0, color=0):
        messages.append([ttl, txt, color])

    def push_combo_msg(txt, x, y, ttl=1.0):
        combo_messages.append([ttl, txt, x, y])

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
                        for info in msg.get("players", []):
                            rid = info.get("id")
                            if rid in remote_entities:
                                continue
                            e = Entity(random.randint(10, max_x-6), ground_row - 1, info.get("ch") or '🙂', name=info.get("name") or "Remote", ai=False)
                            remote_entities[rid] = e
                            remote_by_id[e] = rid
                            entities.append(e)
                        push_msg(f"Joined room {msg.get('room')}", ttl=2.0)
                    elif mtype == "player_joined":
                        rid = msg.get("id")
                        if rid and rid not in remote_entities:
                            e = Entity(random.randint(10, max_x-6), ground_row - 1, msg.get("ch") or '🙂', name=msg.get("name") or "Remote", ai=False)
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
            except queue.Empty:
                pass
            except Exception:
                pass

        skip_set = set(remote_entities.values()) if multiplayer else set()
        game_logic.update_entities(entities, elapsed, skip=skip_set)
        game_logic.handle_entity_collisions(entities)

        def collision_filter(p, e):
            if not multiplayer:
                return True
            is_remote_owner = p.owner in remote_by_id
            is_remote_target = e in remote_by_id
            # Local projectiles only affect remote targets; remote projectiles only affect local
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
