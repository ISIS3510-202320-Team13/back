from controller import controller
from utils import request_objects as r
from utils import tags
from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.responses import FileResponse 

import api_keys as keys

api_keys = keys.api_keys

api_key_header = APIKeyHeader(name="X-API-Key")

app = FastAPI(
    title="ParkEz Back",
    summary="I have no knowledge of myself as I am, but merely as I appear to myself. -Kant",
    version="0.0.1",
    openapi_tags=tags.info,
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    )

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=401,
        detail="Invalid or missing API Key",
    )

@app.get("/")
def read_root(api_key: str = Security(get_api_key)):
    routes = {
        "Available routes": {
            "Users":{
                "user_by_uid": "/users/{uid}",
            },
            "Parkings":{
                "parkings_all": "/parkings/all",
                "parkings_by_latlon": "/parkings/near/bylatlon/{lat}/{lon}", 
            },
            "Reservations":{
                "reservations_all": "/reservations/all", 
            },
            "Utils":{
                "get_raw_collection": "/raw/collection/{collection}",
                "get_raw_document": "/raw/document/{document}/{uid}",
                "get_raw_filtered_documents":"/raw/filtered/documents/{collection}/{atribute}/{comparison}/{value}",
                "address_by_latlon": "/address/bylatlon/{lat}/{lon}",
            },
            }
        }
    return routes
# ------------------------------------ Users ------------------------------------
@app.post("/users", tags=["Users"])
async def post_reservation(user: r.Usuarios, api_key: str = Security(get_api_key)):
    """
    This function will allow you to create and store a new user in the database

    Parameters
    ----------
    Body : (JSON) It's a JSON with the atributes of a user. 

    """
    try:
        controller.create_user(user.model_dump())
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Looks like something went wrong with post at 'users' --- {e}")
    return {}

@app.put("/users", tags=["Users"])
async def put_reservation(user: r.Usuarios_update, api_key: str = Security(get_api_key)):
    """
    This function will allow you to update an user in the database

    Parameters
    ----------
    Body : (JSON) It's a JSON with the atributes of a user. 

    """
    try:
        controller.update_user(user.model_dump())
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Looks like something went wrong with post at 'users' --- {e}")
    return {}

@app.get("/users/{uid}", tags=["Users"])
async def get_user_by_uid(uid: str, api_key: str = Security(get_api_key)):
    """
    This function will allow you get an specific user stored in the database

    Parameters
    ----------
    uid : (str) It's the ID of the user in the DB
 
    Returns
    -------
    JSON
        The information of an user

    """
    try:
        response = controller.get_user_by_uid(uid)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Looks like something went wrong with '/users/{uid}' --- {e}")
    return response

# ------------------------------------ Reservations ------------------------------------
@app.post("/reservations", tags=["Reservations"])
async def post_reservation(reservation: r.Reservation, api_key: str = Security(get_api_key)):
    """
    This function will allow you to create and store a new reservation in the database

    Parameters
    ----------
    Body : (JSON) It's a JSON with the atributes of a reservation. 

    """
    try:
        controller.create_reservation(reservation.model_dump())
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Looks like something went wrong with post at 'reservations' --- {e}")
    return {}

@app.put("/reservations/{uid}", tags=["Reservations"])
async def put_reservation(uid: str, reservation: r.Reservation_update, api_key: str = Security(get_api_key)):
    """
    This function will allow you to update a reservation in the database

    Parameters
    ----------
    Body : (JSON) It's a JSON with the atributes of a reservation. 

    """
    try:
        controller.update_reservation(uid, reservation.model_dump())
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Looks like something went wrong with post at 'reservations' --- {e}")
    return {}

@app.get("/reservations/all", tags=["Reservations"])
async def get_reservations(api_key: str = Security(get_api_key)):
    """
    This function will allow you get a complete collection of reservations in the database
 
    Returns
    -------
    JSON
        The list of reservations

    """
    return controller.get_all_reservations()

@app.get("/reservations/confirmation/{uid}", tags=["Reservations"])
async def get_reservations(uid: str):
    """
    This function will allow you get a complete collection of reservations in the database
 
    Returns
    -------
    JSON
        The list of reservations

    """
    controller.update_reservation(uid,{"status": "Active"})
    return FileResponse('index.html')
# ------------------------------------ Parkings ------------------------------------
@app.post("/parkings", tags=["Parkings"])
async def post_parking(parking: r.Parking, api_key: str = Security(get_api_key)):
    """
    This function will allow you to create and store a new parking in the database

    Parameters
    ----------
    Body : (JSON) It's a JSON with the atributes of a parking. 

    """
    try:
        controller.create_parking(parking.model_dump())
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Looks like something went wrong with post at 'parkings' --- {e}")
    return {}

@app.put("/parkings", tags=["Parkings"])
async def put_parking(parking: r.Parking_update, api_key: str = Security(get_api_key)):
    """
    This function will allow you to update a parking in the database

    Parameters
    ----------
    Body : (JSON) It's a JSON with the atributes of a parking. 

    """
    try:
        controller.update_parking(parking.model_dump())
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Looks like something went wrong with post at 'parkings' --- {e}")
    return {}

@app.get("/parkings/all", tags=["Parkings"])
async def get_parkings(api_key: str = Security(get_api_key)):
    """
    This function will allow you get a complete collection of parkings in the database
 
    Returns
    -------
    JSON
        The list of parkings

    """
    return controller.get_all_parkings()

@app.get("/parkings/near/bylatlon/{lat}/{lon}", tags=["Parkings"])
async def get_parkings_bylatlon(lat: float, lon: float, api_key: str = Security(get_api_key)):
    """
    This function will allow you to get the parking lots in a radious of 500m of a location

    Parameters
    ----------
    lat : (str) It's the latitude of the location. \n
    lon : (str) It's the longitude of the location.
 
    Returns
    -------
    JSON
        The list of parkings

    """
    return controller.get_parkings_by_latlon(lat, lon)

# ------------------------------------ Utils ------------------------------------
@app.get("/confirmation/{uid}/", tags=["Utils"])
async def send_confirmation_email(uid: str, api_key: str = Security(get_api_key), status_code=200):
    """
    This function will allow you get a complete collection as is stored in the database

    Parameters
    ----------
    collection : (str) Must be an existent collection of the DB.
 
    Returns
    -------
    JSON
        The raw list of documents

    """
    try:
        controller.send_email_comfirmation(uid)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Looks like something went wrong with'/raw/collection/{uid}' --- {e}")
    return {'response':'ok'}

@app.get("/raw/collection/{collection}", tags=["Utils"])
async def get_raw_collection(collection: str, api_key: str = Security(get_api_key)):
    """
    This function will allow you get a complete collection as is stored in the database

    Parameters
    ----------
    collection : (str) Must be an existent collection of the DB.
 
    Returns
    -------
    JSON
        The raw list of documents

    """
    try:
        response = controller.get_raw_collection(collection)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Looks like something went wrong with'/raw/collection/{collection}' --- {e}")
    return response

@app.get("/raw/document/{collection}/{uid}", tags=["Utils"])
async def get_raw_document(collection: str, uid: str, api_key: str = Security(get_api_key)):
    """
    This function will allow you get a document as is stored in the database

    Parameters
    ----------
    collection : (str) Must be an existent collection of the DB. \n
    uid : (str) It's id of the document at the DB
 
    Returns
    -------
    JSON
        The raw document

    """
    try:
        response = controller.get_raw_document(collection, uid)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Looks like something went wrong with '/raw/document/{collection}' --- {e}")
    return response

@app.get("/raw/filtered/documents/{collection}/{atribute}/{comparison}/{value}", tags=["Utils"])
async def get_raw_filtered_documents(collection:str, atribute:str, comparison:str, value:str, type:str="str", format:str=None, api_key: str = Security(get_api_key)):
    """
    This function will allow you to make queries to the database but filtering the documents by one value

    Parameters
    ----------
    collection : (str) Must be an existent collection of the DB. \n
    atribute : (str) It's the atribute which will filter the documents by value i.e. price. \n
    comparison : (str) The kind of comparison, must be equal or different. \n
    value : (float/bool/str/int) The value that will be compared to. \n
    -- Query params -- \n
    type : (str) Must specify the kind of value, should be str, int, bool or float i.e. /route?type=bool . \n
    format : (float) Speficy if the documents format. Available: Reservations
 
    Returns
    -------
    JSON
        The filtered documents

    """
    return controller.get_custom_query(collection, atribute, comparison, value, type, format)

@app.get("/address/bylatlon/{lat}/{lon}", tags=["Utils"])
async def get_address_bylatlon(lat: str, lon: str, api_key: str = Security(get_api_key)):
    """
    This function will allow you get an address near to a location based on it's coodinates

    Parameters
    ----------
    lat : (str) It's the latitude of the location. \n
    lon : (str) It's the longitude of the location.

    Returns
    -------
    JSON
        The address

    """
    return controller.get_address_by_latlon(lat, lon)

@app.get("/stats/all", tags=["Utils"])
async def get_statistics(api_key: str = Security(get_api_key)):
    """
    This function will allow you get an address near to a location based on it's coodinates

    Parameters
    ----------
    lat : (str) It's the latitude of the location. \n
    lon : (str) It's the longitude of the location.

    Returns
    -------
    JSON
        The address

    """
    return controller.get_stats()