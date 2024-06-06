import nltk
import json
import random
from collections import *
import math
from purple.machine import Purple97
from purple.main import filter_plaintext, filter_whitespace, group_text
import tqdm
import string
sw_fast_slow = {1:'12', 2:'21', 3:'13', 4:'31', 5:'23', 6:'32'}
def RandomPurple():
    a = random.randint(1, 25)
    b = random.randint(1, 25)
    c = random.randint(1, 25)
    d = random.randint(1, 25)
    e = random.randint(1, 6)
    key = f"{a}-{b},{c},{d}-{sw_fast_slow[e]}"
    machine = Purple97().from_key_sheet(key)
    return [machine, key]
def prepare_bigram_scores():
    key = Counter()
    with open("book-war-and-peace.txt", 'r', encoding="utf-8") as f:
        data = f.read().split("\n")
        data = filter(data)
        prev = ""
        for char in data:
            if prev:
                key[prev+char] += 1
            prev = char

    # Total number of bigrams counted
    total_bigrams = sum(key.values())
    
    # Calculate log probabilities of bigrams
    bigram_log_probs = {}
    for bigram, count in key.items():
        bigram_log_probs[bigram] = math.log(count / total_bigrams)

    return bigram_log_probs
def load_bigram(filename="bigram_scores.json"):
    # Read the file and deserialize the JSON content into a dictionary
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            bigram_scores = json.load(f)
        print(f"Bigram scores loaded from {filename}")
        return bigram_scores
    except FileNotFoundError:
        print(f"Error: The file {filename} does not exist.")
        return None

def save_bigram(bigram_scores, filename="bigram_scores.json"):
    # Serialize the dictionary of bigram scores and write it to a file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(bigram_scores, f, ensure_ascii=False, indent=4)
    print(f"Bigram scores saved to {filename}")     

def grade(s: str, bigram_scores):
    """
    Grades a string based on its bigram scores.

    :param s: The string to be graded.
    :param bigram_scores: A dictionary containing log probabilities of bigrams.
    :return: A float score, with higher scores indicating a better match to the expected bigram frequencies.
    """
    filtered = filter(s)
    score = 0
    prev = ""
    for char in filtered:
        if prev:
            score += bigram_scores.get(prev + char, -15)
        prev = char
    return score
def filter(text:str):
    return filter_whitespace(filter_plaintext(text))
def generate_cipher(cypher:str) -> str:
    char_count = {x:0 for x in string.ascii_uppercase}
    for c in cypher:
        if c not in string.ascii_uppercase:
            continue
        if c in char_count:
            char_count[c]+=1
        else:
            char_count[c]=1
    sorted_char_count = sorted(char_count.items(),key=lambda x:x[1],reverse=True)
    common_chars = "EARIOTNSLCUDPMHGBFYWKVXZJQ"
    char_pairs = list(zip(common_chars,sorted_char_count))
    sorted_char_pair = sorted(char_pairs,key=lambda x:x[1][0])
    return ''.join([x[0] for x in sorted_char_pair])
def apply_key(text:str,key:str) -> str:
    u = text.upper()
    return ''.join([key[string.ascii_uppercase.index(c)] if c in string.ascii_uppercase else c for c in u])
def swap(cipher:str) -> str:
    i = random.randint(0,25)
    j = random.randint(0,25)
    new_cipher = list(cipher)
    if i != j:
        new_cipher[i],new_cipher[j] = new_cipher[j],new_cipher[i]
    return ''.join(new_cipher)

class MCMC:
    def __init__(self, text, bigrams):
        self.text = text
        self.bigrams = bigrams
        self.best_score = -float('inf')
        self.best_text = ""
        self.key = generate_cipher(self.text)
        self.grade = grade
    
    def decrypt(self, key):
        return apply_key(self.text, key)
            
    def score(self, key):
        grade = 0
        decrypted = self.decrypt(key)
        return self.grade(decrypted, self.bigrams)
    
    def run(self, iterations=10000):
        current_key = self.key
        current_score = self.score(current_key)
        
        for i in range(iterations):
            # Propose a new key by randomly changing one part of the current key
            new_key_str = swap(current_key)
            new_score = self.score(new_key_str)
            
            # Accept the new key based on the acceptance probability
            if new_score > current_score or random.random() < math.exp((new_score - current_score) / 1.0):  # Simulated annealing temperature
                current_key = new_key_str
                current_score = new_score
                print(f"New score: {current_score}, Key: {new_key_str}",end="\r")
                if new_score > self.best_score:
                    self.best_score = new_score
                    self.best_text = self.decrypt(new_key_str)
        return self.best_text, self.best_score
           


if __name__ == "__main__":
    try:
        bigrams = load_bigram()
        if bigrams is None:
            bigrams = prepare_bigram_scores()
            save_bigram(bigrams)
    except:
        bigrams = prepare_bigram_scores()
        save_bigram(bigrams)
    text = "In the heart of a dense forest, dappled sunlight pierced the thick canopy, casting a mosaic of light and shadow on the forest floor. "
    pur, key = RandomPurple()
    print(f"Key: {key}")
    encrypted = pur.encrypt(filter(text))
    print(f"Encrypted: {encrypted}")
    pur = Purple97().from_key_sheet(key)
    print(f"The cypher should be decrypt like this: {pur.decrypt(encrypted)}")
    best_text = ""
    best_score = -float('inf')
    for i in tqdm.tqdm(range(1,pow(25,4)), desc="Decyphering"):
        for m in range(1, 6):
            key = f"{i%25+1}-{i//25%25+1},{i//625%25+1},{i//15625%25+1}-{sw_fast_slow[m]}"
            depur = Purple97().from_key_sheet(key)
            decrypted = depur.decrypt(encrypted)
            score = grade(decrypted, bigrams)
            if score > best_score:
                best_score = score
                best_text = decrypted
    print(f"Best score: {best_score}, text: {best_text}")
        