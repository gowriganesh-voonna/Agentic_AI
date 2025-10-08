from google.auth import default

creds, project = default()
print("Credentials loaded successfully.")
print(f"Project ID: {project}")