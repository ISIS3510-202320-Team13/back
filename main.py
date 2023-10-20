from controller import controller
from fastapi import FastAPI, HTTPException

app = FastAPI()
@app.get("/")
def read_root():
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
# ------------------ Users ------------------
@app.get("/users/{uid}")
def get_user_by_uid(uid: str):
    try:
        response = controller.get_user_by_uid(uid)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Looks like something went wrong with '/users/{uid}' --- {e}")
    return response

# ------------------ Reservations ------------------
@app.get("/reservations/all")
def get_reservations():
    return controller.get_all_reservations()

# ------------------ Parkings ------------------
@app.get("/parkings/all")
def get_parkings():
    return controller.get_all_parkings()

@app.get("/parkings/near/bylatlon/{lat}/{lon}")
def get_parkings_bylatlon(lat: float, lon: float):
    return controller.get_parkings_by_latlon(lat, lon)

# ------------------ Utils ------------------
@app.get("/raw/collection/{collection}")
def get_raw_collection(collection: str):
    try:
        response = controller.get_raw_collection(collection)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Looks like something went wrong with'/raw/collection/{collection}' --- {e}")
    return response

@app.get("/raw/document/{collection}/{uid}")
def get_raw_document(collection: str, uid: str):
    try:
        response = controller.get_raw_document(collection, uid)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Looks like something went wrong with '/raw/document/{collection}' --- {e}")
    return response

@app.get("/raw/filtered/documents/{collection}/{atribute}/{comparison}/{value}")
def get_raw_filtered_documents(collection:str, atribute:str, comparison:str, value:str, type:str="str"):
    return controller.get_custom_query(collection, atribute, comparison, value, type)

@app.get("/address/bylatlon/{lat}/{lon}")
def get_address_bylatlon(lat: str, lon: str):
    return controller.get_address_by_latlon(lat, lon)