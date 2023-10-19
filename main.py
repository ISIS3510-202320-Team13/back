from controller import controller
from fastapi import FastAPI

app = FastAPI()
@app.get("/")
def read_root():
    return {"Available routes": {"userInfoByUID": "/users/{uid}", "address_bylatlon": "/address/bylatlon/{lat}/{lon}", 
                                 "reservations": "/reservations/all", "parkings": "/parkings/all", "parkings_bylatlon": "/parkings/near/bylatlon/{lat}/{lon}"}}

@app.get("/users/{uid}")
def get_user_by_uid(uid: str):
    return controller.get_user_by_uid(uid)

@app.get("/address/bylatlon/{lat}/{lon}")
def get_address_bylatlon(lat: str, lon: str):
    return controller.get_address_by_latlon(lat, lon)

@app.get("/reservations/all")
def get_reservations():
    return controller.get_all_reservations()

@app.get("/parkings/all")
def get_parkings():
    return controller.get_all_parkings()

@app.get("/parkings/near/bylatlon/{lat}/{lon}")
def get_parkings_bylatlon(lat: float, lon: float):
    return controller.get_parkings_by_latlon(lat, lon)
    