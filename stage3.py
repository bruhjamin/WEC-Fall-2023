import csv
import json
from tabulate import tabulate

items = []
combinations = []
invalid_combinations = []

with open('gear.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        items.append([row[0], row[1], row[2], row[3]])

with open('combinations.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        combinations.append([row[0], row[1], row[2], row[3], row[4]])

with open('invalidCombinations.json', 'r') as file:
    invalid_data = json.load(file)
    for gear_item in invalid_data.get('gear', []):
        gear_name = gear_item['gearName']
        exceptions = gear_item['gearExceptions']
        exceptions.append(gear_name)
        invalid_combinations.append(exceptions)

# Set the weight limit for gear
weight_limit = 9.0  # adjust this value

# Calculate the combined attributes of gear combinations
def calculate_combination_bonus(selected_gear):
    total_survival = 0
    total_combat = 0
    for gear in selected_gear:
        total_survival += int(gear[2])
        total_combat += int(gear[3])
    for combo in combinations:
        if combo[0] in selected_gear and combo[1] in selected_gear:
            total_survival += int(combo[3])
            total_combat += int(combo[4])
    return total_survival, total_combat

# Check if a combination is invalid
def is_combination_invalid(selected_gear, gear_to_add):
    for invalid_combo in invalid_combinations:
        if gear_to_add[0] in invalid_combo:
            for gear_name in [gear[0] for gear in selected_gear]:
                if gear_name in invalid_combo:
                    return True
    return False

# Greedy algorithm to select gear
selected_gear = []
current_weight = 0.0

while current_weight < weight_limit:
    best_gear = None
    best_combination_bonus = (0, 0)

    for gear in items:
        if gear not in selected_gear and current_weight + float(gear[1]) <= weight_limit:
            if not is_combination_invalid(selected_gear, gear):
                selected_gear.append(gear)
                bonus = calculate_combination_bonus(selected_gear)
                if bonus > best_combination_bonus:
                    best_combination_bonus = bonus
                    best_gear = gear
                selected_gear.remove(gear)

    if best_gear is not None:
        selected_gear.append(best_gear)
        current_weight += float(best_gear[1])
    else:
        break


print(tabulate(selected_gear, headers=["Item", "Weight", "Survival", "Combat"]))

total_survival_bonus, total_combat_bonus = calculate_combination_bonus(selected_gear)
print(f"Total Survival Bonus: {total_survival_bonus}")
print(f"Total Combat Bonus: {total_combat_bonus}")