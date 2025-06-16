import  json
import os

from utils.helpers import load_from_json, save_to_json
ROLES_JSON = os.path.join(os.path.dirname(__file__), "..", "json", "roles.json")

class Role:
    def __init__(self, role_id, role_name):
        self.role_id = role_id
        self.role_name = role_name

    def to_dict(self):
        return vars(self)
    
    def __str__(self):
        return f"Role [{self.role_id}] - {self.role_name}"
    
    def list_roles():
        """List all saved roles """
        roles = load_from_json(ROLES_JSON)
        print("\033[92m\nAvailable Roles:")
        for r in roles:
            print(f"{r['role_id']} : {r['role_name']}")
        print("\033[0m")

    @classmethod
    def add_role(cls):
        role_id = input ("Enter Role ID: ")
        role_name = input ("Enter Role Name: ")

        roles = load_from_json (ROLES_JSON)
        role = Role(role_id, role_name).to_dict() 
        roles.append (role)
        save_to_json(roles, ROLES_JSON)