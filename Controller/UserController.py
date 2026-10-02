import bcrypt
from database.DBConnection import connect_db

def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM user WHERE username=%s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user:
        if user['status'].lower() == "inactive":
            conn.close()
            return "inactive"

        stored_password = user['password']

        if stored_password.startswith("$2b$"):
            if bcrypt.checkpw(password.encode(), stored_password.encode()):
                conn.close()
                return user
        else:
            if password == stored_password:
                hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

                update_query = "UPDATE user SET password=%s WHERE username=%s"
                cursor.execute(update_query, (hashed, username))
                conn.commit()

                conn.close()
                return user

    conn.close()
    return None

def insert_staff(firstname, lastname, gmail, role, username, password):
    conn = connect_db()
    cursor = conn.cursor()

    check_query = "SELECT * FROM user WHERE username=%s"
    cursor.execute(check_query, (username,))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        raise Exception("Username already exists!")

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    query = """
        INSERT INTO user (firstname, lastname, gmail, role, username, password)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (firstname, lastname, gmail, role, username, hashed_password))
    conn.commit()
    conn.close()

def get_all_staff():
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT firstname, lastname, gmail, username, role, status FROM user"
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()

    return data

def get_staff_by_username(username):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT firstname, lastname, gmail, username, role, status
        FROM user
        WHERE username = %s
    """, (username,))

    data = cursor.fetchone()
    conn.close()

    return data

def update_staff(username, fname, lname, gmail, role, status):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE user
        SET firstname=%s, lastname=%s, gmail=%s, role=%s, status=%s
        WHERE username=%s
    """, (fname, lname, gmail, role, status, username))

    conn.commit()
    conn.close()
    
def get_total_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def get_active_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user WHERE status='Active'")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def get_inactive_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user WHERE status='Inactive'")
    total = cursor.fetchone()[0]
    conn.close()
    return total