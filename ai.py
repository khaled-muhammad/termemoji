import random
import math
from utils import dist, AI_NAMES, AI_TAUNTS
from models import Entity, Projectile

class AIController:
    def __init__(self):
        self.attack_probability = 0.02
        self.jump_probability = 0.015
        self.special_probability = 0.01
        self.taunt_probability = 0.2

    def update_ai_entity(self, entity, entities, projectiles, messages, dt):
        if not entity.ai or not entity.is_alive:
            return
            
        entity.update_power_ups(dt)
        
        targets = [o for o in entities if o is not entity and o.is_alive]
        if not targets:
            return
            
        target = min(targets, key=lambda o: dist(entity, o))
        dx = target.x - entity.x
        
        self._handle_movement(entity, dx)
        self._handle_jumping(entity)
        self._handle_attacking(entity, dx, projectiles, messages)
        self._handle_special_ability(entity, targets, projectiles)

    def _handle_movement(self, entity, dx):
        if abs(dx) > 2:
            entity.vx = 7.0 * (1 if dx > 0 else -1) * entity.get_speed_multiplier()
        else:
            entity.vx = 0

    def _handle_jumping(self, entity):
        if random.random() < self.jump_probability and entity.on_ground:
            entity.vy = -18 - random.random() * 6
            entity.on_ground = False

    def _handle_attacking(self, entity, dx, projectiles, messages):
        if entity.cooldown <= 0 and random.random() < self.attack_probability:
            dir = 1 if dx > 0 else -1
            damage = 20 * entity.get_damage_multiplier()
            projectile = Projectile(
                entity.x + dir*1.1, 
                entity.y-0.5, 
                18.0*dir, 
                0, 
                '⚡', 
                entity, 
                damage
            )
            projectiles.append(projectile)
            entity.cooldown = 1.2
            
            if random.random() < self.taunt_probability:
                taunt = random.choice(AI_TAUNTS)
                messages.append([1.5, f"{entity.name}: {taunt}", 0])

    def _handle_special_ability(self, entity, targets, projectiles):
        if entity.special_cooldown <= 0 and random.random() < self.special_probability:
            for target in targets[:2]:
                dx = target.x - entity.x
                dy = target.y - entity.y
                dist_to_target = math.hypot(dx, dy)
                if dist_to_target > 0:
                    vx = (dx / dist_to_target) * 12
                    vy = (dy / dist_to_target) * 12
                    projectile = Projectile(
                        entity.x, 
                        entity.y-0.5, 
                        vx, 
                        vy, 
                        '🔥', 
                        entity, 
                        25, 
                        special=True
                    )
                    projectiles.append(projectile)
            entity.special_cooldown = 5.0

def create_ai_entities(max_x, ground_row, count=5):
    from utils import EMOJI_CHARACTERS, get_random_position
    
    entities = []
    for i in range(count):
        x, y = get_random_position(max_x, ground_row)
        ch = random.choice(EMOJI_CHARACTERS)
        name = random.choice(AI_NAMES)
        entity = Entity(x, y, ch, name=name, ai=True)
        entities.append(entity)
    
    return entities
