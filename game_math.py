def add_xp(current_xp, points_to_add):
    """Add XP when a focus session is completed."""
    new_xp = current_xp + points_to_add
    return new_xp

def subtract_hp(current_hp, damage):
    """Subtract HP when Give Up is clicked. HP cannot go below 0."""
    new_hp = max(0, current_hp - damage)
    return new_hp

def get_level(current_xp):
    """Return the level based on XP. Every 100 XP = 1 level."""
    return current_xp // 100

def is_alive(current_hp):
    """Return True if the pet still has HP remaining."""
    return current_hp > 0

# --- quick test (run this file directly to check your logic) ---
if __name__ == "__main__":
    print(add_xp(0, 20)) # expect: 20
    print(subtract_hp(100, 10)) # expect: 90
    print(subtract_hp(5, 10)) # expect: 0
    print(get_level(250)) # expect: 2
    print(is_alive(0)) # expect: False