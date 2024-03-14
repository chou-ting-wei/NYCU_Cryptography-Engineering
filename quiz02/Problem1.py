import hashlib
import time
import requests

url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt"

response = requests.get(url)
passwords = response.text.splitlines()

hashes = [
    "ef0ebbb77298e1fbd81f756a4efc35b977c93dae",
    "0bc2f4f2e1f8944866c2e952a5b59acabd1cebf2",
    "9d6b628c1f81b4795c0266c0f12123c1e09a7ad3",
    "44ac8049dd677cb5bc0ee2aac622a0f42838b34d"
]

salt = "dfc3e4f0b9b5fb047e9be9fb89016f290d2abb06"

def crack_sha1(hash_to_crack):
    attempts = 0
    start_time = time.time()

    for password in passwords:
        attempts += 1
        if hashlib.sha1(password.encode()).hexdigest() == hash_to_crack:
            return password, attempts, time.time() - start_time

    return None, attempts, time.time() - start_time

def crack_sha1_salt(hash_to_crack, _salt):
    attempts = 0
    start_time = time.time()
    
    for password in passwords:
        attempts += 1
        if hashlib.sha1((_salt + password).encode()).hexdigest() == hash_to_crack:
            return _salt + password, attempts, time.time() - start_time

    return None, attempts, time.time() - start_time

def crack_sha1_two_word(hash_to_crack):
    attempts = 0
    start_time = time.time()
    
    for password in passwords:
        attempts += 1
        for second_word in password:
            combined = f"{password} {second_word}"
            if hashlib.sha1(combined.encode()).hexdigest() == hash_to_crack:
                return password, second_word, attempts, time.time() - start_time

    return None, attempts, time.time() - start_time

for i, hash_value in enumerate(hashes):
    if i < 2:
        result = crack_sha1(hash_value)
        if result[0]:
            print(f"Hash: {hash_value}\nPassword: {result[0]}\nTook {result[1]} attempts to crack input hash. Time Taken: {result[2]}")
        else:
            print(f"Hash: {hash_value} not found in the top 1 million passwords.")
    elif i == 2:
        tmp = crack_sha1(salt)
        result = crack_sha1_salt(hash_value, tmp[0])
        if result[0]:
            print(f"Hash: {hash_value}\nPassword: {result[0]}\nTook {result[1]} attempts to crack input hash. Time Taken: {result[2]}")
        else:
            print(f"Hash: {hash_value} not found in the top 1 million passwords.")

def revtext(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    reversed_lines = lines[::-1]

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(reversed_lines)


input_file_path1 = './Quiz2/dict1.txt'  
output_file_path1 = './Quiz2/revdict1.txt' 
input_file_path2 = './Quiz2/dict2.txt' 
output_file_path2 = './Quiz2/revdict2.txt'  

revtext(input_file_path1, output_file_path1)
revtext(input_file_path2, output_file_path2)
