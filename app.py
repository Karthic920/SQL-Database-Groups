import database

MENU_PROMPT = """
-- Movie Finder App --

Please choose one of these options:

1) Add a new movie.
2) See all movies.
3) Find a movie by name.
4) See which year the movie was made
5) Select movie rating range.
6) Delete movie.
7) Exit.

Your selection:"""


def menu():
    connection = database.connect()
    database.create_tables(connection)

    while (user_input := input(MENU_PROMPT)) != "7":
        if user_input == "1":
            prompt_add_new_movie(connection)

        elif  user_input == "2":
            prompt_see_all_movies(connection)

        elif  user_input == "3":
            prompt_find_movie(connection)

        elif  user_input == "4":
            prompt_find_movie_year(connection)

        elif  user_input == "5":
            prompt_movie_range(connection)

        elif  user_input == "6":
            prompt_delete_movie(connection)

        else:
            print("Invalid input, please try again!")

def prompt_add_new_movie(connection):
    name = input("Enter movie name: ")
    year = input("Enter the year it was published: ")
    actor = input("Enter lead actor: ")
    director = input("Enter director: ")
    rating = int(input("Enter your rating score (0-100): "))

    database.add_movie(connection, name, year, actor, director, rating)

def prompt_see_all_movies(connection):
    movies = database.get_all_movies(connection)

    for movie in movies:
        print(f"{movie[1]} ({movie[2]}), actor: {movie[3]}, director: {movie[4]} - {movie[5]}/100")

def prompt_find_movie(connection):
    name = input("Enter movie name to find: ")
    movies = database.get_movies_by_name(connection, name)

    for movie in movies:
        print(f"{movie[1]} ({movie[2]}), actor: {movie[3]}, director: {movie[4]} - {movie[5]}/100")

def prompt_find_movie_year(connection):
    name = input("Enter movie name to find: ")
    year = database.get_movie_year(connection, name)

    print(f"The year {name} was published is: {year[2]}")

def prompt_movie_range(connection):
    range1 = int(input("What is the lowest rating of movie you would like?"))
    range2 = int(input("What is the highest rating of movie you would like?"))
    movies = database.get_movie_range(connection, range1, range2)

    print("\n")

    for movie in movies:
        print(f"{movie[1]} ({movie[2]}), actor: {movie[3]}, director: {movie[4]} - {movie[5]}/100")

def prompt_delete_movie(connection):
    user_input = input("""Please choose one of these options:

    1) Delete by name.
    2) Delete by ID.

    Your selection:""")

    if user_input == "1":
        name = input("Enter movie name to delete: ")
        database.delete_movie_by_name(connection, name)

    elif user_input == "2":
        ID = int(input("Enter movie ID to delete: "))
        database.delete_movie_by_id(connection, ID)


menu()
