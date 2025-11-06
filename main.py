from data_handler import ApiDataHandler, ApiError
from cli_handler import CliHandler
from collections import defaultdict
import math

BASE_URL = "https://d30r5p5favh3z8.cloudfront.net"

def ask_for_valid_username(cli, api):
    while True:
        username = cli.get_input("What is your username?")
        try:
            user = api.get_user_by_username(username)
            return user
        except ApiError:
            cli.print_error("There is no such username. Try again.")

def ask_for_valid_set(cli, api, all_sets):
    setnames = [s.name for s in all_sets]
    cli.print_output("Please choose from the following sets")
    cli.print_list(all_sets)

    while True:
        name = cli.get_input("Which set would you like to build?")
        if name not in setnames:
            cli.print_error("No such set. Try again.")
            continue
        return api.get_set_by_set_name(name)

def main():
    api = ApiDataHandler(BASE_URL)
    cli = CliHandler()
    cli.print_welcome_header()

    try:
        all_users = api.get_all_users()
        all_sets = api.get_all_sets()
    except ApiError:
        cli.print_error("Unable to load data from the server.")

    user = ask_for_valid_username(cli, api)
    cli.print_hello(user.username)

    while True:
        choice = cli.print_guide(user.username)

        if choice == "1":
            cli.print_output("All users:")
            cli.print_list(all_users)

        elif choice == "2":
            cli.print_output("All sets:")
            cli.print_list(all_sets)

        elif choice == "3":
            buildable = user.find_buildable_sets(all_sets)
            cli.print_output("You can build:")
            cli.print_list(buildable)

        elif choice == "4":
            target = ask_for_valid_set(cli, api, all_sets)
            collaborators = user.find_collaborators(target, all_users)
            cli.print_output(f"These are the users you can collaborate with for {target.name}")
            cli.print_list(collaborators)

        elif choice == "5":
            user.find_buildable_sets_no_color(all_sets)

        elif choice == "6":
            target = ask_for_valid_set(cli, api, all_sets)
            missing_pieces = user.find_missing_pieces(target.required_pieces)
            cli.print_output(f"These are pieces that you need to complete {target.name}")
            cli.print_list(missing_pieces)

        elif choice == "7":
            target = ask_for_valid_set(cli, api, all_sets)
            percentage = target.buildable_percentage(user)
            cli.print_output(f"You can build {percentage}% of {target.name}")
        elif choice == "8":
            cli.print_output(f"Bye {user.username}! Hope to see you again :-)")
            break

        else:
            cli.print_error("Invalid option.")


if __name__ == "__main__":
    main()
