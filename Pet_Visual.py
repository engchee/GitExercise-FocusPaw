import os
from PIL import Image, ImageTk

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

def get_pet_image(pet_type, state, equipped_item=None):
    #Loads the requested pet image based on its state and what it is wearing.
    # 1. Base names without the ".jpeg"
    file_names = {
        "Cat": {"default": "cat", "studying": "cat_studying", "crying": "cat_crying", "resting": "cat_resting"},
        "Dog": {"default": "dog", "studying": "dog_studying", "crying": "dog_crying", "resting": "dog_resting"},
        "Ebee": {"default": "ebee", "studying": "ebee_studying", "crying": "ebee_crying", "resting": "ebee_resting"}
    }

    if pet_type not in file_names or state not in file_names[pet_type]:
        print(f"Error: Could not find {pet_type} in {state} state.")
        return None

    # Get the base name (e.g., "dog_studying")
    base_name = file_names[pet_type][state]

    # 2. Add the item name to the end of the file string
    if equipped_item == "Top Hat":
        file_name = f"{base_name}_top hat.jpeg"
    elif equipped_item == "Glasses":
        file_name = f"{base_name}_glasses.jpeg"
    elif equipped_item == "Bowtie":
        file_name = f"{base_name}_bowtie.jpeg"
    else:
        # If they aren't wearing anything, just use the normal file
        file_name = f"{base_name}.jpeg"

    # 3. Build the exact path to the file
    img_path = os.path.join(script_dir, file_name)

    # 4. Open, resize, and convert for Tkinter
    try:
        original_img = Image.open(img_path)
        resized_img = original_img.resize((150, 150), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized_img)
    except Exception as e:
        print(f"Error loading image {file_name}: {e}")
        return None

def get_background_image(app_width, app_height):
    #Loads and resizes the standard background image.
    try:
        bg_path = os.path.join(script_dir, "background.jpeg")
        original_img = Image.open(bg_path)
        resized_img = original_img.resize((app_width, app_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized_img)
    except Exception as e:
        print(f"Error loading background image: {e}")
        return None 

def get_dark_background_image(app_width, app_height):
    #Loads and resizes the dark mode background image.
    try:
        bg_path = os.path.join(script_dir, "background (dark mode).png")
        original_img = Image.open(bg_path)
        resized_img = original_img.resize((app_width, app_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized_img)
    except Exception as e:
        print(f"Error loading dark background image: {e}")
        return None