from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_restful import Api,Resource
from bson.objectid import ObjectId
import json
from bson.json_util import dumps


app = Flask(__name__)
api = Api(app)
app.config['MONGO_URI'] = 'mongodb+srv://admin:admin@neargroup.i1hko.mongodb.net/test'
mongo = PyMongo(app)


class TodoList(Resource):
    def get(self):
        customers = mongo.db.crudApp.find()
        resp = dumps(customers)
        res = resp.replace("\"","")
        return res

    def post(self):
        _json = request.get_json(force=True)
        _user_id = _json['user_id']
        _amount = _json['amount']
        _coins_balance = _json['coins_balance']
        _txn_type = _json['txn_type']
        _txn_info = _json['txn_info']
        _action = _json['action']
        _time = _json['time']
        if _user_id and _amount and _coins_balance and _txn_type and _txn_info and _action and _time and request.method == 'POST':
            id = mongo.db.crudApp.insert({'user_id':_user_id,'amount':_amount,'coins_balance':_coins_balance,'txn_type':_txn_type,'txn_info':_txn_info,'action':_action,'time':_time })
            resp = jsonify("User added successfully.")
            resp.status_code = 200
            return resp
        else:
            not_found()


class TodoAgain(Resource):

    def get(self,id):
        customer = mongo.db.crudApp.find_one({'_id':ObjectId(id)})
        resp = dumps(customer)
        res = resp.replace("\"","")
        return res

    ## updating record.
    def put(self,id):
        _id = id
        _json = request.json
        _user_id = _json['user_id']
        _amount = _json['amount']
        _coins_balance = _json['coins_balance']
        _txn_type = _json['txn_type']
        _txn_info = _json['txn_info']
        _action = _json['action']
        _time = _json['time']
        if _id and request.method == 'PUT':
            mongo.db.crudApp.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set':{'user_id':_user_id,'amount':_amount,'coins_balance':_coins_balance,'txn_type':_txn_type,'txn_info':_txn_type,'action':_action,'time':_time}})
            resp = jsonify("User updated successfully.")
            return resp
        else:
            return not_found()

    def delete(self,id):
        mongo.db.crudApp.delete_one({'_id':ObjectId(id)})
        resp = jsonify("User deleted successfully.")
        return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
    'status': 404,
    'message': 'Not found'+request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

api.add_resource(TodoList, '/')
api.add_resource(TodoAgain, '/todo/<id>')
api = Api(app)


if __name__ == '__main__':
    app.run(debug=True)
