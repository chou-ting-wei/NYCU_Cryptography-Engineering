import random
import os

random_bytes = bytearray(random.randint(0, 255) for _ in range(1048576))
random_bytes += bytearray(os.urandom(1048576))

with open("secureRandom.bin", "wb") as file:
    file.write(bytes(random_bytes))