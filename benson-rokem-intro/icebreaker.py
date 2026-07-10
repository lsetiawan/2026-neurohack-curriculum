
room_list_online = [
    'Alder Auditorium',
    'Alder Commons',
    'Alder 103',
    'Alder 105',
    'Alder 106',
    'Alder 107']
weights_online = [1, 1, 1, 1, 1, 1]
room_list_inperson = [
    'Alder Auditorium',
    'Alder Commons',
    'Alder 103',
    'Alder 105',
    'Alder 106',
    'Alder 107',
    'Alder Courtyard',
    'Coffe Table']
weights_inperson = [1, 1, 1, 1, 1, 1, 2, 2]

def get_rooms(n=5, inperson=False):
    import numpy as np
    if inperson:
        room_list = room_list_inperson
        weights = weights_inperson
    else:
        room_list = room_list_online
        weights = weights_online
    weights = np.array(weights)
    p = weights / np.sum(weights)
    sel = np.random.choice(room_list, n, replace=False, p=p)
    for (ii,room) in enumerate(sel):
        print(f"{ii+1}. {room}")
    return None
