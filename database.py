
import sqlite3, csv


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
WHERE actor LIKE ?
ORDER BY rating DESC
"""

GET_MOVIE_BY_DIRECTOR = """
SELECT * FROM movies
WHERE director LIKE ?
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

GET_TOP_MOVIES = """
SELECT * FROM movies
ORDER BY rating DESC
LIMIT 5;"""


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
        actor = f"%{actor}%"
        return connection.execute(GET_MOVIE_BY_ACTOR, (actor,)).fetchall()

def get_movie_by_director(connection, director):
    with connection:
        director = f"%{director}%"
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

def export_movies_to_csv(connection, filename='movies_export.csv'):
    movies = get_all_movies(connection)
    
    # Export movies to CSV file, with UTF-8 encoding
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Year", "Actor", "Director", "Rating"])
        writer.writerows(movies)

def import_movies_from_csv(connection, filename):
    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            try:
                # Assuming CSV has the same structure: ID, Name, Year, Actor, Director, Rating
                name, year, actor, director, rating = row[1], int(row[2]), row[3], row[4], int(row[5])
                add_movie(connection, name, year, actor, director, rating)
                
            except (IndexError) as e:
                print(f"Skipping row due to error: {e}")  
            except (ValueError) as e:
                print(f"Skipping row due to error: {e}")

def get_top_movies(connection):
    with connection:
        return connection.execute(GET_TOP_MOVIES).fetchall()
