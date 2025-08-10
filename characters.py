import curses

class Character:
    def __init__(self, name, emoji, ascii_char, description, stats):
        self.name = name
        self.emoji = emoji
        self.ascii_char = ascii_char
        self.description = description
        self.stats = stats


CHARACTERS = {
    'warrior': Character(
        name="Warrior",
        emoji="🗡️",
        ascii_char="W",
        description="Balanced fighter with high HP",
        stats={'hp': 120, 'speed': 1.0, 'damage': 1.0, 'special': 'charge'}
    ),
    'ninja': Character(
        name="Ninja", 
        emoji="🐲",
        ascii_char="N",
        description="Fast and agile with low HP",
        stats={'hp': 80, 'speed': 1.3, 'damage': 1.2, 'special': 'shadow_step'}
    ),
    'tank': Character(
        name="Tank",
        emoji="🛡️", 
        ascii_char="T",
        description="Slow but very durable",
        stats={'hp': 150, 'speed': 0.8, 'damage': 0.9, 'special': 'shield_bash'}
    ),
    'mage': Character(
        name="Mage",
        emoji="🔮",
        ascii_char="M",
        description="High damage but fragile",
        stats={'hp': 70, 'speed': 0.9, 'damage': 1.4, 'special': 'fireball'}
    ),
    'archer': Character(
        name="Archer",
        emoji="🏹",
        ascii_char="A",
        description="Ranged specialist",
        stats={'hp': 90, 'speed': 1.1, 'damage': 1.1, 'special': 'multi_shot'}
    ),
    'berserker': Character(
        name="Berserker",
        emoji="😈",
        ascii_char="B",
        description="High damage when low HP",
        stats={'hp': 100, 'speed': 1.0, 'damage': 1.0, 'special': 'rage_mode'}
    ),
    'monk': Character(
        name="Monk",
        emoji="☯️",
        ascii_char="K",
        description="Balanced with healing ability",
        stats={'hp': 110, 'speed': 1.0, 'damage': 1.0, 'special': 'heal'}
    ),
    'robot': Character(
        name="Robot",
        emoji="🤖",
        ascii_char="R",
        description="Mechanical precision",
        stats={'hp': 95, 'speed': 1.0, 'damage': 1.1, 'special': 'laser_beam'}
    )
}

def get_character_list():
    return list(CHARACTERS.keys())

def get_character(char_id):
    """Get character by ID"""
    return CHARACTERS.get(char_id)

def get_character_display_name(char_id, use_ascii=False):
    """Get character display name with emoji or ASCII"""
    char = get_character(char_id)
    if char:
        if use_ascii:
            return f"{char.ascii_char} {char.name}"
        else:
            return f"{char.emoji} {char.name}"
    return "Unknown"

def get_character_stats(char_id):
    char = get_character(char_id)
    if char:
        return char.stats.copy()
    return {'hp': 100, 'speed': 1.0, 'damage': 1.0, 'special': 'none'}

def get_character_char(char_id, use_ascii=False):
    char = get_character(char_id)
    if char:
        return char.ascii_char if use_ascii else char.emoji
    return "?" if use_ascii else "🙂"
