import torch
import numpy as np
import random
from purple.machine import Purple97
from purple.main import filter_plaintext, filter_whitespace, group_text

sw_fast_slow = {1:'12', 2:'21', 3:'13', 4:'31', 5:'23', 6:'32'}
def RandomPurple():
    a = random.randint(0, pow(25, 4))
    e = random.randint(1, 6)
    key = f"{a%25+1}-{a//25%25+1},{a//625%25+1},{a//15625%25+1}-{sw_fast_slow[e]}"
    machine = Purple97().from_key_sheet(key)
    return [machine, [a%25+1,a//25%25+1,a//625%25+1,a//15625%25+1,e]]
def CalculateKeyDistance(key1, key2):
    return sum([abs(key1[i] - key2[i]) for i in range(len(key1))])
def CreateRandomKeyFromDistance(key, distance):
    while distance > 0:
        newkey = key.copy()
        it = random.randint(0, len(key) - 1)
        temp = newkey[it]
        preit = it
        newkey[preit] = temp
        preit = it
        it = random.randint(0, len(key) - 1)
        newkey[it] = ((random.randint(-1,1)+newkey[it])+25)%25+1 if it != 4 else ((random.randint(-1,1)+newkey[it]+6)%6 +1)  
        distance -= CalculateKeyDistance(key, newkey)
        if distance < 0:
            distance += CalculateKeyDistance(key, newkey)
        else:
            key = newkey
            
    return key
    
def GetKeyFromArr(arr):
    return f"{arr[0]}-{arr[1]},{arr[2]},{arr[3]}-{sw_fast_slow[arr[4]]}"

def filter(text:str):
    return filter_plaintext(text)

def PorcessData(data:str):
    pur1, key1 = RandomPurple()
    # key2 = CreateRandomKeyFromDistance(key1, random.randint(0, 10))
    # pur2 = Purple97().from_key_sheet(GetKeyFromArr(key2))
    # filtered = filter(data)
    # encrypted = pur1.encrypt(filtered)
    # decrypted = pur2.decrypt(encrypted)
    # return [decrypted, CalculateKeyDistance(key1, key2)]
    processed = pur1.encrypt(filter(data))
    return [processed, key1]

if __name__ == "__main__":
    data = "This is an example text with normal typing.Hello enigma machine. This is purple machine."
    data = filter(data)
    print(data)
    pur1, key1 = RandomPurple()
    dis = random.randint(0, 40)
    print(dis)
    key2 = CreateRandomKeyFromDistance(key1, dis)
    print(key1, key2)
    encrypted = pur1.encrypt(data)
    pur2 = Purple97().from_key_sheet(GetKeyFromArr(key2))
    pur1 = Purple97().from_key_sheet(GetKeyFromArr(key1))
    print(pur1.decrypt(encrypted))
    decrypted = pur2.decrypt(encrypted)
    print(decrypted)