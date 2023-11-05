import csv
from tabulate import tabulate
import timeit

items = []
combinations = []

with open('gear.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        items.append([row[0], float(row[1]), int(row[2]), int(row[3])])

with open('combinations.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        combinations.append([row[0], row[1], row[2], int(row[3]), int(row[4])])

# Set the weight limit for gear
weight_limit = 10  # adjust this value

# Define a function to calculate the combined attributes of gear combinations
def calculate_combination_bonus(selected_gear):
    total_survival = 0
    total_combat = 0
    for gear in selected_gear:
        total_survival += gear[2]
        total_combat += gear[3]
    for combo in combinations:
        if combo[0] in selected_gear and combo[1] in selected_gear:
            total_survival += combo[3]
            total_combat += combo[4]
    return [total_survival, total_combat, (total_survival + total_combat) / gear[1]]

# Greedy algorithm to select gear
def select_items():
    selected_gear = []
    current_weight = 0.0
    while current_weight < weight_limit:
        best_gear = None
        best_combination_bonus = 0

        for gear in items:
            if gear not in selected_gear and current_weight + gear[1] <= weight_limit:
                selected_gear.append(gear)
                bonus = calculate_combination_bonus(selected_gear)
                if bonus[2] > best_combination_bonus:
                    best_combination_bonus = bonus[2]
                    best_gear = gear
                selected_gear.remove(gear)

        if best_gear is not None:
            selected_gear.append(best_gear)
            current_weight += best_gear[1]
        else:
            break

    print(tabulate(selected_gear, headers=["Item", "Weight", "Survival", "Combat"]))

    total_survival_bonus, total_combat_bonus, _ = calculate_combination_bonus(selected_gear)
    print(f"Total Survival Bonus: {total_survival_bonus}")
    print(f"Total Combat Bonus: {total_combat_bonus}")

start_time = timeit.default_timer()
select_items()
print("Select items took:", timeit.default_timer() - start_time, 'seconds')

# This is O(n^3) because the outer loop is O(n) and the inner loop is O(n) and the innermost loop is O(n).
