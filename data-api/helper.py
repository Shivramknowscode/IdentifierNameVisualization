from csv import reader, writer
from pprint import pprint


# def make_csv(data):
#     with open("data.csv", "w", newline="") as file:
#         csv_writer = writer(file)
#         for row in data:
#             csv_writer.writerow(row.split(","))


# def read_csv():
#     with open("data.csv") as f:
#         return f.read()


def make_csv():
    data = None
    with open("sample.csv") as f:
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
        print(sp_word)
        for w in sp_word:
            total += splited.count(w)
        dotted.append(f'{".".join(word.split(" ")).lower()}, {total}')

    # pprint(dotted)

    with open("data.csv", "w", newline="") as f:
        csv_writer = writer(f)
        for row in dotted:
            csv_writer.writerow(row.split(", "))


def read_data():
    with open("data.csv") as f:
        return f.read()


if __name__ == "__main__":
    make_csv()
