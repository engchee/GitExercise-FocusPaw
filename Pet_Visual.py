import os
from PIL import Image, ImageTk

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

def get_pet_image(pet_type, state):
    """
    Loads and resizes the requested pet image.
    - pet_type: "Cat", "Dog", or "Ebee"
    - state: "default", "studying", "crying", or "resting"
    """
    # 1. Map the pet and state to the exact file names
    file_names = {
        "Cat": {"default": "cat.jpeg", "studying": "cat_studying.jpeg", "crying": "cat_crying.jpeg", "resting": "cat_resting.jpeg"},
        "Dog": {"default": "puppy.jpeg", "studying": "dog_studying.jpeg", "crying": "dog_crying.jpeg", "resting": "dog_resting.jpeg"},
        "Ebee": {"default": "ebee.jpeg", "studying": "ebee_studying.jpeg", "crying": "ebee_crying.jpeg", "resting": "ebee_resting.jpeg"}
    }

    # Safety check: If the pet or state doesn't exist, stop to prevent a crash.
    if pet_type not in file_names or state not in file_names[pet_type]:
        print(f"Error: Could not find {pet_type} in {state} state.")
        return None

    # 2. Build the exact path to the file
    file_name = file_names[pet_type][state]
    img_path = os.path.join(script_dir, file_name)

    # 3. Open, resize, and convert for Tkinter
    try:
        original_img = Image.open(img_path)
        resized_img = original_img.resize((150, 150), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized_img)
    except Exception as e:
        print(f"Error loading image {file_name}: {e}")
        return None

def get_background_image(app_width, app_height):
    """
    Loads and resizes the standard background image to perfectly fit the master window.
    """
    try:
        bg_path = os.path.join(script_dir, "background.jpeg")
        original_img = Image.open(bg_path)
        resized_img = original_img.resize((app_width, app_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized_img)
    except Exception as e:
        print(f"Error loading background image: {e}")
        return None 

def get_dark_background_image(app_width, app_height):
    """
    Loads and resizes the dark mode background image.
    """
    try:
        bg_path = os.path.join(script_dir, "background (dark mode).png")
        original_img = Image.open(bg_path)
        resized_img = original_img.resize((app_width, app_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized_img)
    except Exception as e:
        print(f"Error loading dark background image: {e}")
        return None