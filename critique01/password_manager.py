from cryptography.fernet import Fernet
import getpass

class SecurePasswordManager:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        self.stored_passwords = {}  
    
    def encrypt_password(self, password):
        return self.cipher_suite.encrypt(password.encode())

    def decrypt_password(self, encrypted_password):
        return self.cipher_suite.decrypt(encrypted_password).decode()

    def save_password(self, domain, protocol, password):
        encrypted_password = self.encrypt_password(password)
        self.stored_passwords[domain] = (protocol, encrypted_password)
        print(f"Password for {domain} saved securely.")

    def auto_fill_password(self, domain, protocol):
        if domain in self.stored_passwords:
            stored_protocol, encrypted_password = self.stored_passwords[domain]
            if stored_protocol.lower() == protocol.lower():
                decrypted_password = self.decrypt_password(encrypted_password)
                print(f"Auto-filling password for {domain}.\nPassword: {decrypted_password}")
                return decrypted_password
            else:
                print(f"Security warning: Protocol mismatch for {domain}. Auto-fill denied.")
        else:
            print(f"No password stored for {domain}.")
            return None

    def manual_user_interaction(self, domain, protocol):
        input("Press Enter to auto-fill password...")
        return self.auto_fill_password(domain, protocol)

print("Welcome to the Secure Password Manager!")
print("Store and retrieve your passwords securely.")
while True:
    print("\n1. Save Password\n2. Retrieve Password\n3. Quit Secure Password Manager")
    mode = input("Enter your choice (1~3): ")
    if mode == "1":
        password_manager = SecurePasswordManager()
        domain = input("Enter the domain: ")
        protocol = input("Enter the protocol (HTTP/HTTPS): ")
        password = getpass.getpass("Enter your password: ")
        password_manager.save_password(domain, protocol, password)
    elif mode == "2":
        user_requested_domain = input("Enter domain to retrieve password: ")
        user_requested_protocol = input("Enter the protocol for retrieval (HTTP/HTTPS): ")
        password_manager.manual_user_interaction(user_requested_domain, user_requested_protocol)
    else:
        print("Goodbye!")
        break
