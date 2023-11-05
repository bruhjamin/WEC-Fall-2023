import timeit
import pulp
import csv

from tabulate import tabulate

# util function to calculate totals
def calculate_totals(selected_gear):
    survival = 0
    combat = 0
    surv_bonus = 0
    combat_bonus = 0
    for name in selected_gear:
        survival += gear_data[name]['surv']
        combat += gear_data[name]['combat']
    for combo in combinations:
        if combo['name1'] in selected_gear and combo['name2'] in selected_gear:
            surv_bonus += combo['surv_bonus']
            combat_bonus += combo['combat_bonus']
    return survival + surv_bonus, combat + combat_bonus, surv_bonus, combat_bonus
# Initialize the LP problem
problem = pulp.LpProblem("GearOptimization", pulp.LpMaximize)

# Read gear data from CSV
gear_data = {}
with open('gear.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        name, weight, surv, combat = row
        gear_data[name] = {'weight': float(weight), 'surv': int(surv), 'combat': int(combat)}

# Read combination data from CSV
combinations = []
with open('combinations.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        name1, name2, comb_name, surv_bonus, combat_bonus = row
        combinations.append({
            'name1': name1, 'name2': name2, 'comb_name': comb_name,
            'surv_bonus': int(surv_bonus), 'combat_bonus': int(combat_bonus)
        })

# Create gear variables
gear_vars = {name: pulp.LpVariable(name, 0, 1, pulp.LpBinary) for name in gear_data}

# Create combination variables
comb_vars = {comb['comb_name']: pulp.LpVariable(comb['comb_name'], 0, 1, pulp.LpBinary) for comb in combinations}

# Add weight constraint
max_weight = 10 # Set your weight limit here
problem += pulp.lpSum(gear_data[name]['weight'] * gear_vars[name] for name in gear_data) <= max_weight

# Add objective function
objective = pulp.lpSum(gear_data[name]['surv'] * gear_vars[name] + gear_data[name]['combat'] * gear_vars[name] for name in gear_data)
for comb in combinations:
    objective += (comb['surv_bonus'] + comb['combat_bonus']) * comb_vars[comb['comb_name']]
problem += objective


# start timer
start_time = timeit.default_timer()

# Solve the MILP problem
problem.solve()

# Print the results
print("Optimal Solution:")

selected_gear = []

for name, var in gear_vars.items():
    if var.varValue > 0.5:
        selected_gear.append(name)

total_surv, total_combat, surv_bonus, combat_bonus = calculate_totals(selected_gear)

data = []
for name in selected_gear:
    data.append([name, gear_data[name]['weight'], gear_data[name]['surv'], gear_data[name]['combat']])
    
print(tabulate(data, ["Item", "Weight", "Survival", "Combat"]))
print("Total Survival:", total_surv)
print("Total Combat:", total_combat)
print("Survival Bonus:", surv_bonus)
print("Combat Bonus:", combat_bonus)
print("Select items took:", timeit.default_timer() - start_time, 'seconds')