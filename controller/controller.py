from model import model 
from dto import dto as format

def get_all_parkings() -> dict:
    return model.get_collection('parkings')

def get_all_reservations() -> dict:
    reservations = model.get_collection('reservations')

    ret_dict = {}
    for reservation in reservations:
        temp_res = reservations[reservation]
        parking_details = model.get_document('parkings', temp_res["parking"])
        new_reservation = format.dto_reservation(temp_res, parking_details, False)

        ret_dict[reservation] = new_reservation 
    
    return ret_dict

def get_reservation_list(reservations:list):
    ret_dict = {}

    for reservation in reservations:
        ret_dict[reservation] = get_reservation_by_uid(reservation)
    
    return ret_dict

def get_reservation_by_uid(uid:str) -> dict:
    
    reservation = model.get_document('reservations', uid)
    parking_details = model.get_document('parkings', reservation["parking"])
    new_reservation = format.dto_reservation(reservation, parking_details, False)

    return new_reservation

def get_user_by_uid(uid:str) -> dict:

    user = model.get_document('users', uid)
    if "Reservations" in user:
        reservation_list = user['Reservations']
        reservations = get_reservation_list(reservation_list)
        new_user = format.dto_user(user, reservations)
    else:
        new_user = user
    
    return new_user

def get_parkings_by_latlon(lat: float, lon: float):
    docs = model.get_collection('parkings')
    
    
    ret = {}

    for doc in docs:
        docdic = docs[doc]

        #(float(docdic["coordinates"].latitude), float(docdic["coordinates"].longitude)
        dist = model.get_distance_by_latlon(lat, lon, float(docdic["coordinates"].latitude), float(docdic["coordinates"].longitude))
        
        t_price = docdic["price"]
        t_rate = docdic["rating"]+((-1*t_price)/100)

        if dist <= 500:
            if (rate == -1) or (rate > (t_rate)):
                rate = t_rate
                price = t_price
                choice = doc.id

            docdic["distance"] = round(dist, 2)
            docdic["choice"] = False
            ret[doc.id] = docdic
    
    temp = ret.copy()
    if choice in temp:
        p_choosed = temp.pop(choice)
        if price == p_choosed["price"]:
            p_choosed["price_match"] = True
        else:
            p_choosed["price_match"] = False
        p_choosed["choice"] = True

    ret = {"choice":p_choosed, "others":temp}

    return None
    
def get_address_by_latlon(lat: str, lon: str):
    return model.get_address_by_latlon(lat, lon)
    