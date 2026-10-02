from database.DBConnection import connect_db

def insert_reservation(room_id, fname, lname, email, phone,
                       type_id, num_id, checkin, checkout,
                       payment_method, payment_amount):

    conn = connect_db()
    cursor = conn.cursor()

    query = """
        INSERT INTO reservation (
            room_id, firstname, lastname, email, phone,
            type_id, num_id, checkin, checkout,
            payment_method, payment_amount, status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Confirmed')
    """

    cursor.execute(query, (
        room_id, fname, lname, email, phone,
        type_id, num_id, checkin, checkout,
        payment_method, payment_amount
    ))

    conn.commit()
    conn.close()
    
def get_reservations():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            r.rev_id AS id,
            r.room_id,
            CONCAT(r.firstname, ' ', r.lastname) AS fullname,
            rm.room_number,
            rm.category,
            r.checkin,
            r.checkout,
            r.payment_amount AS price,
            r.status
        FROM reservation r
        JOIN room rm ON r.room_id = rm.room_id
        ORDER BY r.rev_id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def update_reservation_status(res_id, status):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE reservation SET status=%s WHERE rev_id=%s",
        (status, res_id)
    )

    conn.commit()
    cursor.close()
    conn.close()
    
def update_room_available(room_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE room SET status='Available' WHERE room_id=%s",
        (room_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()
    
def update_room_occupied(room_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE room SET status='Occupied' WHERE room_id=%s",
        (room_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()
    
def update_reservation_room(res_id, new_room_id, new_amount):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT room_id FROM reservation WHERE rev_id = %s", (res_id,))
    old_room = cursor.fetchone()

    if not old_room:
        return

    old_room_id = old_room[0]

    cursor.execute("""
        UPDATE reservation 
        SET room_id=%s, payment_amount=%s 
        WHERE rev_id=%s
    """, (new_room_id, new_amount, res_id))

    cursor.execute("UPDATE room SET status='Available' WHERE room_id=%s", (old_room_id,))
    cursor.execute("UPDATE room SET status='Occupied' WHERE room_id=%s", (new_room_id,))

    conn.commit()
    conn.close()
    
def get_total_revenue():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT IFNULL(SUM(payment_amount), 0)
        FROM reservation
        WHERE status IN ('Checked-in', 'Checked-out')
    """)

    total = cursor.fetchone()[0]
    conn.close()

    return total

def get_reservation_count_by_status(status):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) 
        FROM reservation 
        WHERE LOWER(status) = LOWER(%s)
    """, (status,))

    total = cursor.fetchone()[0]
    conn.close()
    return total