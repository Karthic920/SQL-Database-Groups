import sqlite3

print("shyssy baka")


CREATE_BEANS_TABLE = "CREATE TABLE IF NOT EXISTS beans (id INTEGER PRIMARY KEY, name TEXT, method TEXT, rating INTEGER);"

INSERT_BEAN = "INSERT INTO beans(name, method, rating) VALUES (?, ?, ?);"

GET_ALL_BEANS = "SELECT * FROM beans;"
GET_BEANS_BY_NAME = "SELECT * FROM beans WHERE name = ?;"
GET_BEST_PREPARATION_FOR_BEAN = """
SELECT * FROM beans
WHERE name = ?
ORBER BY rating DESC
LIMIT 1;"""

GET_BEAN_RANGE = "SELECT * FROM beans WHERE rating >= ? AND ? >= rating"

DELETE_BEAN_BY_NAME = """
DELETE FROM beans
WHERE name = ? """

DELETE_BEAN_BY_ID = """
DELETE FROM beans
WHERE id = ?  """


def connect():
    return sqlite3.connect("data.db")


def create_tables(connection):
    with connection:
        connection.execute(CREATE_BEANS_TABLE)


def add_bean(connection, name, method, rating):
    with connection:
        connection.execute(INSERT_BEAN, (name, method, rating))


def get_all_beans(connection):
    with connection:
        return connection.execute(GET_ALL_BEANS).fetchall()

def get_beans_by_name(connection, name):
    with connection:
        return connection.execute(GET_BEANS_BY_NAME, (name,)).fetchall()

def get_best_preparation_for_bean(connection, name):
    with connection:
        return connection.execute(GET_BEST_PREPARATION_FOR_BEAN, (name,)).fetchone()

def get_bean_range(connection, range1, range2):
    with connection:
        return connection.execute(GET_BEAN_RANGE, (range1, range2)).fetchall()

def delete_bean_by_name(connection, name):
    with connection:
        connection.execute(DELETE_BEAN_BY_NAME, (name,))

def delete_bean_by_id(connection, bean_id):
    with connection:
        connection.execute(DELETE_BEAN_BY_ID, (bean_id,))
