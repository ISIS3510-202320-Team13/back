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
    
    ret = {}
    for doc in docs:
        docdic = doc.to_dict()
        dist = haversine((lat, lon), (float(docdic["coordinates"].latitude), float(docdic["coordinates"].longitude)), unit=Unit.METERS)
        if dist <= 500:
            docdic["distance"] = dist
            ret[doc.id] = docdic
    
    return ret
    