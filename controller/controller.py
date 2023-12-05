from model import model
from dto import dto as format
from utils import choice, emails_sender

# ------------------------------------ Reservations ------------------------------------

def create_reservation(reservation_p:dict):
    parking = get_parking_by_uid(reservation_p['parking'])

    cost = parking['price']*reservation_p['time_to_reserve']
    reservation_p['cost'] = cost

    uid = model.add_document('reservations', reservation_p)
    user = get_raw_document('users', reservation_p['user'])

    user['Reservations'].append(uid)
    user['uid'] = reservation_p['user']
    update_user(user)

    emails_sender.send_email(user['email'],uid,parking['name'], reservation_p['entry_time'], reservation_p['time_to_reserve'], cost, user['name'])
    return None

def update_reservation(reservation_p:dict):
    model.update_document('reservations', reservation_p)
    return None

def get_all_reservations(external = None) -> dict:
    if external is None:
        reservations = model.get_collection('reservations')
    else:
        reservations = external

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

def get_reservation_by_uid(uid:str, includes_user = False) -> dict:
    
    reservation = model.get_document('reservations', uid)
    parking_details = model.get_document('parkings', reservation["parking"])
    new_reservation = format.dto_reservation(reservation, parking_details, includes_user)

    return new_reservation

# ------------------------------------ Users ------------------------------------

def create_user(user_p:dict):
    model.add_document('users', user_p)
    return None

def update_user(user_p:dict):
    model.update_document('users', user_p)
    return None

def get_user_by_uid(uid:str) -> dict:

    user = model.get_document('users', uid)

    reservations = get_custom_query('reservations', 'user', 'equals', uid, type='str' ,format='reservations')
    if reservations != {}:
        new_user = format.dto_user(user, reservations)
    else:
        new_user = user

    return new_user

# ------------------------------------ Parkings ------------------------------------

def create_parking(parking_p:dict):
    model.add_document('parkings', parking_p)
    return None

def update_parking(parking_p:dict):
    model.update_document('parkings', parking_p)
    return None

def get_all_parkings() -> dict:
    return model.get_collection('parkings')

def get_parkings_by_latlon(lat: float, lon: float):
    c = choice.Choice()

    docs = model.get_collection('parkings')

    for doc in docs:
        docdic = docs[doc]
        dist = model.get_distance_by_latlon(lat, lon, float(docdic["coordinates"].latitude), float(docdic["coordinates"].longitude))
        c.compare_to_choosed(docdic, dist, doc)

    ret = c.get_choosed()

    return ret

def get_parking_by_uid(uid:str) -> dict:
    parking = model.get_document('parkings', uid)
    return parking

# ------------------------------------ Utils ------------------------------------
def send_email_comfirmation(uid:str):
    reservation_p = get_reservation_by_uid(uid, includes_user=True)
    print(reservation_p)
    user = get_user_by_uid(reservation_p['user'])
    emails_sender.send_email(user['email'],uid,reservation_p['parking']['name'], reservation_p['entry_time'], reservation_p['time_to_reserve'], reservation_p['cost'], user['name'])

def get_raw_collection(collection: str):
    return model.get_collection(collection)

def get_raw_document(collection: str, uid:str):
    return model.get_document(collection, uid)

def get_custom_query(collection:str, atribute:str, comparison:str, value:str, type:str, format:str):
    filtered = model.get_documents_filtered(collection, atribute, comparison, value, type)

    if format == "reservations":
        filtered = get_all_reservations(filtered)

    return filtered

def get_address_by_latlon(lat: str, lon: str):
    return model.get_address_by_latlon(lat, lon)

def get_stats():
    return model.fixed_stats()