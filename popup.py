import json
import os
from datetime import date, datetime

# --- FILE PATH SETUP ---
script_dir = os.path.dirname(os.path.abspath(__file__))

def get_file_path(userid):
    """Generates the file path based on the provided User ID."""
    if not userid:
        return None
    return os.path.join(script_dir, f"{userid}_pet.json")

# --- ACADEMIC WEEK CALCULATION ---
def get_academic_week():
    """Calculates the current academic week based on a semester start date."""
    try:
        semester_start = datetime.strptime("2026-03-30", "%Y-%m-%d").date() 
        today = date.today()
        
        if today < semester_start:
            return "Pre-Sem"
            
        days_diff = (today - semester_start).days
        week_number = (days_diff // 7) + 1
        
        if week_number > 14:  # Adjust max weeks if needed
            return "Post-Sem"
        return f"Week {week_number}"
    except Exception:
        return "Week 1"

# --- STREAK CALCULATION LOGIC ---
def calculate_streak(saved_date_str, current_streak):
    today = date.today()
    
    if not saved_date_str or current_streak == 0:
        return 1

    last_login = date.fromisoformat(saved_date_str)
    delta = (today - last_login).days

    if delta == 1:
        return current_streak + 1 
    elif delta > 1:
        return 1                  
    else:
        return max(current_streak, 1)

# --- PARAMETERIZED CRUD FUNCTIONS ---
def load_data(userid):
    """Loads user data, calculates updated streak, and returns stats."""
    path = get_file_path(userid)
    if path and os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                
                saved_date = data.get("last_login", "")
                old_streak = data.get("streak", 0)
                new_streak = calculate_streak(saved_date, old_streak)
                
                data["streak"] = new_streak
                if "history" not in data:
                    data["history"] = {}
                    
                return data
        except Exception as e:
            print(f"Error loading data for {userid}: {e}")
            return None
    return None

def save_data(userid, petname, pet_type, current_xp, current_hp, streak, coins, owned_items, equipped_item, xp_earned_now=0):
    """Accepts variables and saves/updates the JSON file with history logs and shop items."""
    if not userid:
        print("Error: Cannot save without a User ID.")
        return
    
    # Safety check for lists
    if owned_items is None:
        owned_items = []
        
    path = get_file_path(userid)
    history = {}
    
    # Try to load existing history first so we don't overwrite old data
    if path and os.path.exists(path):
        try:
            with open(path, "r") as f:
                existing_data = json.load(f)
                history = existing_data.get("history", {})
        except Exception:
            pass

    # Log XP to current academic week if XP was earned
    if xp_earned_now > 0:
        current_week = get_academic_week()
        history[current_week] = history.get(current_week, 0) + xp_earned_now
    
    data = {
        "user id": userid,
        "pet name": petname,
        "pet type": pet_type,
        "current_xp": current_xp,
        "current_hp": current_hp,
        "streak": streak, 
        "coins": coins,
        "owned_items": owned_items,
        "equipped_item": equipped_item,
        "last_login": date.today().isoformat(),
        "history": history
    }
    
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully auto-saved for {userid}!")
    except Exception as e:
        print(f"Failed to auto-save: {e}")

# --- TASK 1 & 2: BACKEND FILE DELETION ---
def delete_data(userid):
    """Permanently deletes the JSON data file for the given User ID."""
    path = get_file_path(userid)
    if path:
        try:
            os.remove(path)
            print(f"Data for user {userid} successfully deleted.")
            return True
        except Exception as e:
            print(f"Error deleting data safely for {userid}: {e}")
            return False
    return False