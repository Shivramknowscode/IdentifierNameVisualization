import pygtrie
from csv import reader
from pprint import pprint


class PosParser:
    """Part of speech, word parser"""

    ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "

    # Class attribute to define allowed characters

    def __init__(self, file):
        self.file = file
        self.data = None
        self.trie = None

    # instance attributes

    def clean_words(self, words):
        lowercased = words.lower()
        return "".join(e for e in lowercased if e in PosParser.ALLOWED_CHARS)

    # normalizes data

    def make_word_pos(self, row):
        result = []
        words = self.clean_words(row[0]).split(" ")
        pos_words = row[1].split(" ")
        i = 0
        while i < len(words):
            word = f"{pos_words[i]}/{words[i]}"
            result.append(word)
            i += 1
        return result

    # associates PoS tag with individual words in an identifier name

    def format_words(self):
        with open(self.file) as file:
            csv_data = reader(file)
            for row in csv_data:
                data = map(
                    lambda row: {
                        "identifier": "".join(row[0].split(" ")),
                        "pos_words": self.make_word_pos(row),
                        "language": row[-1],
                        "system": "".join(
                            [w for w in row[-2] if w not in "'{}\""]),
                        "raw_words": [w.lower() for w in row[0].split(" ")]
                    }, csv_data)
                self.data = list(data)

    # creates a dictionary of associated data with a word (identifier name, pos words, programming language, raw words, source of identifier name)

    def make_trie(self):
        t = pygtrie.StringTrie()
        self.format_words()
        for item in self.data:
            for word in item["pos_words"]:
                t[word] = item
        self.trie = t

    # creates the trie using pygtrie

    def filter_word_by_pos(self, term):
        try:
            return list(self.trie[term:])
        except (KeyError):
            return "Could not find any word with the given term"

    # filters by PoS tag

    def post_term_count(self, term):
        return len(list(self.trie[term:]))

    # shows number of instances of word in the dataset

    def filter_by_identifier(self, term):
        result = []
        for item in self.trie.items():
            if term.lower() == item[0].split("/")[1]:
                result.append(item)
        return result
    # filters data by word and shows all instances of word


if __name__ == "__main__":
    # Create parser object
    pos = PosParser("data.csv")

    # Make the trie from the data
    pos.make_trie()

    # # Example1: Get all words that are a "NM"
    # pprint(pos.filter_word_by_pos("NM"))

    # # Example2: Search by identifier
    pprint(pos.filter_by_identifier("Get"))

    # # Example3: Get the total count of a POS term
    # pprint(pos.post_term_count("NM"))
