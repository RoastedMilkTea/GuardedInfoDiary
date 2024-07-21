import os
from cryptography.fernet import Fernet

#gets the encryption key
with open("encryption_key.key", "rb") as key_file:
    key = key_file.read()

cipher_suite = Fernet(key)

#decrypts the file and then reads it line by line
  
def decrypt_log_file(filename):
    try:
        with open(filename, "r") as f:
            encrypted_lines = f.readlines()

        for encrypted_line in encrypted_lines:
            encrypted_line = encrypted_line.strip()  # Remove the newline character

            try:
                decrypted_data = cipher_suite.decrypt(encrypted_line.encode())
                print(decrypted_data.decode())
            except Exception as e:
                print(f"Decryption failed for line: {encrypted_line}")
                print(e)
    except Exception as e:
        print(f"Failed to read or process file: {filename}")
        print(e)

decrypt_log_file("log.txt")
if os.path.exists("log_old.txt"):
    decrypt_log_file("log_old.txt")