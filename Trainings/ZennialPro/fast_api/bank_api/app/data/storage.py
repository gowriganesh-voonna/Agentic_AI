import json
import os

DATA_FILE= "app/data/accounts.json"

def load_accounts():
    try:
        # Example assuming JSON storage
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Failed to load accounts: {e}")
        return {}
def save_accounts(accounts):
    with open(DATA_FILE,"w") as f:
        json.dump(accounts,f, indent=4)
