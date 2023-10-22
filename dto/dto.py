
def dto_user(raw_user, raw_reservations) -> dict:
    raw_user.pop('Reservations')
    raw_user['reservations'] = raw_reservations
    return raw_user

def dto_reservation(raw_reservation:dict, raw_parking:dict, user_includes:bool, user:dict=None) -> dict:
    
    if not user_includes:
        raw_reservation.pop('user')  
    else:
        raw_reservation["user"] = user  
        
    raw_reservation["parking"] = raw_parking

    return raw_reservation