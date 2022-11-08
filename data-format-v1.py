from csv import reader
import json
from pprint import pprint

identifier_data = []


"""
Example:
pprint(identifier_data[2])

Output:
[...
    {'identifiers': 'bke lattice index flip',
    'word': 'BkeLatticeIndexFlip',
    'word_list': ['bke', 'lattice', 'index', 'flip']}
...]
"""
with open("data.csv") as f:
    csv_reader = reader(f)
    data = list(csv_reader)
    for i in data:
        word = " ".join(i[0].split()).lower()
        identifier_data.append(
            {
                "identifiers": word,
                "word_list": list(map(lambda w: w.lower(), i[0].split(" "))),
                "word": "".join(w.capitalize() for w in word.split(" ")),
            }
        )

# pprint(identifier_data[2])

"""
Example:
pprint(identifiers_table)

Output:
[[...],
 ['identifier', 'name'],
 ['ares', 'expand', 'name', 'for', 'response'],
 ['bke', 'lattice', 'index', 'flip'], 
 [...]]
"""
identifiers_table = []
for item in identifier_data:
    identifiers_table.append(item["word_list"])

# pprint(identifiers_table)

final_struct = {"name": "visualization", "children": []}

for row in identifiers_table:
    temps = []
    for word in row:
        obj = {"name": word, "children": []}
        temps.append(obj)
    c = len(temps) - 1
    while c > 0:
        temps[c - 1]["children"].append(temps[c])
        c -= 1
    final_struct["children"].append(temps[0])


"""Convert to JSON"""
json_data = json.dumps(final_struct)

"""Write JSON data to file"""
with open("struct.json", "w") as f:
    f.write(json_data)

# result = []

# # print(identifier_data[0])

# for i in identifier_data:
#     temp = {"name": i["word_list"][0], "children": set()}
#     for word in i["word_list"]:
#         for j in identifier_data:
#             if j["word_list"][0] == temp["name"]:
#                 for id in j["word_list"]:
#                     if temp["name"] != id:
#                         temp["children"].add(id)
#     result.append(temp)

# pprint(result)
