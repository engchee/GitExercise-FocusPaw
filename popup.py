import json
import os
<<<<<<< HEAD
from datetime import date, datetime
=======
from datetime import date
>>>>>>> main

# --- FILE PATH SETUP ---
script_dir = os.path.dirname(os.path.abspath(__file__)) 

def get_file_path(userid):
    """Generates the file path based on the provided User ID."""
    if not userid:
        return None
    return os.path.join(script_dir, f"{userid}_pet.json")

<<<<<<< HEAD
# --- ACADEMIC WEEK CALCULATION ---
def get_academic_week():
    """
    Calculates the current academic week based on a semester start date.
    Adjust the start date string below to match your actual semester start.
    """
    try:
        semester_start = datetime.strptime("2026-03-02", "%Y-%m-%d").date() # Example start date
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

=======
>>>>>>> main
# --- STREAK CALCULATION LOGIC ---
def calculate_streak(saved_date_str, current_streak):
    today = date.today()
    
<<<<<<< HEAD
=======
    # If there is no date OR the current streak is 0, start it at 1
>>>>>>> main
    if not saved_date_str or current_streak == 0:
        return 1 

    last_login = date.fromisoformat(saved_date_str)
    delta = (today - last_login).days

    if delta == 1:
<<<<<<< HEAD
        return current_streak + 1  
=======
        return current_streak + 1  # Next day, increase streak
>>>>>>> main
    elif delta > 1:
        return 1                    
    else:
<<<<<<< HEAD
        return max(current_streak, 1) 

# --- PARAMETERIZED CRUD FUNCTIONS ---
def load_data(userid):
    """Loads user data, calculates updated streak, and returns stats."""
=======
        return max(current_streak, 1) # Same day, ensure it's at least 1

# --- PARAMETERIZED CRUD FUNCTIONS ---
def load_data(userid):
    """
    Loads user data by User ID, calculates the updated streak, 
    and returns the stats as a dictionary.
    """
>>>>>>> main
    path = get_file_path(userid)
    if path and os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                
<<<<<<< HEAD
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

def save_data(userid, petname, pet_type, current_xp, current_hp, streak, xp_earned_now=0):
    """Accepts variables and saves/updates the JSON file with history logs."""
=======
                # Calculate the updated streak on load
                saved_date = data.get("last_login", "")
                old_streak = data.get("streak", 0)
                new_streak = calculate_streak(saved_date, old_streak)
                
                # Update the dictionary with the correct active streak
                data["streak"] = new_streak
                
                return data # Send the dictionary back to main.py
        except Exception as e:
            print(f"Error loading data for {userid}: {e}")
            return None
            
    # Return None if the file doesn't exist yet (New User)
    return None 

def save_data(userid, petname, pet_type, current_xp, current_hp, streak):
    """
    Accepts specific variables from main.py or timer.py and overwrites the JSON file.
    """
>>>>>>> main
    if not userid:
        print("Error: Cannot save without a User ID.")
        return
    
    path = get_file_path(userid)
<<<<<<< HEAD
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
    
=======
    
    # Pack the incoming variables into a clean dictionary
>>>>>>> main
    data = {
        "user id": userid,
        "pet name": petname,
        "pet type": pet_type,
        "current_xp": current_xp,
        "current_hp": current_hp,
        "streak": streak, 
<<<<<<< HEAD
        "last_login": date.today().isoformat(),
        "history": history
=======
        "last_login": date.today().isoformat() # Automatically stamp today's date
>>>>>>> main
    }
    
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully auto-saved for {userid}!")
    except Exception as e:
<<<<<<< HEAD
        print(f"Failed to auto-save: {e}")

def delete_data(userid):
    """Permanently deletes the JSON pet file for the given user ID."""
    if not userid:
        print("Error: Cannot delete data without a User ID.")
        return False

    path = get_file_path(userid)
    
    if path and os.path.exists(path):
        try:
            os.remove(path)
            print(f"Data file for user '{userid}' has been permanently deleted.")
            return True
        except Exception as e:
            print(f"Failed to delete data file for {userid}: {e}")
            return False
    else:
        print(f"No data file found for user '{userid}'.")
        return False
=======
        print(f"Failed to auto-save: {e}")
>>>>>>> main
