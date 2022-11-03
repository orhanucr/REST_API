from flask import Flask
from flask_restful import Api, Resource, reqparse
import pandas as pd

app = Flask(__name__)
api = Api(app)


class Book(Resource):
    def get(self):
        data = pd.read_csv('book.csv')
        data = data.to_dict('records')
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True , location= 'args')
        parser.add_argument('author', required=True, location= 'args')
        parser.add_argument('year', required=True, location= 'args')
        parser.add_argument('number_of_pages', required=True, location= 'args')

        args = parser.parse_args()

        data = pd.read_csv('book.csv')

        new_data = pd.DataFrame({
            'name'      : [args['name']],
            'author'       : [args['author']],
            'year'      : [args['year']],
            'number_of_pages' : [args['number_of_pages']]
        })

        data = data.append(new_data, ignore_index = True)
        data.to_csv('book.csv', index=False)
        return {'data' : new_data.to_dict('records')}, 201

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location= 'args')
        args = parser.parse_args()

        data = pd.read_csv('book.csv')
        data = data[data['name'] != args['name']]

        data.to_csv('book.csv', index=False)
        return {'message': 'Record deleted successfully.'}, 200


class Year(Resource):
    def get(self):
        data = pd.read_csv('book.csv', usecols=[3])
        data = data.to_dict('records')
        return {'data': data}, 200

class Number_Of_Pages(Resource):
    def get(self):
        data = pd.read_csv('book.csv', usecols=[3])
        data = data.to_dict('records')
        return {'data': data}, 200
class Author(Resource):
    def get(self):
        data = pd.read_csv('book.csv', usecols=[3])
        data = data.to_dict('records')
        return {'data': data}, 200

class Name(Resource):
    def get(self, name):
        data = pd.read_csv('book.csv')
        data = data.to_dict('records')
        for entry in data:
            if entry['name'] == name:
                return {'data': entry}, 200
        return {'message': 'No entry found with this name !'}, 200



api.add_resource(Book, '/book')
api.add_resource(Name, '/<string:name>')
api.add_resource(Author, '/author')
api.add_resource(Year, '/year')
api.add_resource(Number_Of_Pages, '/number_of_pages')



if __name__ == '__main__':
    app.run()