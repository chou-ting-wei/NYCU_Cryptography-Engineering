def cypher_freq(f_path):
    freq = {}
    with open(f_path, "r") as file:
        for l in file:
            for c in l:
                if c.isalpha():
                    freq[c] = freq.get(c, 0) + 1
    
    return freq

f_path = "./Quiz1/cyphertext.txt"
unsorted_freq = cypher_freq(f_path)
sorted_freq = {k: v for k, v in sorted(unsorted_freq.items(), key=lambda item: item[1], reverse=True)}
print(sorted_freq)