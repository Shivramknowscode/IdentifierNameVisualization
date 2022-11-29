from flask import Flask
from flask_restful import Resource, Api, request
from flask_cors import CORS
from pprint import pprint

from PosParser import PosParser
from utils import read_csv, make_csv

app = Flask(__name__)
api = Api(app)
CORS(app,
     origins="*",
     allow_headers=["Content-Type", "Access-Control-Allow-Origin"])


class GetAllTm(Resource):

    def get(self):
        pos_query = request.args['posterm']
        search_query = request.args['searchterm']
        search_query = search_query and search_query.split(',')
        print(pos_query, search_query)

        pos = PosParser("./data/sample.csv")
        pos.make_trie()

        final_data = None
        result = None

        if pos_query and pos_query != 'all' and len(search_query) == 0:
            result = pos.filter_word_by_pos(pos_query)
            result = result.trie.values()
            prepared_data = pos.create_tree_map_csv(result)
            make_csv(prepared_data)
            final_data = read_csv()
        elif pos_query and len(search_query) == 0:
            raw_data = pos.trie.values()
            prepared_data = pos.create_tree_map_csv(raw_data)
            make_csv(prepared_data)
            final_data = read_csv()
        elif pos_query and len(search_query) > 0:
            if pos_query != 'all':
                result = pos.filter_word_by_pos(pos_query)
                raw_data = result.trie.values()
            else:
                raw_data = pos.trie.values()
            final_result = []
            for t in search_query:
                for item in raw_data:
                    if t.lower() in item["raw_words"]:
                        final_result.append(item)
            prepared_data = pos.create_tree_map_csv(final_result)
            make_csv(prepared_data)
            final_data = read_csv()
        else:
            raw_data = pos.trie.values()
            prepared_data = pos.create_tree_map_csv(raw_data)
            make_csv(prepared_data)
            final_data = read_csv()

        return final_data


class GetAllSb(Resource):

    def get(self):
        pos_query = request.args['posterm']
        search_query = request.args['searchterm']
        search_query = search_query and search_query.split(',')
        print(pos_query, search_query)

        pos = PosParser("./data/sample.csv")
        pos.make_trie()

        final_data = None
        result = None

        if pos_query and pos_query != 'all' and len(search_query) == 0:
            result = pos.filter_word_by_pos(pos_query)
            result = result.trie.values()
            final_data = pos.create_sunburst_data(result)
        elif pos_query and len(search_query) == 0:
            raw_data = pos.trie.values()
            final_data = pos.create_sunburst_data(raw_data)
        elif pos_query and len(search_query) > 0:
            if pos_query != 'all':
                result = pos.filter_word_by_pos(pos_query)
                raw_data = result.trie.values()
            else:
                raw_data = pos.trie.values()
            final_result = []
            for t in search_query:
                for item in raw_data:
                    if t.lower() in item["raw_words"]:
                        final_result.append(item)
            final_data = pos.create_sunburst_data(final_result)
        else:
            raw_data = pos.trie.values()
            final_data = pos.create_sunburst_data(raw_data)

        return final_data


api.add_resource(GetAllTm, "/")
api.add_resource(GetAllSb, "/sb")

if __name__ == "__main__":
    app.run(debug=True)
