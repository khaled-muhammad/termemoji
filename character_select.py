import curses
import time
from characters import get_character_list, get_character, get_character_display_name, get_character_stats

class CharacterSelectScreen:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.selected_index = 0
        self.characters = get_character_list()
        
    def run(self):
        self.stdscr.clear()
        self.stdscr.nodelay(True)
        
        while True:
            try:
                self._draw_screen()
                ch = self.stdscr.getch()
                
                if ch == ord('q') or ch == ord('Q'):
                    return None
                elif ch == ord('\n') or ch == ord(' '):
                    return self.characters[self.selected_index]
                elif ch == curses.KEY_LEFT or ch == ord('a') or ch == ord('A'):
                    self.selected_index = (self.selected_index - 1) % len(self.characters)
                elif ch == curses.KEY_RIGHT or ch == ord('d') or ch == ord('D'):
                    self.selected_index = (self.selected_index + 1) % len(self.characters)
                elif ch == curses.KEY_UP or ch == ord('w') or ch == ord('W'):
                    self.selected_index = (self.selected_index - 2) % len(self.characters)
                elif ch == curses.KEY_DOWN or ch == ord('s') or ch == ord('S'):
                    self.selected_index = (self.selected_index + 2) % len(self.characters)
                    
            except curses.error:
                continue
                
    def _draw_screen(self):
        try:
            self.stdscr.clear()
            max_y, max_x = self.stdscr.getmaxyx()
            
            title = "CHOOSE YOUR CHARACTER"
            if max_x > len(title):
                self.stdscr.addstr(1, (max_x - len(title)) // 2, title, curses.A_BOLD)
            
            instructions = "Use A/D or Arrow Keys to navigate, ENTER to select, Q to cancel"
            if max_x > len(instructions):
                self.stdscr.addstr(3, (max_x - len(instructions)) // 2, instructions)
            
            start_y = 6
            chars_per_row = 2
            
            for i, char_id in enumerate(self.characters):
                row = i // chars_per_row
                col = i % chars_per_row
                y = start_y + row * 3
                x = (max_x // chars_per_row) * col + 2
                
                if y >= max_y - 8 or x >= max_x - 20:
                    continue
                
                if i == self.selected_index:
                    self.stdscr.attron(curses.A_REVERSE)
                
                char = get_character(char_id)
                if char:
                    display_name = f"{char.emoji} {char.name}"
                    safe_name = display_name[:18]
                    self.stdscr.addstr(y, x, safe_name)
                    
                    stats = char.stats
                    hp_text = f"HP:{stats['hp']}"
                    speed_text = f"SPD:{stats['speed']:.1f}"
                    damage_text = f"DMG:{stats['damage']:.1f}"
                    
                    if y + 1 < max_y - 8:
                        self.stdscr.addstr(y + 1, x, hp_text)
                    if y + 2 < max_y - 8:
                        self.stdscr.addstr(y + 2, x, speed_text)
                
                if i == self.selected_index:
                    self.stdscr.attroff(curses.A_REVERSE)
            
            if self.selected_index < len(self.characters):
                selected_char_id = self.characters[self.selected_index]
                selected_char = get_character(selected_char_id)
                
                if selected_char and max_y > 20:
                    details_y = max_y - 12
                    if details_y > start_y + 8:
                        self.stdscr.addstr(details_y, 2, "Selected:", curses.A_BOLD)
                        self.stdscr.addstr(details_y + 1, 4, f"Name: {selected_char.name}")
                        self.stdscr.addstr(details_y + 2, 4, f"HP: {selected_char.stats['hp']}")
                        self.stdscr.addstr(details_y + 3, 4, f"Speed: {selected_char.stats['speed']:.1f}x")
                        self.stdscr.addstr(details_y + 4, 4, f"Damage: {selected_char.stats['damage']:.1f}x")
                        self.stdscr.addstr(details_y + 5, 4, f"Special: {selected_char.stats['special']}")
            
            controls_y = max_y - 3
            if controls_y > 0:
                controls = "A/D - Navigate | ENTER - Select | Q - Cancel"
                if max_x > len(controls):
                    self.stdscr.addstr(controls_y, 2, controls)
            
            self.stdscr.refresh()
            
        except curses.error:
            pass
