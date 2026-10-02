from database.DBConnection import connect_db

def insert_room(roomnumber, floornumber, category, status, price, capacity):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
        INSERT INTO room (room_number, room_floor, category, status, price, capacity)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (roomnumber, floornumber, category, status, price, capacity))
    conn.commit()
    conn.close()
    
def get_all_room():
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT room_number, room_floor, category, capacity, price, status FROM room"
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()

    return data

def get_room_by_number(room_number):
    """Fetch a single room by room_number"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT room_number, room_floor, category, status, price, capacity FROM room WHERE room_number=%s", 
                   (room_number,))
    data = cursor.fetchone()
    conn.close()
    return data


def update_room(original_room_number, new_room_number, floor, category, status, price, capacity):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM room WHERE room_number=%s AND room_number != %s", 
                   (new_room_number, original_room_number))
    if cursor.fetchone():
        conn.close()
        raise Exception("Room number already exists!")
    
    cursor.execute("""
        UPDATE room
        SET room_number=%s, room_floor=%s, category=%s, status=%s, price=%s, capacity=%s
        WHERE room_number=%s
    """, (new_room_number, floor, category, status, price, capacity, original_room_number))
    conn.commit()
    conn.close()


def delete_room(room_number):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM room WHERE room_number=%s", (room_number,))
    conn.commit()
    conn.close()

def get_available_rooms(checkin, checkout):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
        SELECT r.room_id, r.room_number, r.category, r.capacity, r.price
        FROM room r
        WHERE r.status = 'Available'
        AND NOT EXISTS (
            SELECT 1 FROM reservation res
            WHERE res.room_id = r.room_id
            AND res.status IN ('Confirmed', 'Checked-in')
            AND (
                res.checkin < %s AND res.checkout > %s
            )
        )
    """

    cursor.execute(query, (checkout, checkin))
    data = cursor.fetchall()
    conn.close()

    return data

def update_room_status(room_id, status):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE room SET status=%s WHERE room_id=%s", (status, room_id))

    conn.commit()
    conn.close()
    
def get_total_rooms():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM room")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def get_available_rooms_count():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM room WHERE status='Available'")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def get_occupied_rooms_count():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM room WHERE status='Occupied'")
    total = cursor.fetchone()[0]
    conn.close()
    return total

def get_room_count_by_category(category):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM room WHERE category=%s",
        (category,)
    )

    total = cursor.fetchone()[0]
    conn.close()
    return total