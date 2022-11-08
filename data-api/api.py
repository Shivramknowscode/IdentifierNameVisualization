from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

# from helper import make_csv, read_data

from PosParser import PosParser
from utils import read_csv, make_csv

app = Flask(__name__)
api = Api(app)
CORS(app, origins="*", allow_headers=["Content-Type", "Access-Control-Allow-Origin"])


# class CSVData(Resource):
#     def get(self):
#         make_csv()
#         data = read_data()
#         return data


class GetAllTm(Resource):
    def get(self):
        pos = PosParser("./data/sample.csv")
        pos.make_trie()
        raw_data = pos.trie.values()
        prepared_data = pos.create_tree_map_csv(raw_data)
        make_csv(prepared_data)
        final_data = read_csv()
        return final_data


# api.add_resource(CSVData, "/")
api.add_resource(GetAllTm, "/")

if __name__ == "__main__":
    app.run(debug=True)
