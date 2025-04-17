import database, csv
MENU_PROMPT = """
-- Movie Finder App --

Please choose one of these options:

1) Add a new movie.
2) See all movies.
3) Find a movie by name.
4) See which year the movie was made
5) Select movie rating range.
6) Find movie by lead actor or director
7) Find movies by series
8) Delete movie
9) Export movies to CSV
10) Import movies from CSV
11) Show top 5 rated movies
12) Clear your table :)
13) Exit

Your selection:"""

def pause():
    input("Press enter to continue: ")
def wipe_movies():
    open('data.db', 'w').close()


def menu():
    connection = database.connect()
    database.create_tables(connection)

    while (user_input := input(MENU_PROMPT)) != "13":
        if user_input == "1":
            prompt_add_new_movie(connection)
            pause()

        elif user_input == "2":
            prompt_see_all_movies(connection)
            pause()

        elif  user_input == "3":
            prompt_find_movie(connection)
            pause()

        elif  user_input == "4":
            prompt_find_movie_year(connection)
            pause()

        elif  user_input == "5":
            prompt_movie_range(connection)
            pause()

        elif  user_input == "6":
            prompt_find_movie_actor_or_director(connection)
            pause()

        elif user_input == "7":
            prompt_find_movie_series(connection)
            pause()

        elif user_input == "8":
            prompt_delete_movie(connection)
            pause()
        elif user_input == "9":
            prompt_export_to_csv(connection)
            pause()
        elif user_input == "10":
            prompt_import_from_csv(connection)
            pause()
        elif user_input == "11":
            prompt_get_top_movies(connection)
            pause()
        elif user_input == "12":
            prompt_clear_table(connection)
            pause()
        else:
            print("Invalid input, please try again!")

def prompt_add_new_movie(connection):
    while True:
        name = input("Enter movie name: ")
        year = input("Enter the year it was published: ")
        actor = input("Enter lead actor: ")
        director = input("Enter director: ")
        rating = input("Enter your rating score (0-100): ")
        if rating.isdigit() and year.isdigit():
            year = int(year)
            rating = int(rating)

            if not (0 <= rating <= 100):
                print("Rating must be between 0 and 100.")
                continue
            break
        else:
            print("Make sure year and rating are integer values!")


    database.add_movie(connection, name, year, actor, director, rating)

def prompt_see_all_movies(connection):
    movies = database.get_all_movies(connection)

    for movie in movies:
        print(f"{movie[1]} ({movie[2]}), actor: {movie[3]}, director: {movie[4]} - {movie[5]}/100")

def prompt_find_movie(connection):
    name = input("Enter movie name to find: ")
    movies = database.get_movies_by_name(connection, name)

    if not movies:
        print(f"No movie found with the name '{name}'.")
        add_movie = input("Would you like to add it to the database? (y/n): ").lower()
        if add_movie == "y" or add_movie == "Y":
            prompt_add_new_movie(connection)
        return

    for movie in movies:
        print(f"{movie[1]} ({movie[2]}), actor: {movie[3]}, director: {movie[4]} - {movie[5]}/100")

def prompt_find_movie_year(connection):
    name = input("Enter movie name to find: ")
    year = database.get_movie_year(connection, name)

    if year is None:
        print(f"No movie found with the name '{name}'.")

    print(f"The year {name} was published is: {year[2]}")

def prompt_movie_range(connection):
    range1 = int(input("What is the lowest rating of movie you would like?"))
    range2 = int(input("What is the highest rating of movie you would like?"))
    movies = database.get_movie_range(connection, range1, range2)

    print("\n")

    for movie in movies:
        print(f"{movie[1]} ({movie[2]}), actor: {movie[3]}, director: {movie[4]} - {movie[5]}/100")

def prompt_find_movie_actor_or_director(connection):
    user_input = input("""Please choose one of these options:

        1) Find by Actor.
        2) Find by Director.

        Your selection:""")
    while True:
        if user_input == "1":
            actor_name = input("What is the lead actors name?: ")
            movies = database.get_movie_by_actor(connection, actor_name)

            if not movies:
                print(f"No movies found for {actor_name}.")

            for movie in movies:
                print(f"{movie[1]} ({movie[2]}), actor: {movie[3]}, director: {movie[4]} - {movie[5]}/100")
            break
        elif user_input == "2":
            director_name = input("What is the directors name?: ")
            movies = database.get_movie_by_director(connection, director_name)

            if not movies:
                print(f"No movies found for {director_name}.")

            for movie in movies:
                print(f"{movie[1]} ({movie[2]}), actor: {movie[3]}, director: {movie[4]} - {movie[5]}/100")
            break
        else:
            print("Bruh enter an actual option")
            return

def prompt_find_movie_series(connection):
    user_input = input("What is the name of the movie franchise?\n(EX: 'Hunger games 1, Hunger games 2, Hunger games 3'\nThe Movie franchise name is: Hunger games):")
    print("\n\n")

    movies = database.get_movie_series(connection, user_input)

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

def prompt_export_to_csv(connection):
    database.export_movies_to_csv(connection)
    print("Movies exported to 'movies_export.csv'")

def prompt_import_from_csv(connection):
    filename = input("Enter the filename to import from: ")
    try:
        database.import_movies_from_csv(connection, filename)
        print(f"Movies imported successfully from '{filename}'.")
    except FileNotFoundError:
        print(f"File '{filename}' not found. Make sure it's in the same folder.")


def prompt_get_top_movies(connection):
    movies = database.get_top_movies(connection)
    print("Top 5 movies are:\n")

    for movie in movies:
        print(f"{movie[1]} ({movie[2]}), actor: {movie[3]}, director: {movie[4]} - {movie[5]}/100")
def prompt_clear_table(connection):
    database.clear_table(connection)
    print("Movies successfully cleared :))))")

menu()
