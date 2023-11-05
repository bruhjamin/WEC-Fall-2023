import csv
from tabulate import tabulate

items = []

with open('gear.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        items.append([row[0], row[1], row[2], row[3]])

# sort items
def sort_items(items, sort_by):
    items.sort(key=sort_by)
    print(tabulate(items, headers=["Item", "Weight", "Survival", "Combat"]))

sort_items(items, lambda x: x[0])
sort_items(items, lambda x: (float(x[1]), x[0]))
sort_items(items, lambda x: (int(x[2]), x[0]))
sort_items(items, lambda x: (int(x[3]), x[0]))
