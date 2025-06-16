from utils.helper import load_from_json,save_to_file
import json
import os



ROLES_JSON=os.path.join(os.path.dirname(__file__), "roles.json")
class Role:
    def __init__(self,role_id,role_name):
        self.role_id= role_id
        self.role_name= role_name
    def to_dict(self):
        return vars(self)
    

    @classmethod
    def add_role(cls):
        """Add a role to the list of roles."""
        # Ask for role id and name
        # Load the roles
        # Create a new role
        # Append it to the list of roles
        # Save the roles back to the file
        role_id=input("Enter the role_id :")
        role_name=input("Enter the role_name:")
        roles=load_from_json(ROLES_JSON)
        role=Role(role_id,role_name).to_dict()
        roles.append(role)
        save_to_file(roles,ROLES_JSON)

    def list_roles():
        """Displaying the list of saved roles."""

        roles=load_from_json(ROLES_JSON)
        print("\n Available Roles:")

        for r in roles:
            print(f"{r['role_id']} : {r['role_name']}")
        print(" ")

        

    def __str__(self):
        return f"Role [{self.role_id}] - {self.role_name}"
