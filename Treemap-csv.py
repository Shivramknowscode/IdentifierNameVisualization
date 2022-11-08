from csv import reader, writer
data = None
with open("data.csv") as f:
    csv_reader = reader(f)
    d = list(csv_reader)[1:]
    data = [i[0] for i in d]

splited = []
for item in data:
    for i in item.split(" "):
        splited.append(i.lower())

dotted = []
for word in data:
    total = 0
    sp_word = [w.lower() for w in word.split(" ")]
    for w in sp_word:
        total += splited.count(w)
    dotted.append(f'{".".join(word.split(" ")).lower()}, {total}')

with open("dotted-data.csv", "w", newline="") as f:
    csv_writer = writer(f)
    for row in dotted:
        csv_writer.writerow(row.split(", "))
