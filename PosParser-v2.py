import pygtrie
from csv import reader
from pprint import pprint
from random import random


class PosParser:
    """Part of speech, word parser"""

    ALLOWED_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "

    def __init__(self, file=None):
        self.file = file
        self.data = None
        self.trie = None
        self.print = None  # Store printable data
        self.current_result = None

    # return example -> str: 'workspace file mask'
    def clean_words(self, words):
        lowercased = words.lower()
        result = "".join(e for e in lowercased if e in PosParser.ALLOWED_CHARS)
        return result

    # return example -> list<str>:
    # ['NM/workspace/0.5675714129699463', 'NM/file/0.8837231705519263', 'N/mask/0.9825123719848783']
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
        return ["/".join(i.split('/')[0:2]) for i in words]

    def clean_result(self, result):
        cleaned_identifier = "/".join(result[0].split("/")[0:2])
        cleaned_pos_words = self.pos_words_cleaner(result[1]["pos_words"])
        cleaned_data = {**result[1], "pos_words": cleaned_pos_words}
        return (cleaned_identifier, cleaned_data)

    # return example -> list<dict>:
    # [
    # ...,
    # {'identifier': 'WorkspaceFileMask',
    #  'language': 'Java',
    #  'pos_words': ['NM/workspace/0.3871674661078577',
    #                'NM/file/0.30064693460391667',
    #                'N/mask/0.9048221147389223'],
    #  'raw_words': ['workspace', 'file', 'mask'],
    #  'system': 'jenkins.srcml.xml_identifiers'},
    # ...]
    def format_words(self):
        with open(self.file) as file:
            csv_data = reader(file)
            for _ in csv_data:
                data = map(
                    lambda row: {
                        "identifier": "".join(row[0].split(" ")),
                        "pos_words": self.make_word_pos(row),
                        "language": row[-1],
                        "system": "".join(
                            [w for w in row[-2] if w not in "'{}\""]),
                        "raw_words": [w.lower() for w in row[0].split(" ")]
                    }, csv_data)
                # pprint(list(data))
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

    # return example -> list<dict>:
    # [...,
    #   {'identifier': 'WorkspaceFileMask',
    #   'language': 'Java',
    #   'pos_words': ['NM/workspace', 'NM/file', 'N/mask'],
    #   'raw_words': ['workspace', 'file', 'mask'],
    #   'system': 'jenkins.srcml.xml_identifiers'},
    # ...]
    def filter_word_by_pos(self, term):
        try:
            result = list(self.trie[term:])
            printable_result = [{
                **r, "pos_words":
                    self.pos_words_cleaner(r["pos_words"])
            } for r in result]
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


if __name__ == "__main__":
    # Create parser object
    pos = PosParser("data.csv")

    # Make the trie from the data
    pos.make_trie()

    # # Example: Get all words that are a "NM"
    # pprint(pos.filter_word_by_pos("NM"))
    # result = pos.filter_word_by_pos("NM").filter_by_identifier("get")

    result = pos.filter_word_by_pos("D").filter_by_identifier(
    "flight").filter_by_identifier("k")
    pprint(result.print)
    # pprint(result.print)
