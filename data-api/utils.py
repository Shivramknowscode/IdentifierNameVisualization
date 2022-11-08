from csv import writer


def make_csv(data):
    with open("data.csv", "w", newline="") as file:
        csv_writer = writer(file)
        for row in data:
            csv_writer.writerow(row.split(","))


def read_csv():
    with open("data.csv") as f:
        data = f.read()
        return data
