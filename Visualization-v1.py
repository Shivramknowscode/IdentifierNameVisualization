from csv import reader
import json
from pprint import pprint
import itertools

identifier_data = []

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

identifiers_table = []

for item in identifier_data:
    identifiers_table.append(item["word_list"])

identifiers_table = identifiers_table[1:]

new_data = []
for item in identifiers_table:
    cols = []
    for lst in identifiers_table:
        if item[0] == lst[0]:
            cols.append([item[0], lst[1:]])
    new_data.append(cols)


nd = []
for item in new_data:
    new = [i[1:][0] for i in item if len(i[1:][0]) != 0]  # remove all empty arrays
    nd.append([item[0][0], new])


# remove duplicates
nd.sort()
fn = list(k for k, _ in itertools.groupby(nd))


# Create the final structure
result = []
for item in fn:
    r = {"name": item[0], "value": len(item[1]), "children": []}
    if len(item[1]) > 0:
        for i in item[1]:
            if len(i) > 1:
                temp = []
                for x in i:
                    temp.append({"name": x, "value": 1, "children": []})
                count = len(temp) - 1
                while count > 0:
                    temp[count - 1]["children"].append(temp[count])
                    temp.pop()
                    count -= 1
                r["children"].append(temp[0])
            else:
                r["children"].append({"name": i[0], "value": 1})
    result.append(r)

final_struct = {"name": "Visualization", "children": result}

json_data = json.dumps(final_struct)

with open("result.json", "w") as f:
    f.write(json_data)
