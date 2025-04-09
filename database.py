import sqlite3


CREATE_MOVIES_TABLE = "CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, name TEXT, year INTEGER, actor TEXT, director TEXT, rating INTEGER);"

INSERT_MOVIE = "INSERT INTO movies(name, year, actor, director, rating) VALUES (?, ?, ?, ?, ?);"

GET_ALL_MOVIES = "SELECT * FROM movies;"
GET_MOVIES_BY_NAME = "SELECT * FROM movies WHERE name = ?;"
GET_MOVIE_YEAR = """
SELECT * FROM movies
WHERE name = ?
ORDER BY rating DESC
LIMIT 1;"""

GET_MOVIE_RANGE = "SELECT * FROM movies WHERE rating >= ? AND ? >= rating ORDER BY rating DESC"

GET_MOVIE_BY_ACTOR = """
SELECT * FROM movies
WHERE actor = ?
ORDER BY rating DESC
"""

GET_MOVIE_BY_DIRECTOR = """
SELECT * FROM movies
WHERE director = ?
ORDER BY rating DESC
"""

GET_MOVIE_SERIES = """
SELECT * FROM movies
WHERE name LIKE ?
ORDER BY year ASC
;"""

DELETE_MOVIE_BY_NAME = """
DELETE FROM movies
WHERE name = ? """

DELETE_MOVIE_BY_ID = """
DELETE FROM movies
WHERE id = ?  """


def connect():
    return sqlite3.connect("data.db")


def create_tables(connection):
    with connection:
        connection.execute(CREATE_MOVIES_TABLE)


def add_movie(connection, name, year, actor, director, rating):
    with connection:
        connection.execute(INSERT_MOVIE, (name, year, actor, director, rating))


def get_all_movies(connection):
    with connection:
        return connection.execute(GET_ALL_MOVIES).fetchall()

def get_movies_by_name(connection, name):
    with connection:
        return connection.execute(GET_MOVIES_BY_NAME, (name,)).fetchall()

def get_movie_year(connection, name):
    with connection:
        return connection.execute(GET_MOVIE_YEAR, (name,)).fetchone()

def get_movie_range(connection, range1, range2):
    with connection:
        return connection.execute(GET_MOVIE_RANGE, (range1, range2)).fetchall()

def get_movie_by_actor(connection, actor):
    with connection:
        return connection.execute(GET_MOVIE_BY_ACTOR, (actor,)).fetchall()

def get_movie_by_director(connection, director):
    with connection:
        return connection.execute(GET_MOVIE_BY_DIRECTOR, (director,)).fetchall()

def get_movie_series(connection, name):
    with connection:
        search_pattern = f"%{name}%"
        return connection.execute(GET_MOVIE_SERIES, (search_pattern,)).fetchall()

def delete_movie_by_name(connection, name):
    with connection:
        connection.execute(DELETE_MOVIE_BY_NAME, (name,))

def delete_movie_by_id(connection, movie_id):
    with connection:
        connection.execute(DELETE_MOVIE_BY_ID, (movie_id,))
