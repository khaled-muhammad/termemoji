import curses
import time
import random
import math

from utils import (
    FPS, DT, KEY_LEFT, KEY_RIGHT, KEY_JUMP, KEY_ATTACK, 
    KEY_SPECIAL, KEY_QUIT, setup_colors, get_random_position
)
from models import Entity, Projectile, PowerUp, Particle
from ai import AIController, create_ai_entities
from renderer import Renderer
from game_logic import GameLogic

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)
    max_y, max_x = stdscr.getmaxyx()

    ground_row = max_y - 6

    renderer = Renderer(stdscr)
    game_logic = GameLogic(max_x, max_y, ground_row)
    ai_controller = AIController()

    entities = []
    
    player = Entity(4, ground_row - 1, '😎', name="You", ai=False)
    entities.append(player)
    
    ai_entities = create_ai_entities(max_x, ground_row, count=2)
    entities.extend(ai_entities)

    projectiles = []
    particles = []
    power_ups = []
    messages = []
    combo_messages = []

    last = time.time()
    game_time = 0.0

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

        ch = stdscr.getch()
        keys = {}
        while ch != -1:
            keys[ch] = True
            ch = stdscr.getch()

        if KEY_QUIT in keys:
            break

        game_logic.spawn_power_ups(power_ups, elapsed)

        game_logic.handle_player_input(player, keys, projectiles, combo_messages)

        for entity in entities:
            ai_controller.update_ai_entity(entity, entities, projectiles, messages, elapsed)

        game_logic.update_entities(entities, elapsed)
        game_logic.handle_entity_collisions(entities)
        game_logic.handle_projectile_collisions(projectiles, entities, particles, messages)
        game_logic.update_projectiles(projectiles, elapsed)
        game_logic.update_particles(particles, elapsed)
        game_logic.update_messages(messages, elapsed)
        game_logic.update_combo_messages(combo_messages, elapsed)

        power_ups = game_logic.handle_power_up_collection(power_ups, entities, particles, messages)

        renderer.clear_screen()
        renderer.draw_stage(ground_row)
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

if __name__ == '__main__':
    curses.wrapper(main)
