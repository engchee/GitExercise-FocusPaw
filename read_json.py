import json

# Open and read JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Print full data
print("Full Data:")
print(data)

# Print nicely
print("\n--- Pet Status ---")
print(f"Name      : {data['pet_name']}")
print(f"Hunger    : {data['hunger']}")
print(f"Energy    : {data['energy']}")
print(f"Happiness : {data['happiness']}")