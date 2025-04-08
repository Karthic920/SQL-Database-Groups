import database

MENU_PROMPT = """
-- Coffee Bean App --

Please choose one of these options:

1) Add a new bean.
2) See all beans.
3) Find a bean by name.
4) See which preparation method is best for a bean.
5) Select bean rating range.
6) Delete bean.
7) Exit.

Your selection:"""


def menu():
    connection = database.connect()
    database.create_tables(connection)

    while (user_input := input(MENU_PROMPT)) != "7":
        if user_input == "1":
            prompt_add_new_bean(connection)

        elif  user_input == "2":
            prompt_see_all_beans(connection)

        elif  user_input == "3":
            prompt_find_bean(connection)

        elif  user_input == "4":
            prompt_find_best_method(connection)

        elif  user_input == "5":
            prompt_bean_range(connection)

        elif  user_input == "6":
            prompt_delete_bean(connection)

        else:
            print("Invalid input, please try again!")

def prompt_add_new_bean(connection):
    name = input("Enter bean name: ")
    method = input("Enter how you've prepared it: ")
    rating = int(input("Enter your rating score (0-100): "))

    database.add_bean(connection, name, method, rating)

def prompt_see_all_beans(connection):
    beans = database.get_all_beans(connection)

    for bean in beans:
        print(f"{bean[1]} ({bean[2]}) - {bean[3]}/100")

def prompt_find_bean(connection):
    name = input("Enter bean name to find: ")
    beans = database.get_beans_by_name(connection, name)

    for bean in beans:
        print(f"{bean[1]} ({bean[2]}) - {bean[3]}/100")

def prompt_find_best_method(connection):
    name = input("Enter bean name to find: ")
    best_method = database.get_best_perparation_for_bean(connection, name)

    print(f"The best preparation method for {name} is: {best_method[2]}")

def prompt_bean_range(connection):
    range1 = int(input("What is the lowest rating of bean you would like?"))
    range2 = int(input("What is the highest rating of bean you would like?"))
    beans = database.get_bean_range(connection, range1, range2)

    print("\n")

    for bean in beans:
        print(f"{bean[1]} ({bean[2]}) - {bean[3]}/100")

def prompt_delete_bean(connection):
    user_input = input("""Please choose one of these options:

    1) Delete by name.
    2) Delete by ID.

    Your selection:""")

    if user_input == "1":
        name = input("Enter bean name to delete: ")
        database.delete_bean_by_name(connection, name)

    elif user_input == "2":
        ID = int(input("Enter bean ID to delete: "))
        database.delete_bean_by_id(connection, ID)


menu()
