import curses
from characters import get_character_list, get_character, get_character_display_name

class SimpleCharacterSelect:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.selected_index = 0
        self.characters = get_character_list()
        
    def run(self):
        self.stdscr.clear()
        self.stdscr.nodelay(False)
        
        while True:
            self._draw_screen()
            ch = self.stdscr.getch()
            
            if ch == ord('q') or ch == ord('Q'):
                self.stdscr.clear()
                self.stdscr.refresh()
                return None
            elif ch == ord('\n') or ch == ord(' '):
                self.stdscr.clear()
                self.stdscr.refresh()
                return self.characters[self.selected_index]
            elif ch == ord('a') or ch == ord('A') or ch == curses.KEY_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.characters)
            elif ch == ord('d') or ch == ord('D') or ch == curses.KEY_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.characters)
                
    def _draw_screen(self):
        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()
        
        title = "CHOOSE YOUR CHARACTER"
        x = max(0, (max_x - len(title)) // 2)
        self.stdscr.addstr(1, x, title, curses.A_BOLD)
        
        instructions = "A/D to navigate, ENTER to select, Q to cancel"
        x = max(0, (max_x - len(instructions)) // 2)
        self.stdscr.addstr(3, x, instructions)
        
        start_y = 6
        for i, char_id in enumerate(self.characters):
            y = start_y + i
            if y >= max_y - 5:
                break
                
            char = get_character(char_id)
            if not char:
                continue
                
            if i == self.selected_index:
                self.stdscr.attron(curses.A_REVERSE)
            
            try:
                display_name = get_character_display_name(char_id, use_ascii=False)
                line = f"{display_name} - HP:{char.stats['hp']} SPD:{char.stats['speed']:.1f} DMG:{char.stats['damage']:.1f}"
            except:
                display_name = get_character_display_name(char_id, use_ascii=True)
                line = f"{display_name} - HP:{char.stats['hp']} SPD:{char.stats['speed']:.1f} DMG:{char.stats['damage']:.1f}"
            
            if len(line) > max_x - 2:
                line = line[:max_x - 5] + "..."
            
            self.stdscr.addstr(y, 2, line)
            
            if i == self.selected_index:
                self.stdscr.attroff(curses.A_REVERSE)
        
        if self.selected_index < len(self.characters):
            selected_char = get_character(self.characters[self.selected_index])
            if selected_char and max_y > 15:
                details_y = max_y - 8
                self.stdscr.addstr(details_y, 2, "Selected Character:", curses.A_BOLD)
                self.stdscr.addstr(details_y + 1, 4, f"Name: {selected_char.name}")
                self.stdscr.addstr(details_y + 2, 4, f"Description: {selected_char.description}")
                self.stdscr.addstr(details_y + 3, 4, f"Special: {selected_char.stats['special']}")
        
        self.stdscr.refresh()
