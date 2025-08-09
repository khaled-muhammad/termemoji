import math
import random
import time
from utils import GRAVITY, POWERUP_TYPES

class Entity:
    def __init__(self, x, y, ch, name="E", ai=False):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.ch = ch
        self.max_hp = 100
        self.hp = self.max_hp
        self.name = name
        self.ai = ai
        self.on_ground = False
        self.cooldown = 0.0
        self.special_cooldown = 0.0
        self.combo_count = 0
        self.combo_timer = 0.0
        self.kills = 0
        self.deaths = 0
        self.respawn_timer = 0.0
        self.is_alive = True
        self.invulnerable = False
        self.invulnerable_timer = 0.0
        self.power_ups = {
            'speed': 0.0,
            'damage': 0.0,
            'shield': 0.0,
            'infinite': 0.0
        }
        self.original_ch = ch
        self.animation_frame = 0.0
        self.trail_positions = []
        self.special_effect_timer = 0.0
        self.facing_dir = 1

    def respawn(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.hp = self.max_hp
        self.is_alive = True
        self.invulnerable = True
        self.invulnerable_timer = 2.0
        self.combo_count = 0
        self.trail_positions.clear()

    def update_power_ups(self, dt):
        for power_type in self.power_ups:
            if self.power_ups[power_type] > 0:
                self.power_ups[power_type] -= dt
                if self.power_ups[power_type] <= 0:
                    self.power_ups[power_type] = 0.0

    def get_speed_multiplier(self):
        return 1.0 + (self.power_ups['speed'] * 0.5)

    def get_damage_multiplier(self):
        return 1.0 + (self.power_ups['damage'] * 0.8)

    def has_shield(self):
        return self.power_ups['shield'] > 0

    def is_infinite_mode(self):
        return self.power_ups['infinite'] > 0

    def update_physics(self, dt, ground_row, max_x):
        self.cooldown = max(0.0, self.cooldown - dt)
        self.special_cooldown = max(0.0, self.special_cooldown - dt)
        self.special_effect_timer = max(0.0, self.special_effect_timer - dt)
        
        self.combo_timer = max(0.0, self.combo_timer - dt)
        if self.combo_timer <= 0:
            self.combo_count = 0
            
        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                
        self.animation_frame += dt * 10
        
        self.vy += GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        if self.y >= ground_row - 0.5:
            if self.vy > 0:
                self.vy = 0
            self.y = ground_row - 0.5
            self.on_ground = True
            
        if self.x < 1:
            self.x = 1
            self.vx *= -0.2
        if self.x > max_x - 2:
            self.x = max_x - 2
            self.vx *= -0.2

class Projectile:
    def __init__(self, x, y, vx, vy, ch, owner, damage=20, special=False):
        self.x = float(x)
        self.y = float(y)
        self.vx = vx
        self.vy = vy
        self.ch = ch
        self.owner = owner
        self.life = 3.0
        self.damage = damage
        self.special = special
        self.trail_positions = []

    def update(self, dt):
        self.trail_positions.append((self.x, self.y))
        if len(self.trail_positions) > 5:
            self.trail_positions.pop(0)

    def update_physics(self, dt, max_x, max_y):
        self.life -= dt
        self.vy += GRAVITY * dt * 0.1
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.update(dt)
        
        return (self.life <= 0 or self.x < 0 or self.x > max_x-1 or self.y > max_y)

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = float(x)
        self.y = float(y)
        self.power_type = power_type
        self.collected = False
        self.bob_offset = 0.0
        self.bob_speed = 3.0

    def update(self, dt):
        self.bob_offset += self.bob_speed * dt
        self.y = self.y + 0.1 * math.sin(self.bob_offset)

    def collect(self, entity):
        power_type = self.power_type
        if power_type == 'health':
            entity.hp = min(entity.max_hp, entity.hp + 50)
            return f"{entity.name} got HEALTH!"
        elif power_type == 'speed':
            entity.power_ups['speed'] = 10.0
            return f"{entity.name} got SPEED!"
        elif power_type == 'damage':
            entity.power_ups['damage'] = 8.0
            return f"{entity.name} got DAMAGE!"
        elif power_type == 'shield':
            entity.power_ups['shield'] = 5.0
            return f"{entity.name} got SHIELD!"
        elif power_type == 'infinite':
            entity.power_ups['infinite'] = 15.0
            return f"{entity.name} got INFINITE MODE!"
        
        self.collected = True
        return None

class Particle:
    def __init__(self, x, y, vx, vy, ch, life=1.0):
        self.x = float(x)
        self.y = float(y)
        self.vx = vx
        self.vy = vy
        self.ch = ch
        self.life = life
        self.max_life = life

    def update(self, dt):
        self.life -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += GRAVITY * dt * 0.5
        return self.life <= 0

