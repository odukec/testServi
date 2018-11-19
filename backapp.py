import os
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'usuarios'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/usuarios'

mongo = PyMongo(app)

@app.route('/user', methods=['GET'])
def get_all_users():
    _id = request.args.get('id')
    user = mongo.db.users
    if _id is None:
        output = []
        for s in user.find():
            output.append({ s })
        return dumps(output)
    else:
        s = user.find_one({'id' : _id})
        if s:
            output = { s }
        else:
            output = "User not found!"
        return dumps(output) 
    

@app.route('/crear', methods=['POST'])
def add_star():
    user = mongo.db.users
    name = request.json['name']
    surname = request.json['surname']
    address = request.json['address']
    city = request.json['city']
    idu = request.json['id']
    user_id = user.insert({
        'name': name, 
        'surname': surname,
        'address': address,
        'city': city,
        'id': idu,
        'lattitud': '0',
        'longitud': '0'
    })
    new_user = user.find_one({'_id': user_id })
    return dumps(new_user)

@app.route('')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(port=port, debug=True)