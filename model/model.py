import firebase_connection as firebase

from haversine import haversine, Unit
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="ParkEz-API")

collection_list = [
    'users',
    'reservations',
    'parkings'
]

def get_collection(collection:str) -> dict:
    if collection not in collection_list:
        raise Exception("Collection do not exists")
    users_dict = parse_collection(firebase.get_collection(collection))
    return users_dict

def get_document(collection:str, uid:str) -> dict:
    if collection not in collection_list:
        raise Exception("Collection do not exists")
    user_dict = parse_document(firebase.get_document(collection, uid))
    return user_dict

def parse_collection(docs) -> dict:

    ret_dict = {}
    for doc in docs:
        ret_dict[doc.id] = parse_document(doc)
    
    return ret_dict

def parse_document(doc) -> dict:
    return doc.to_dict()

def get_address_by_latlon(lat: str, lon: str):
    location = geolocator.reverse(lat+","+lon).raw['address']
    return {"loc": location}

def get_distance_by_latlon(lat_orig, lon_orig, lat_dest, lon_des):
    return haversine((lat_orig, lon_orig), (lat_dest, lon_des), unit=Unit.METERS)