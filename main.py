from haversine import haversine, Unit
from geopy.geocoders import Nominatim

from fastapi import FastAPI

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('parkez.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

geolocator = Nominatim(user_agent="ParkEz-API")

app = FastAPI()

@app.get("/parkings/all")
def read_root():
    users_ref = db.collection("parkings")
    docs = users_ref.stream()
    
    ret = {}
    for doc in docs:
        ret[doc.id] = doc.to_dict()

    return ret

@app.get("/users/{uid}")
def read_userInfoByUID(uid: str):

    doc_ref = db.collection('users').document(uid)
    doc = doc_ref.get()
    docdic_user = doc.to_dict()

    user = {'name':docdic_user['name'], 'picture': docdic_user['picture']}

    if "Reservations" in docdic_user:
        reservations = docdic_user["Reservations"]

        res_in_dict = {}

        for reservation in reservations:
            doc_ref = db.collection('reservations').document(reservation)
            doc = doc_ref.get()

            docdic = doc.to_dict()
            docdic.pop('user')

            parking_id = docdic.pop('parking')
            doc_ref_p = db.collection('parkings').document(parking_id)
            doc_p = doc_ref_p.get()

            docdic_p = doc_p.to_dict()
            docdic["parking"] = docdic_p

            res_in_dict[doc.id] = docdic
        
        user['reservations'] = res_in_dict

    return user

@app.get("/address/bylatlon/{lat}/{lon}")
def read_item(lat: str, lon: str):
    location = geolocator.reverse(lat+","+lon).raw['address']
    return {"loc": location}
    
@app.get("/parkings/near/bylatlon/{lat}/{lon}")
def read_item(lat: float, lon: float):
    
    users_ref = db.collection("parkings")
    docs = users_ref.stream()
    
    choice = ""
    rate = -1
    price = 0
    ret = {}

    for doc in docs:
        docdic = doc.to_dict()

        dist = haversine((lat, lon), (float(docdic["coordinates"].latitude), float(docdic["coordinates"].longitude)), unit=Unit.METERS)
        t_price = docdic["price"]
        t_rate = docdic["rating"]*t_price

        if dist <= 500:
            if (rate == -1) or (rate > (t_rate)):
                rate = t_rate
                price = t_price
                choice = doc.id

            docdic["distance"] = round(dist, 2)
            docdic["choice"] = False
            ret[doc.id] = docdic
    
    temp = ret.copy()
    if choice in temp:
        p_choosed = temp.pop(choice)
        if price == p_choosed["price"]:
            p_choosed["price_match"] = True
        else:
            p_choosed["price_match"] = False
        p_choosed["choice"] = True

    ret = {"choice":p_choosed, "others":temp}

    return ret
    