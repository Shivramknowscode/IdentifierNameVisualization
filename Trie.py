import pygtrie
from csv import reader
from pprint import pprint


def split_words(words):
    return "/".join(words.split(" "))


def format_words(words):
    ALLOWED = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
    lowercased = words.lower()
    cleaned = "".join(e for e in lowercased if e in ALLOWED)
    final_words = "/".join(cleaned.split(" "))
    return final_words


def prepare_data(csv_file):
    with open(csv_file) as file:
        csv_data = reader(file)
        data = map(
            lambda row: [
                format_words(row[0]),
                split_words(row[1]),
                split_words(row[2]),
                split_words(row[3]),
                split_words(row[4]), *row[5:]
            ], csv_data)
        return list(data)


def make_trie(file):
    t = pygtrie.StringTrie()
    data = prepare_data(file)
    for row in data:
        words = row[0].split("/")
        grammar = row[1].split("/")
        i = 0
        while i < len(words):
            t[f"{grammar[i]}/{words[i]}"] = {
                "word": words[i],
                "lang": str(row[-1]).lower()
            }
            i += 1
    return t


def filter_word_by_pos(term, trie):
    return list(trie[term:])


def filter_by_word(word, trie):
    result = []
    for item in trie.items():
        if str(item[1]["word"]) == word:
            result.append(item)  # item[0]
    return result


def grammar_pattern_count(grammar_term, trie):
    return len(list(trie[grammar_term:]))


t = make_trie("data.csv")

# pprint(t.items())

# pprint(filter_word_by_pos("NM", t))

# pprint(filter_by_word("item", t))

print(grammar_pattern_count("NM", t))
