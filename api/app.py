# system libraries
import os, random, json, requests, smtplib
from datetime import date, datetime, timedelta
# UTILITY
from scripts.utility import sendsms, sendemail
# CREDENTIALS
from app_secrets import FLASK_KEY, GMAIL_APP_KEY
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
app.config['KEY'] = FLASK_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
# for location coordinates
geo = geopy.Nominatim(timeout=5)
# firebase initialization
cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), "private/blood-bank-826da-firebase-adminsdk-7g896-f208f8a8fc.json"))
firebase = firebase_admin.initialize_app(cred)
db = firestore.client()
# API class
class Createdonor(Resource):
    def post(self):
        # authentication
        key = dict(request.form)['key']
        if key is None or key != app.config['KEY']:
            abort(401)

        dname, dlocation, dbgroup, demail, dphone, sex, age, weight = dict(request.form)['name'], dict(request.form)['location'], dict(request.form)['bloodgroup'], dict(request.form)['email'], dict(request.form)['phone'], dict(request.form)['sex'], dict(request.form)['age'], dict(request.form)['weight']
        try:
            location = geo.geocode(dlocation)
        except geopy.exc.GeocoderServiceError:
            abort(401)
        d_date = dict(request.form)['date']
        db.collection('donor').document(f'{demail}').set({
            'name': dname,
            'bloodgroup': dbgroup,
            'email': demail,
            'location': firestore.GeoPoint(location.latitude, location.longitude),
            'phone': int(dphone),
            'sex': sex,
            'age': age,
            'weight': weight,
            'date': d_date
        })

        return 'HOI GECHEY', 201

class Find(Resource):
    def post(self):
        # authentication
        key = dict(request.form)['key']
        if key is None or key != app.config['KEY']:
            abort(401)

        tmplocation, bloodgroup,= dict(request.form)['location'], dict(request.form)['bloodgroup']

        radius = float(request.form['radius'])
        try:
            location = geo.geocode(tmplocation)
        except geopy.exc.GeocoderServiceError:
            abort(402)
        except LookupError:
            abort(405)

        blood_list = db.collection('donor').where('bloodgroup', '==', bloodgroup).stream()
        final = list()
        current_date = datetime.today().date()
        for blood in blood_list:
            d = blood.to_dict()
            d_location = (d['location'].latitude, d['location'].longitude)
            d_date = d['date']

            check_date = datetime.strptime(d_date, "%d %b, %Y").date()

            if (current_date-check_date).days < 84:
                continue
            if great_circle(d_location, (location.latitude, location.longitude)).km <= radius:
                d['location'] = geo.reverse(d_location)._address

                final.append(json.loads(json.dumps(d)))

        return final, 201

class Notify(Resource):
    def post(self):
        # authentication
        key = dict(request.form)['key']
        if key is None or key != app.config['KEY']:
            abort(401)
        # fetching
        rname, rbloodgroup, phones, rlocation, rphone = dict(request.form)['name'], dict(request.form)['bloodgroup'], dict(request.form)['phone'], dict(request.form)['location'], dict(request.form)['recipentphone']
        phones = phones.split()
        emails = list()
        try:
            emails = dict(request.form)['email']
            emails = emails.split()
        except KeyError:
            pass
        # cleaning
        if rbloodgroup[-1]=='+':
            rbloodgroup = rbloodgroup[:len(rbloodgroup)-1]+" positive"
        elif rbloodgroup[-1]=='-':
            rbloodgroup = rbloodgroup[:len(rbloodgroup)-1]+" negative"
        
        status_code = None
        for phone in phones:
            sendsms(rname, rlocation, rbloodgroup, phone, rphone)
        fromaddr = "debdutgoswami7@gmail.com"
        for email in emails:
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("debdutgoswami7@gmail.com", GMAIL_APP_KEY)
            text = sendemail(server, rname, rlocation, rbloodgroup, email, rphone)
            server.sendmail(fromaddr, email, text)

        return "OK", 201

class RequestBlood(Resource):
    def post(self):
        # authentication
        key = dict(request.form)['key']
        if key is None or key != app.config['KEY']:
            abort(401)
        name, bloodgroup, location, phone, sex, age = dict(request.form)['name'], dict(request.form)['bloodgroup'], dict(request.form)['location'], int(dict(request.form)['phone']), dict(request.form)['sex'], dict(request.form)['age']
        try:
            location = geo.geocode(location)
        except geopy.exc.GeocoderServiceError:
            abort(401)
        current_date = date.today().strftime("%d %b, %Y")

        db.collection('requestblood').document(f'{phone}').set({
            'name': name,
            'bloodgroup': bloodgroup,
            'location': firestore.GeoPoint(location.latitude, location.longitude),
            'phone': int(phone),
            'sex': sex,
            'age': age,
            'created': current_date
        })

        return "OK", 201

class RequireBlood(Resource):
    def post(self):
        # authentication
        key = dict(request.form)['key']
        if key is None or key != app.config['KEY']:
            abort(401)
        
        request_list = db.collection('requestblood').stream()
        final = list()
        current_date = datetime.today().date()
        for req in request_list:
            d = req.to_dict()
            check_date = datetime.strptime(d['created'], "%d %b, %Y").date()
            if (current_date-check_date).days >= 7:
                db.collection('requestblood').document(f"{d['phone']}").delete()
                continue
            d_location = (d['location'].latitude, d['location'].longitude)
            location = geo.reverse(d_location).address
            d['location'] = location
            final.append(d)

        return final, 201

# url route for API
api.add_resource(Createdonor, '/createdonor')
#api.add_resource(Createhospital, '/createhospital')
api.add_resource(Find, '/find')
api.add_resource(Notify, '/notify')
api.add_resource(RequestBlood, '/requestblood')
api.add_resource(RequireBlood, '/requireblood')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
