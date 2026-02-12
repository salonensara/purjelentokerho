import db

def add_reservation(item_id, begin_date, end_date, info, user_id):
    sql = """INSERT INTO reservations (item_id, begin_date, end_date, info, user_id)
            VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [item_id, begin_date, end_date, info, user_id])

def get_reservations(item_id):
    sql = """SELECT reservations.id, reservations.begin_date, reservations.end_date,
            reservations.info, users.id user_id, users.username
            FROM reservations, users
            WHERE reservations.item_id = ? AND reservations.user_id = users.id
            ORDER BY reservations.id DESC"""
    return db.query(sql, [item_id])

def add_item(glider_type, callsign, compsign, glider_class, options, user_id):
    sql = """INSERT INTO items (glider_type, callsign, compsign,
            glider_class, options, user_id) VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [glider_type, callsign, compsign, glider_class, options, user_id])

def get_items():
    sql = """SELECT id, glider_type, callsign, compsign,
             glider_class, options FROM items ORDER BY id DESC"""
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT
            items.id,
            items.glider_type, items.callsign,
            items.compsign, items.glider_class,
            items.options, users.username,
            users.id user_id
            FROM items, users
            WHERE items.user_id = users.id
            AND items.id = ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, glider_type, callsign, compsign, glider_class, options):
    sql = """UPDATE items SET glider_type = ?,
                    callsign = ?,
                    compsign = ?,
                    glider_class = ?,
                    options = ?
            WHERE   id = ?"""
    db.execute(sql, [glider_type, callsign, compsign, glider_class, options, item_id])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])


def search_items(query):
    sql = """SELECT id, glider_type, callsign, compsign, glider_class, options
            FROM items
            WHERE glider_type LIKE ? OR callsign LIKE ?
            ORDER BY id DESC"""
    
    search_term = "%" + (query or "") + "%"
    return db.query(sql, [search_term, search_term])