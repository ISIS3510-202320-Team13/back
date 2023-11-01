from pydantic import BaseModel

class Parking(BaseModel):
    coordinates: dict
    direccion: str
    availabilityCars: int
    availabilityMotorcycle: int
    price: int
    rating: float
    name:str
    uid:str | None = None

class Reservation(BaseModel):
    cost: int
    entry_time: str
    exit_time: str
    parking: str
    status: str
    user: str
    uid:str | None = None

class Usuarios(BaseModel):
    reservations: list
    email: str
    name: str
    picture: str
    uid:str | None = None

class Parking_update(BaseModel):
    coordinates: dict | None = None
    direccion: str | None = None
    availabilityCars: int | None = None
    availabilityMotorcycle: int | None = None
    price: int | None = None
    rating: float | None = None
    name:str | None = None
    uid:str

class Reservation_update(BaseModel):
    cost: int | None = None
    entry_time: str | None = None
    exit_time: str | None = None
    parking: str | None = None
    status: str | None = None
    user: str | None = None
    uid:str

class Usuarios_update(BaseModel):
    reservations: list | None = None
    email: str | None = None
    name: str | None = None
    picture: str | None = None
    uid:str