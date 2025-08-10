import curses
from simple_char_select import SimpleCharacterSelect
from characters import get_character_list, get_character, get_character_display_name

def test_char_select(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Testing Character Selection...")
    stdscr.refresh()
    
    char_select = SimpleCharacterSelect(stdscr)
    selected_char = char_select.run()
    
    if selected_char:
        char_data = get_character(selected_char)
        stdscr.clear()
        stdscr.addstr(1, 2, f"Selected: {get_character_display_name(selected_char)}")
        stdscr.addstr(2, 2, f"HP: {char_data.stats['hp']}")
        stdscr.addstr(3, 2, f"Speed: {char_data.stats['speed']:.1f}x")
        stdscr.addstr(4, 2, f"Damage: {char_data.stats['damage']:.1f}x")
        stdscr.addstr(5, 2, f"Special: {char_data.stats['special']}")
        stdscr.addstr(7, 2, "Press any key to exit...")
        stdscr.refresh()
        stdscr.getch()
    else:
        stdscr.clear()
        stdscr.addstr(1, 2, "No character selected")
        stdscr.addstr(3, 2, "Press any key to exit...")
        stdscr.refresh()
        stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(test_char_select)
