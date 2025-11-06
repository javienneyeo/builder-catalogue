import requests
from user import User
from set import Set
from piece import Piece

class ApiError(Exception):
    """Custom exception for API-related issues."""
    pass

class ApiDataHandler:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _get_json(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise ApiError(f"Timeout error: The request to {url} took too long to respond.")
        except requests.exceptions.ConnectionError:
            raise ApiError(f"Connection error: Unable to connect to {url}.")
        except requests.exceptions.HTTPError as http_err:
            raise ApiError(f"HTTP error {response.status_code} when accessing {url}: {http_err}")
        except requests.exceptions.RequestException as req_err:
            raise ApiError(f"Request exception occurred for {url}: {req_err}")
        except ValueError as json_err:
            raise ApiError(f"JSON decoding failed for {url}: {json_err}")

    def get_all_users(self) -> list[User]:
        users_list = self._get_json("/api/users")
        all_users = []
        for u in users_list['Users']:
            user_data = self._get_json(f"/api/user/by-id/{u['id']}")
            
            pieces_dict = {}
            for p in user_data['collection']:
                for v in p['variants']:
                    pieces_dict[Piece(p['pieceId'], v['color'])] = v['count']

            all_users.append(User(u['id'], u['username'], u['brickCount'], pieces_dict))
        return all_users

    def get_user_by_username(self, username: str) -> User:
        data = self._get_json(f"/api/user/by-username/{username}")

        user_id = data['id']
        brick_count = data['brickCount']
        user_data = self._get_json(f"/api/user/by-id/{user_id}")
        
        inventory = {}
        for p in user_data['collection']:
            for v in p['variants']:
                inventory[Piece(p['pieceId'], v['color'])] = v['count']
        return User(user_id, username, brick_count, inventory)

    def get_all_sets(self) -> list[Set]:
        sets_list = self._get_json("/api/sets")
        all_sets = []
        for s in sets_list['Sets']:
            set_data = self._get_json(f"/api/set/by-id/{s['id']}")
            
            pieces = {}
            for p in set_data['pieces']:
                pieces[Piece(p['part']['designID'], p['part']['material'])] = p['quantity']

            all_sets.append(Set(set_data['id'], set_data["name"], set_data['totalPieces'], pieces))

        return all_sets

    def get_set_by_set_name(self, set_name) -> Set:
        set_summary = self._get_json(f"/api/set/by-name/{set_name}")
        set_id = set_summary['id']
        set_full = self._get_json(f"/api/set/by-id/{set_id}")

        required_pieces = {}
        for p in set_full['pieces']:
            required_pieces[Piece(p['part']['designID'], p['part']['material'])] = p['quantity']

        return Set(set_summary['id'], set_name, set_summary['totalPieces'], required_pieces)