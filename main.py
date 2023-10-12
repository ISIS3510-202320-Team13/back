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
        

        if (rate == -1) or (rate > (t_rate)):
            rate = t_rate
            price = t_price
            choice = doc.id

        if dist <= 500:
            docdic["distance"] = round(dist, 2)
            docdic["choice"] = False
            ret[doc.id] = docdic
    
    temp = ret.copy()
    p_choosed = temp.pop(choice)
    if price == p_choosed["price"]:
        p_choosed["price_match"] = True
        p_choosed["choice"] = True

    temp["choice"] = p_choosed

    return temp
    