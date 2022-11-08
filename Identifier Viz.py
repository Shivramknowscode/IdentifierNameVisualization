from csv import reader, writer


class Trie:

    def __init__(self):
        self.root = {"*": "*"}

    def add_word(self, word):
        curr_node = self.root
        for letter in word:
            if letter not in curr_node:
                curr_node[letter] = {}
            curr_node = curr_node[letter]
        curr_node["*"] = "*"

    def does_word_exist(self, word):
        curr_node = self.root
        for letter in word:
            if letter not in curr_node:
                return False
            curr_node = curr_node[letter]
        return "*" in curr_node


# basic trie implementation

ALLOWED = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
raw_data = None

with open("data.csv") as file:
    csv_reader = reader(file)
    original_headers = next(csv_reader)
    raw_data = list(csv_reader)

# reading all the data in the first column

with open("cleaned.csv", "w", newline="") as file:
    csv_writer = writer(file)

    cleaned = []
    i = 0
    while i < len(raw_data):
        new_row = []
        l_str = raw_data[i][0].lower()
        new_row.append(",".join("".join(e for e in l_str
                                        if e in ALLOWED).split(" ")))
        j = 0
        while j < len(raw_data[i]) - 1:
            d = raw_data[i]
            d.pop(0)
            new_row.append(d[j])
            j += 1
        cleaned.append(new_row)
        i += 1

    csv_writer.writerow(original_headers)
    csv_writer.writerows(cleaned)

with open("cleaned.csv") as file:
    csv_reader = reader(file)
    all_words = []
    for row in csv_reader:
        all_words.append(row[0].split(","))

# cleaning up row 1 by lowercasing all letters and removing anything but a-z, A-Z & 0-9, - also removes spaces and creates a list for each identifier name and replaces it in the cleaned file

trie = Trie()

for words in all_words:
    for word in words:
        trie.add_word(word)

# creating one big trie with all identifier names in row 1 (using pygtrie)

print(trie.does_word_exist("selection"))
print(trie.does_word_exist("buffer"))
print(trie.does_word_exist("cow"))

# testing to see if words 'selection', 'buffer' & 'cow' exists in any of the identifier names
