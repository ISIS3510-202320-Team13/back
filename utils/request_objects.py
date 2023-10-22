from pydantic import BaseModel

class Parking(BaseModel):
    coordinates: dict
    direccion: str
    availabilityCars: int
    availabilityMotorcycle: int
    price: int
    rating: float