from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017')#localhost connection

db = client.track_location_db
app = Flask(__name__)


@app.route('/emp_registration_edit/<string:name>', methods=['PUT'])
def emp_registration_edit(name):


    client = MongoClient('mongodb://localhost:27017')  # localhost connection

    db = client.database1  # created colection
    sub_collection1 = db.collection1
    login_user = sub_collection1.find_one(
        {'_id': ObjectId('5d0a122718262e5eb62fefe4')})
    print(login_user)
    var1 = sub_collection1.update_one({'_id': ObjectId('5d0a122718262e5eb62fefe4')},
                                      {
                                          "$set":
                                              {'title': 'Learning test', 'content': 'Learn mongo, it is tough'}
                                      }
                                      )
    login_user1 = sub_collection1.find_one({'_id': ObjectId('5d0a122718262e5eb62fefe4')})


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)

'''
@app.route('/quarks/<string:name>', methods=['PUT'])
def editOne(name):
    new_quark = request.get_json()
    for i,q in enumerate(quarks):
      if q['name'] == name:
        quarks[i] = new_quark    
    qs = request.get_json()
    return jsonify({'quarks' : quarks})
'''
