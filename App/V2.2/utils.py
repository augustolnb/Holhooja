import mariadb
from Models.users_model import User

def connect_to_database():
    try:
        conn = mariadb.connect(
        host="localhost",
        user="augusto",
        password="1234",
        database="test"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_user_by_id(user_id):
    conn = connect_to_database()
    if not conn:
        return None

    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash FROM user WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()

    conn.close()

    return User(user_data[0], user_data[1], user_data[2]) if user_data else None

def criar_user(nome, matricula, email, curso, bcrypt):
    
    try:
        conn = connect_to_database()

        if not conn:
            return False
        
        # tipo >> "aluno" is 0 and "teacher" is 1 and "admin" is 2
        # status >> "waiting" is 0 and "active" is 1 and "desactive" is 2
        # ADICIONAR DATA DE APROVAÇÃO DO USUARIO 
        
        hashed_password = bcrypt.generate_password_hash("12341234")
        tipo = 0 
        status = 0
        
        user = User(nome, matricula, email, curso, hashed_password)

        sql = "INSERT INTO user (nome, matricula, password, email, curso, tipo, status) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, (nome, int(matricula), hashed_password, email, curso, tipo, status))
        print("teste3")

        conn.commit()
        return user

    except mariadb.Error as e:
        print(f"Error: {e}")
        return "Error occurred during registration.\n Dados duplicados"

    finally:
        if conn:
            conn.close()  # Close the connection


def get_user_by_username(username):
    conn = connect_to_database()
    if not conn:
        return None

    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password_hash FROM user WHERE username = ?", (username,))
    user_data = cursor.fetchone()

    conn.close()

    return User(user_data[0], user_data[1], user_data[2]) if user_data else None
