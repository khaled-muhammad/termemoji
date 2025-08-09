import curses
from utils import POWERUP_TYPES, setup_colors

class Renderer:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.max_y, self.max_x = stdscr.getmaxyx()
        setup_colors()
        
    def clear_screen(self):
        self.stdscr.erase()
        
    def draw_stage(self, ground_row):
        for cx in range(self.max_x):
            self.stdscr.addstr(ground_row, cx, '═')
        self.stdscr.addstr(ground_row+1, 0, " "*(self.max_x-1))
        
    def draw_power_ups(self, power_ups):
        for power_up in power_ups:
            sx = int(round(power_up.x))
            sy = int(round(power_up.y))
            if 0 <= sy < self.max_y and 0 <= sx < self.max_x:
                try:
                    emoji = POWERUP_TYPES[power_up.power_type]['emoji']
                    self.stdscr.addstr(int(sy), int(sx), emoji)
                except curses.error:
                    pass
                    
    def draw_particles(self, particles):
        for particle in particles:
            sx = int(round(particle.x))
            sy = int(round(particle.y))
            if 0 <= sy < self.max_y and 0 <= sx < self.max_x:
                try:
                    self.stdscr.addstr(int(sy), int(sx), particle.ch)
                except curses.error:
                    pass
                    
    def draw_projectiles(self, projectiles):
        for p in projectiles:
            for trail_x, trail_y in p.trail_positions:
                sx = int(round(trail_x))
                sy = int(round(trail_y))
                if 0 <= sy < self.max_y and 0 <= sx < self.max_x:
                    try:
                        self.stdscr.addstr(int(sy), int(sx), '·')
                    except curses.error:
                        pass
                        
            sx = int(round(p.x))
            sy = int(round(p.y))
            if 0 <= sy < self.max_y and 0 <= sx < self.max_x:
                try:
                    self.stdscr.addstr(int(sy), int(sx), p.ch)
                except curses.error:
                    pass
                    
    def draw_entities(self, entities):
        for e in entities:
            if not e.is_alive:
                continue
                
            sx = int(round(e.x))
            sy = int(round(e.y))
            if 0 <= sy < self.max_y and 0 <= sx < self.max_x:
                cell = e.ch
                
                if e.special_effect_timer > 0:
                    cell = '🌟'
                elif e.invulnerable:
                    cell = '✨' if int(e.animation_frame) % 2 == 0 else e.ch
                elif e.has_shield():
                    cell = '🛡️'
                elif e.is_infinite_mode():
                    cell = '♾️'
                    
                try:
                    self.stdscr.addstr(int(sy), int(sx), cell)
                except curses.error:
                    pass
                    
            self._draw_entity_hud(e, sx, sy)
            
    def _draw_entity_hud(self, entity, sx, sy):
        if 0 <= sy-1 < self.max_y and 0 <= sx < self.max_x:
            hp_percent = max(0, int((entity.hp / entity.max_hp) * 10))
            hp_bar = '█' * hp_percent + '░' * (10 - hp_percent)
            name_display = f"{entity.name}:{max(0,int(entity.hp))}"
            try:
                self.stdscr.addstr(max(0,sy-1), min(self.max_x-1, sx - len(name_display)//2), name_display)
                if 0 <= sy-2 < self.max_y:
                    self.stdscr.addstr(max(0,sy-2), min(self.max_x-1, sx - 5), hp_bar)
            except curses.error:
                pass
                
    def draw_combo_messages(self, combo_messages):
        for ttl, txt, x, y in combo_messages:
            sx = int(round(x))
            sy = int(round(y))
            if 0 <= sy < self.max_y and 0 <= sx < self.max_x:
                try:
                    self.stdscr.addstr(int(sy), int(sx), txt)
                except curses.error:
                    pass
                    
    def draw_messages(self, messages):
        y = 1
        for i, m in enumerate(messages[:8]):
            ttl, txt, color = m
            try:
                if color > 0:
                    self.stdscr.addstr(y+i, 2, txt[:self.max_x-4], curses.color_pair(color))
                else:
                    self.stdscr.addstr(y+i, 2, txt[:self.max_x-4])
            except curses.error:
                pass
                
    def draw_stats_panel(self, game_time, power_ups, particles, player):
        stats_y = self.max_y - 4
        self.stdscr.addstr(stats_y, 2, f"Time: {int(game_time)}s | Power-ups: {len(power_ups)} | Particles: {len(particles)}")
        
        if player.is_alive:
            self.stdscr.addstr(stats_y + 1, 2, f"Kills: {player.kills} | Deaths: {player.deaths} | Combo: {player.combo_count}")
            
    def draw_controls(self):
        self.stdscr.addstr(self.max_y-2, 2, "Controls: A/D move, W jump, S attack, F special, Q quit")
        self.stdscr.addstr(self.max_y-1, 2, "Power-ups: ❤️ Health ⚡ Speed 💥 Damage 🛡️ Shield ♾️ Infinite")
        
    def refresh(self):
        self.stdscr.refresh()
