import secrets

with open("random.bin", "wb") as file:
    file.write(secrets.token_bytes(1048576))