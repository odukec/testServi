import os
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson.json_util import dumps
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyAYVHSbEo-Rh1qBeOOk_BKiXns7bzVniyQ')

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'usuarios'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/usuarios'

mongo = PyMongo(app)

@app.route('/usuario', methods=['GET'])
def get_users():
    _id = request.args.get('id')
    if _id is not None:
        user = mongo.db.users
        s = user.find_one({'id' : _id})
        if s:
            output = { s }
        else:
            output = "User not found!"
        return dumps(output) 

@app.route('/lista', methods=['GET'])
def get_all_users():
    output = []
    user = mongo.db.users
    for s in user.find():
        output.append( s )
    return dumps(output)    

@app.route('/crear', methods=['POST'])
def add_user():
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

@app.route('/eliminar', methods=['DELETE'])
def del_user():
    user = mongo.db.users
    _id = request.args.get('id')
    if _id is not None:
        s = user.remove({'id' : _id,})
        if s:
            output = "User removed!"
            return dumps(output) 
        else:
            output = "User not found!"
            return dumps(output) 
    else:
        return dumps('You must give an ID!')

@app.route('/geocodificar_base', methods=['GET'])
def getGeoBase():
    user = mongo.db.users
    for s in user.find():
        if s['lattitud'] == '0' and s['longitud'] == '0':
            geocode = gmaps.geocode(s['address'])
            user.update({'id': s['id']},{'lattitud':geocode[0]["geometry"]["location"]["lat"], "longitud":geocode[0]["geometry"]["location"]["lng"] }, upsert=True)
    return dumps('Operation succesfully!')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(port=port, debug=True)
