import pygtrie
from csv import reader
from random import random
from pprint import pprint


class PosParser:
    ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "

    def __init__(self, file=None):
        self.file = file
        self.data = None
        self.trie = None
        self.print = None
        self.current_result = None
        self.pos_term_list = set()
        self.unique_words_list = set()
        self.all_words_list = []
        self.words_count = []
        self._make_pos_term_list()
        self._make_unique_word_list()
        self._make_words_stat()

    def _make_pos_term_list(self):
        with open(self.file) as f:
            cr = reader(f)
            next(cr)
            for row in cr:
                for term in row[1].split(" "):
                    self.pos_term_list.add(term)

    def _make_unique_word_list(self):
        with open(self.file) as f:
            cr = reader(f)
            next(cr)
            for row in cr:
                for term in row[0].split(" "):
                    self.unique_words_list.add(term.lower())
                    self.all_words_list.append(term.lower())

    def _make_words_stat(self):
        for word in self.unique_words_list:
            self.words_count.append({word: self.all_words_list.count(word)})

    def clean_words(self, words):
        lowercased = words.lower()
        result = "".join(e for e in lowercased if e in PosParser.ALLOWED_CHARS)
        return result

    def make_word_pos(self, row):
        result = []
        words = self.clean_words(row[0]).split(" ")
        pos_words = row[1].split(" ")
        i = 0
        while i < len(words):
            word = f"{pos_words[i]}/{words[i]}/{str(random())}"
            result.append(word)
            i += 1
        return result

    def pos_words_cleaner(self, words):
        return ["/".join(i.split("/")[0:2]) for i in words]

    def clean_result(self, result):
        cleaned_identifier = "/".join(result[0].split("/")[0:2])
        cleaned_pos_words = self.pos_words_cleaner(result[1]["pos_words"])
        cleaned_data = {**result[1], "pos_words": cleaned_pos_words}
        return (cleaned_identifier, cleaned_data)

    def format_words(self):
        with open(self.file) as file:
            csv_data = reader(file)
            for _ in csv_data:
                data = map(
                    lambda row: {
                        "identifier": "".join(row[0].split(" ")),
                        "pos_words": self.make_word_pos(row),
                        "language": row[-1],
                        "system": "".join([w for w in row[-2] if w not in "'{}\""]),
                        "raw_words": [w.lower() for w in row[0].split(" ")],
                    },
                    csv_data,
                )
                self.data = list(data)

    def make_trie(self):
        t = pygtrie.StringTrie()
        self.format_words()
        for item in self.data:
            for word in item["pos_words"]:
                t[word] = item
        self.trie = t

    def make_trie_sm(self, data):
        t = pygtrie.StringTrie()
        for item in data:
            for word in item["pos_words"]:
                t[word] = item
        return t

    def filter_word_by_pos(self, term):
        try:
            result = list(self.trie[term:])
            printable_result = [
                {**r, "pos_words": self.pos_words_cleaner(r["pos_words"])}
                for r in result
            ]
            result_trie = self.make_trie_sm(self.trie[term:])
            result_pos_obj = PosParser(self.file)
            result_pos_obj.trie = result_trie
            result_pos_obj.print = printable_result
            return result_pos_obj
        except (KeyError):
            return "Could not find any word with the given term"

    def post_term_count(self, term):
        return len(list(self.trie[term:]))

    def filter_by_identifier(self, term):
        trie_results = []
        result = []
        for item in self.trie.items():
            if term.lower() == item[0].split("/")[1]:
                trie_results.append(item[1])
                result.append(self.clean_result(item))
        result_trie = self.make_trie_sm(trie_results)
        result_pos_obj = PosParser(self.file)
        result_pos_obj.trie = result_trie
        result_pos_obj.print = result
        return result_pos_obj

    def create_tree_map_csv(self, data):
        all_words = []
        for item in data:
            for word in item["raw_words"]:
                all_words.append(word)
        prep_data = []
        for item in data:
            prep_data.append(item["raw_words"])
        pprint(list(set(map(lambda i: " ".join(i), prep_data))))
        csv_ready_data = []
        for item in data:
            total = 0
            for word in item["raw_words"]:
                total += all_words.count(word)
            csv_ready_data.append(f'{".".join(item["raw_words"])},{total}')
        return csv_ready_data


if __name__ == "__main__":
    pass
    pos = PosParser("./data/sample.csv")
    pos.make_trie()
    result = pos.trie.values()
    res = pos.create_tree_map_csv(result)
    # result = pos.filter_word_by_pos("NPL")
    # pos.create_tree_map_csv(result.print)
    # data = result.print
    # pprint(data)
