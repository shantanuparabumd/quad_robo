import json


# Reading array data from a JSON file
with open('data.json', 'r') as file:
    array = json.load(file)

print(array)