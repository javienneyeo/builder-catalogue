from collections import defaultdict
import math
from main import largest_collection_of_pieces  # assuming your main script is named main.py


# Step 1: Mock User class
class MockUser:
    def __init__(self, username, inventory):
        self.username = username
        self.inventory = inventory

    def get_inventory_summary(self):
        return self.inventory

    def has_piece(self, piece, required_qty):
        return self.inventory.get(piece, 0) >= required_qty

    def can_build_set(self, piece_dict):
        for piece, qty in piece_dict.items():
            if self.inventory.get(piece, 0) < qty:
                return False
        return True


# Step 2: Mock API class
class MockApi:
    def __init__(self, users):
        self.users = users

    def get_all_users(self):
        return self.users

    def get_user_by_username(self, username):
        for u in self.users:
            if u.username == username:
                return u
        raise ValueError("User not found")


# Step 3: Create larger test data
user_inventories = [
    {('3029', '4'): 8, ('3029', '8'): 6, ('3001', '1'): 10, ('3710', '2'): 4, ('4070', '5'): 5},
    {('3029', '4'): 5, ('3029', '8'): 3, ('3001', '1'): 8, ('3710', '2'): 5, ('4070', '5'): 2},
    {('3029', '4'): 7, ('3029', '8'): 2, ('3001', '1'): 7, ('3710', '2'): 6, ('4070', '5'): 4},
    {('3029', '4'): 3, ('3029', '8'): 4, ('3001', '1'): 9, ('3710', '2'): 5, ('4070', '5'): 1},
    {('3029', '4'): 9, ('3029', '8'): 8, ('3001', '1'): 11, ('3710', '2'): 7, ('4070', '5'): 6},
    {('3029', '4'): 6, ('3029', '8'): 5, ('3001', '1'): 8, ('3710', '2'): 4, ('4070', '5'): 3},
    {('3029', '4'): 10, ('3029', '8'): 7, ('3001', '1'): 12, ('3710', '2'): 5, ('4070', '5'): 5},
    {('3029', '4'): 4, ('3029', '8'): 3, ('3001', '1'): 9, ('3710', '2'): 6, ('4070', '5'): 3},
    {('3029', '4'): 8, ('3029', '8'): 6, ('3001', '1'): 10, ('3710', '2'): 5, ('4070', '5'): 4},
    # megabuilder99 (main user)
    {('3029', '4'): 10, ('3029', '8'): 8, ('3001', '1'): 12, ('3710', '2'): 7, ('4070', '5'): 5},
]

mock_users = [
    MockUser(f"user{i+1}", user_inventories[i]) for i in range(len(user_inventories) - 1)
]
mock_users.append(MockUser("megabuilder99", user_inventories[-1]))

mock_api = MockApi(mock_users)


# Step 4: Run the test
if __name__ == "__main__":
    threshold = 0.5
    print("=== Running Task 3: Largest Collection of Pieces ===")
    result = largest_collection_of_pieces(mock_api, "megabuilder99", threshold)
    print("\n✅ Final Largest Common Collection:")
    for piece, qty in result.items():
        print(f"{piece}: {qty}")
