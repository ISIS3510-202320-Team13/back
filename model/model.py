from model import firebase_connection as firebase

import uuid
from haversine import haversine, Unit
from geopy.geocoders import Nominatim
from google.cloud.firestore import GeoPoint

geolocator = Nominatim(user_agent="ParkEz-API")

collection_list = [
    'users',
    'reservations',
    'parkings'
]

# ------------------------------------ CRUD METHODS  ------------------------------------

def add_document(collection:str, new_document:dict):
    if collection == 'parkings':
        new_document = validate_parkings(new_document)
        print(new_document)
    firebase.add_document(collection, new_document)
    return None

def get_collection(collection:str) -> dict:
    if collection not in collection_list:
        raise Exception("Collection do not exists")
    users_dict = parse_collection(firebase.get_collection(collection))
    return users_dict

def get_document(collection:str, uid:str) -> dict:
    if collection not in collection_list:
        raise Exception("Collection do not exists")
    user_dict = parse_document(firebase.get_document(collection, uid))
    if user_dict is None:
        raise Exception("Document do not exists")
    return user_dict

def get_documents_filtered(collection:str, atribute:str, comparison:str, value:str, type:str):
    if collection not in collection_list:
        raise Exception("Collection do not exists")
    
    if comparison == "equals":
        comparison = "=="
    elif comparison == "different":
        comparison = "!="

    if type == "int":
        value = int(value)
    elif type == "float":
        value = float(value)
    elif type == "bool":
        value = bool(value)

    user_dict = parse_collection(firebase.get_documents_filtered(collection, atribute, comparison, value))
    if user_dict is None:
        raise Exception(f"There is no documents with {atribute} {comparison} {value}")
    return user_dict

# ------------------------------------ Parse ------------------------------------

def parse_collection(docs) -> dict:

    ret_dict = {}
    for doc in docs:
        ret_dict[doc.id] = parse_document(doc)
    
    return ret_dict

def parse_document(doc) -> dict:
    return doc.to_dict()

# ------------------------------------ Non persistence ------------------------------------

def get_address_by_latlon(lat: str, lon: str):
    location = geolocator.reverse(lat+","+lon).raw['address']
    return {"loc": location}

def get_distance_by_latlon(lat_orig, lon_orig, lat_dest, lon_des):
    return haversine((lat_orig, lon_orig), (lat_dest, lon_des), unit=Unit.METERS)

# ------------------------------------ Validation methods  ------------------------------------

def validate_parkings(parking:dict):

    location = geolocator.geocode(parking['direccion'])
    calculated_latitude = location.latitude 
    calculated_longitude = location.longitude

    latitude = parking['coordinates']["latitude"]
    longitude = parking['coordinates']["longitude"]

    dist = get_distance_by_latlon(calculated_latitude, calculated_longitude, latitude, longitude)

    if dist > 300:
        raise Exception("The address is away from the coordinates")
    
    if ((parking['availabilityCars'] < 0) or (parking['availabilityMotorcycle'] < 0) or (parking['price'] < 0) or (parking['rating'] < 0.0)):
        raise Exception("Numbers should not be negative")
    
    if parking['name'] == "":
        raise Exception("Name should not be an empty string")

    location = GeoPoint(latitude, longitude)

    parking['coordinates'] = location
    
    if 'uid' not in parking:
        parking['uid'] = str(uuid.uuid4())

    return parking
