import random
import math
from utils import GRAVITY, POWERUP_TYPES, create_explosion_particles, get_random_position
from models import Entity, Projectile, PowerUp, Particle

class GameLogic:
    def __init__(self, max_x, max_y, ground_row):
        self.max_x = max_x
        self.max_y = max_y
        self.ground_row = ground_row
        self.power_up_spawn_timer = 0.0
        
    def handle_player_input(self, player, keys, projectiles, combo_messages):
        if not player.is_alive:
            return False, 0
            
        base_speed = 20.0
        speed = base_speed * player.get_speed_multiplier()
        jump_speed = -20.0
        atk_speed = 25.0
        did_attack = False
        attack_dir = 0
        
        if keys.get(ord('a')):
            player.vx = -speed
            player.facing_dir = -1
        elif keys.get(ord('d')):
            player.vx = speed
            player.facing_dir = 1
        else:
            player.vx = 0
            
        if keys.get(ord('w')) and player.on_ground:
            player.vy = jump_speed
            player.on_ground = False
            
        if keys.get(ord('s')) and player.cooldown <= 0:
            dir = player.facing_dir
            pvx = atk_speed * dir
            damage = 20 * player.get_damage_multiplier()
            projectile = Projectile(player.x + dir*1.1, player.y-0.5, pvx, 0, '🔸', player, damage)
            projectiles.append(projectile)
            player.cooldown = 0.6
            did_attack = True
            attack_dir = dir
            
            player.combo_count += 1
            player.combo_timer = 1.0
            if player.combo_count >= 3:
                combo_messages.append([1.0, f"COMBO x{player.combo_count}!", player.x, player.y - 2])
                
        if keys.get(ord('f')) and player.special_cooldown <= 0:
            self._handle_special_ability(player, projectiles, atk_speed)
            
        return did_attack, attack_dir
    
    def _handle_special_ability(self, player, projectiles, atk_speed):
        for angle in range(-30, 31, 15):
            rad = math.radians(angle)
            dir_x = math.cos(rad)
            dir_y = math.sin(rad)
            pvx = atk_speed * dir_x
            pvy = atk_speed * dir_y
            damage = 30 * player.get_damage_multiplier()
            projectile = Projectile(player.x, player.y-0.5, pvx, pvy, '⚡', player, damage, special=True)
            projectiles.append(projectile)
        player.special_cooldown = 3.0
        player.special_effect_timer = 0.5
        
    def spawn_power_ups(self, power_ups, dt):
        self.power_up_spawn_timer += dt
        if self.power_up_spawn_timer > 8.0 and len(power_ups) < 3:
            power_type = random.choice(list(POWERUP_TYPES.keys()))
            x = random.randint(5, self.max_x - 6)
            power_ups.append(PowerUp(x, self.ground_row - 2, power_type))
            self.power_up_spawn_timer = 0.0
            
    def handle_power_up_collection(self, power_ups, entities, particles, messages):
        for power_up in power_ups[:]:
            if power_up.collected:
                continue
                
            for e in entities:
                if not e.is_alive:
                    continue
                    
                if abs(e.x - power_up.x) < 1.0 and abs(e.y - power_up.y) < 1.0:
                    message = power_up.collect(e)
                    if message:
                        color_map = {
                            'HEALTH': 2,
                            'SPEED': 3,
                            'DAMAGE': 5,
                            'SHIELD': 4,
                            'INFINITE': 6
                        }
                        color = 0
                        for key, color_code in color_map.items():
                            if key in message:
                                color = color_code
                                break
                        messages.append([1.5, message, color])
                        
                    particles.extend(create_explosion_particles(power_up.x, power_up.y, 5))
                    break
                    
            power_up.update(0.016)
            
        return [p for p in power_ups if not p.collected]
        
    def handle_entity_collisions(self, entities):
        for i in range(len(entities)):
            a = entities[i]
            if not a.is_alive: 
                continue
            for j in range(i+1, len(entities)):
                b = entities[j]
                if not b.is_alive: 
                    continue
                
                dx = b.x - a.x
                dy = b.y - a.y
                d = math.hypot(dx, dy)
                if d < 1.0 and d > 0.001:
                    overlap = 1.0 - d
                    nx = dx / d
                    ny = dy / d
                    a.x -= nx * overlap * 0.5
                    a.y -= ny * overlap * 0.5
                    b.x += nx * overlap * 0.5
                    b.y += ny * overlap * 0.5
                    
                    ax, ay = a.vx, a.vy
                    bx, by = b.vx, b.vy
                    a.vx = ax*0.5 + bx*0.5
                    b.vx = bx*0.5 + ax*0.5
                    
    def handle_projectile_collisions(self, projectiles, entities, particles, messages, collision_filter=None):
        for p in projectiles[:]:
            for e in entities:
                if not e.is_alive or e.invulnerable: 
                    continue
                if e is p.owner: 
                    continue
                if collision_filter is not None and not collision_filter(p, e):
                    continue
                
                if abs(e.x - p.x) < 1.0 and abs(e.y - p.y) < 1.0:
                    damage = p.damage
                    
                    if e.has_shield():
                        damage = max(5, damage // 2)
                        messages.append([1.0, f"{e.name}'s shield absorbed damage!", 4])
                        
                    e.hp -= damage
                    
                    nx = (e.x - p.owner.x)
                    if nx == 0: 
                        nx = 1 if random.random() < 0.5 else -1
                    nk = 8.0 * (1 if nx > 0 else -1)
                    e.vx += nk
                    e.vy -= 6
                    
                    if p.owner.combo_timer > 0:
                        p.owner.combo_count += 1
                    else:
                        p.owner.combo_count = 1
                    p.owner.combo_timer = 1.0
                    
                    messages.append([1.6, f"{p.owner.name} hit {e.name} for {damage}!", 0])
                    
                    particles.extend(create_explosion_particles(e.x, e.y, 3))
                    
                    if e.hp <= 0:
                        if e.is_infinite_mode():
                            e.hp = 1
                            messages.append([2.0, f"{e.name} is IMMORTAL!", 6])
                        else:
                            e.is_alive = False
                            e.respawn_timer = 3.0
                            e.deaths += 1
                            p.owner.kills += 1
                            messages.append([2.0, f"{e.name} was defeated! (Respawn in 3s)", 1])
                            
                    try:
                        projectiles.remove(p)
                    except ValueError:
                        pass
                    break
                    
    def update_projectiles(self, projectiles, dt):
        for p in projectiles[:]:
            if p.update_physics(dt, self.max_x, self.max_y):
                if p in projectiles:
                    projectiles.remove(p)
                    
    def update_particles(self, particles, dt):
        for particle in particles[:]:
            if particle.update(dt):
                particles.remove(particle)
                
    def update_entities(self, entities, dt, skip=None):
        if skip is None:
            skip = set()
        for e in entities:
            if e in skip:
                continue
            if not e.is_alive:
                e.respawn_timer -= dt
                if e.respawn_timer <= 0:
                    x, y = get_random_position(self.max_x, self.ground_row)
                    e.respawn(x, y)
                continue
                
            e.update_physics(dt, self.ground_row, self.max_x)
            
    def update_messages(self, messages, dt):
        for m in messages[:]:
            m[0] -= dt
            if m[0] <= 0:
                messages.remove(m)
                
    def update_combo_messages(self, combo_messages, dt):
        for combo_msg in combo_messages[:]:
            combo_msg[0] -= dt
            if combo_msg[0] <= 0:
                combo_messages.remove(combo_msg)
