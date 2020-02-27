# system libraries
import os, random, json, requests
# CREDENTIALS
import app_secrets
# geopy
import geopy
from geopy.distance import great_circle
# flask
from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from flask_cors import CORS
# firebase
import firebase_admin
from firebase_admin import credentials,firestore
# flask config
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
# flask initialization
app = Flask(__name__)
CORS(app)
app.config['KEY'] = app_secrets.FLASK_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
# for location coordinates
geo = geopy.Nominatim()
# firebase initialization
cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), "private/blood-bank-02-firebase-adminsdk-cd6a6-fa563dc413.json"))
firebase = firebase_admin.initialize_app(cred)
db = firestore.client()
# API class
class Createdonor(Resource):
    def post(self):
        # authentication
        key = request.form['key']
        if key is None or key != app.config['KEY']:
            abort(401)

        dui, dname, dlocation, dbgroup, demail, dphone = request.form['ui'], request.form['name'], request.form['location'], request.form['bloodgroup'], request.form['email'], int(request.form['phone'])
        geo = geopy.Nominatim()
        location = geo.geocode(dlocation)
        db.collection('donor').document(f'{dui}').set({
            'name': dname,
            'bloodgroup': dbgroup,
            'email': demail,
            'location': firestore.GeoPoint(location.latitude, location.longitude),
            'phone': dphone
        })

        return 'OK', 201

'''
TODO: implement array parsing
'''
class Createhospital(Resource):
    def post(self):
        # authentication
        key = request.form['key']
        if key is None or key != app.config['KEY']:
            abort(401)

        hui, hname, hlocation, hwebsite, hphone = request.form['ui'], request.form['name'], request.form['location'], request.form['website'], int(request.form['phone'])
        hbgroup = request.form.getlist('bloodgroup')

        location = geo.geocode(hlocation)
        db.collection('hospital').document(f'{hui}').set({
            'name': hname,
            'bloodgroup': hbgroup,
            'website': hwebsite,
            'location': firestore.GeoPoint(location.latitude, location.longitude),
            'phone': hphone
        })

        return 'OK', 201

class Find(Resource):
    def post(self):
        # authentication
        key = request.form['key']
        if key is None or key != app.config['KEY']:
            abort(401)

        name, tmplocation, bloodgroup, phone, find = request.form['name'], request.form['location'], request.form['bloodgroup'], int(request.form['phone']), request.form['find']
        radius = int(request.form['radius'])
        location = geo.geocode(tmplocation)

        blood_list = db.collection('hospital').where('bloodgroup', 'array_contains', bloodgroup).stream()
        final = list()
        for blood in blood_list:
            d = blood.to_dict()
            d_location = (d['location'].latitude, d['location'].longitude)
            if great_circle(d_location, (location.latitude, location.longitude)).km <= radius:
                d['location'] = geo.reverse(d_location)._address
                d['bloodgroup'] = bloodgroup
                print(d)
                final.append(json.loads(json.dumps(d)))


        return final, 201

class Sendsms(Resource):
    def post(self):
        # authentication
        key = request.form['key']
        if key is None or key != app.config['KEY']:
            abort(401)
        name, bloodgroup, phone = request.form['name'], request.form['bloodgroup'], request.form['phone']

        url = 'https://www.fast2sms.com/dev/bulk'
        headers = {
            'authorization': app_secrets.FAST2SMS_KEY,
            'cache-control': "no-cache",
            'content-type': "application/x-www-form-urlencoded"
        }
        payload = "sender_id=FSTSMS&language=english&route=qt&numbers={}&message=YOUR_QT_SMS_ID&variables={#DD#}|{#AA#}&variables_values={}|{}".format(phone,name, bloodgroup)
        response = requests.request("POST", url, data=payload, headers=headers)
        return response.text,201
# url route for API
api.add_resource(Createdonor, '/createdonor')
api.add_resource(Createhospital, '/createhospital')
api.add_resource(Find, '/find')
api.add_resource(Sendsms, '/sendsms')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)
