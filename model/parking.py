import uuid as gen

class Parking:
    def __init__(self, availabilityCars, availabilityMotorcycle, coordinates, direccion, price, rating, uid=str(gen.uuid4())):
        self.uid = uid
        self.availabilityCars = availabilityCars
        self.availabilityMotorcycle = availabilityMotorcycle
        self.coordinates = coordinates
        self.direccion = direccion
        self.price = price
        self.rating = rating

    def __str__(self):
        return f"uid: {self.uid} availabilityCars: {self.availabilityCars} availabilityMotorcycle: {self.availabilityMotorcycle} coordinates: {self.coordinates} direccion:{self.direccion} price:{self.price} rating:{self.rating}"

    def to_dict(self):
        ret = { 
            "availabilityCars":self.availabilityCars,
            "availabilityMotorcycle":self.availabilityCars,
            "coordinates":self.coordinates,
            "direccion":self.direccion,
            "price":self.price,
            "rating":self.rating,
            "uid":self.uid
        }
        return ret
    