from csv import reader
from pprint import pprint
import json

file_data = []
identifier_data = []
identifier_list = []
unique_pos_words = set()
vis = []

workable = []

# Prepare data
with open("data.csv") as f:
    csv_reader = reader(f)
    data = list(csv_reader)
    for i in data:
        word = " ".join(i[0].split()).lower()
        identifier_list.append(word)
        identifier_data.append({
            "identifier":
            word,
            "raw_words":
            list(map(lambda w: w.lower(), i[0].split(" "))),
        })

# Get unique words
for i in identifier_data:
    for j in i["raw_words"]:
        unique_pos_words.add(j)

for id in unique_pos_words:
    data = {"name": id, "children": []}
    for w in identifier_list:
        if id in w:
            formated = "".join(word.capitalize() for word in w.split(" "))
            data["children"].append({"name": formated, "value": 1})
    workable.append(data)

json_data = json.dumps(workable)
pprint(json_data)
