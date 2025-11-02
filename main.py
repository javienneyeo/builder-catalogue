from data_handler import ApiDataHandler
from collections import defaultdict
import math

BASE_URL = "https://d30r5p5favh3z8.cloudfront.net"

def find_buildable_sets(api, username):
    user = api.get_user_by_username(username)
    all_sets = api.get_all_sets()

    buildable_sets = []  
    for s in all_sets: 
        if s.can_build(user):  
            buildable_sets.append(s.name)  

    return buildable_sets
    
def find_collaborators(api, username, set_name):
    user = api.get_user_by_username(username)
    inventory_dict = user.get_inventory_summary()
    target_set = api.get_set_by_set_name(set_name)
    set_pieces_dict = target_set.get_required_pieces_summary()
    
    missing_pieces = user.find_missing_pieces(inventory_dict, set_pieces_dict)
    if not missing_pieces:
        return []
    
    all_users = api.get_all_users()
    collaborators = []
    for u in all_users:
        if u.username == username:
            continue
        
        other_inventory = u.get_inventory_summary()

        remaining_missing_pieces = u.find_missing_pieces(other_inventory, missing_pieces)
        if len(remaining_missing_pieces) < len(missing_pieces):
            collaborators.append(u.username)
            missing_pieces = remaining_missing_pieces

    if not missing_pieces:
        return collaborators
    return []

def print_list(item_list):
    if len(item_list) > 0:
        for item in item_list:
            print(f"- {item}")
    else:
        print("No items found")

def main():
    api = ApiDataHandler(BASE_URL)
    username = "brickfan35"
    task = 2
    if task == 1:
        buildable_sets = find_buildable_sets(api, username)
        print(f"{username} can build the following sets:")
        print_list(buildable_sets)
    if task == 2:
        set_name = "tropical-island"
        collaborators = find_collaborators(api, username, set_name)
        print(f"{username} can collaborate with these users to build {set_name}")
        print_list(collaborators)

if __name__ == "__main__":
    main()
