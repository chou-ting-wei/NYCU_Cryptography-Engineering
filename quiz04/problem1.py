key = [0, 0, 0, 0, 0, 0, 0, 1]
for i in range(1, 1000):
    if key == [0, 0, 0, 0, 0, 0, 0, 1]:
        print(f'{i}: {key}')
    tmp = key[0]
    for j in range(7):
        key[j] = key[j + 1]
    key[7] = 0
    if tmp:
        key[3] = 1 ^ key[3]
        key[4] = 1 ^ key[4]
        key[5] = 1 ^ key[5]
        key[7] = 1 ^ key[7]

key = [0, 0, 0, 1]
for i in range(1,20):
    if key == [0, 0, 0, 1]:
        print(f'{i}: {key}')
    tmp = key[0]
    for j in range(3):
        key[j] = key[j + 1]
    key[3] = 0
    if tmp:
        key[0] = 1 ^ key[0]
        key[1] = 1 ^ key[1]
        key[2] = 1 ^ key[2]
        key[3] = 1 ^ key[3]