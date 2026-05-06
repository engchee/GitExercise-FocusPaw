import os
import json

# Get the directory where read_json.py is located
script_dir = os.path.dirname(__file__) 
file_path = os.path.join(script_dir, 'data.json')

with open(file_path, 'r') as file:
    data = json.load(file)
print("Full Data:")
print(data)

print("\n--- Pet Profile ---")
print(f"User id           : {data['user_id']}")
print(f"Name              : {data['pet_name']}")
print(f"Experience Points : {data['current_xp']}")
print(f"Healthy Points     : {data['current_hp']}")