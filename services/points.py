from services.db import add_points

def allocate_points(user_id, bottle_type, points):
    add_points(user_id, points, bottle_type)
    return True