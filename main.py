from data_handler import ApiDataHandler
from collections import defaultdict
import math

BASE_URL = "https://d30r5p5favh3z8.cloudfront.net"

def print_list(item_list):
    if len(item_list) > 0:
        for item in item_list:
            print(f"- {item}")
    else:
        print("No items found")

def main():
    api = ApiDataHandler(BASE_URL)
    username = "brickfan35"
    task = 1
    if task == 1:
        user = api.get_user_by_username(username)
        all_sets = api.get_all_sets()
        buildable_sets = user.find_buildable_sets(all_sets)
        print(f"{username} can build the following sets:")
        print_list(buildable_sets)
    if task == 2:
        set_name = "tropical-island"
        user = api.get_user_by_username(username)
        target_set = api.get_set_by_set_name(set_name)
        all_users = api.get_all_users()
        collaborators = user.find_collaborators(target_set, all_users)
        print(f"{username} can collaborate with these users to build {set_name}")
        print_list(collaborators)
    if task == 3:
        threshold = 0.5
        # largest_collection_of_pieces(api, username, threshold)

if __name__ == "__main__":
    main()
