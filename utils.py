import curses
import math
import random

FPS = 30
DT = 1.0 / FPS
GRAVITY = 30.0
TERMINAL_EMOJI_WIDTH = 1.0

KEY_LEFT = ord('a')
KEY_RIGHT = ord('d')
KEY_JUMP = ord('w')
KEY_ATTACK = ord('s')
KEY_SPECIAL = ord('f')
KEY_QUIT = ord('q')

POWERUP_TYPES = {
    'health': {'emoji': '❤️', 'color': curses.COLOR_RED},
    'speed': {'emoji': '⚡', 'color': curses.COLOR_YELLOW},
    'damage': {'emoji': '💥', 'color': curses.COLOR_MAGENTA},
    'shield': {'emoji': '🛡️', 'color': curses.COLOR_BLUE},
    'infinite': {'emoji': '♾️', 'color': curses.COLOR_CYAN}
}

EMOJI_CHARACTERS = ['😀','😈','👾','🤖','🐲','🦊','🐼','🐵','👻','🤡','👹','👺','💀','🤖','👽','🎃']

AI_NAMES = ["Shadow", "Thunder", "Void", "Phoenix", "Frost", "Chaos"]

PARTICLE_EMOJIS = ['✨', '💫', '⭐', '🌟']

AI_TAUNTS = ['Take this!', 'Booyah!', 'Taste defeat!', 'Feel my power!', 'You\'re finished!']

def clamp(v, a, b):
    return max(a, min(b, v))

def dist(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    return math.hypot(dx, dy)

def create_explosion_particles(x, y, count=8):
    from models import Particle
    
    particles = []
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(5, 15)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        emoji = random.choice(PARTICLE_EMOJIS)
        particles.append(Particle(x, y, vx, vy, emoji, random.uniform(0.5, 1.5)))
    return particles

def setup_colors():
    curses.start_color()
    curses.use_default_colors()
    for i in range(1, 8):
        curses.init_pair(i, i, -1)

def get_random_position(max_x, ground_row):
    return random.randint(4, max_x - 6), ground_row - 1
