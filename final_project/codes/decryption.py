import nltk
import json
import random
from collections import *
import math
from purple.machine import Purple97
from purple.main import filter_plaintext, filter_whitespace, group_text
import tqdm
import substitution
sw_fast_slow = {1:'12', 2:'21', 3:'13', 4:'31', 5:'23', 6:'32'}
def RandomPurple():
    a = random.randint(1, 25)
    b = random.randint(1, 25)
    c = random.randint(1, 25)
    d = random.randint(1, 25)
    e = random.randint(1, 6)
    key = f"{a}-{b},{c},{d}-{sw_fast_slow[e]}"
    machine = Purple97().from_key_sheet(key)
    return [machine, [a,b,c,d,e]]
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
    return filter_plaintext(text)


class MCMC:
    def __init__(self, text, bigrams,grade_function=grade):
        self.text = text
        self.bigrams = bigrams
        self.best_score = -float('inf')
        self.best_text = ""
        self.grade = grade_function
        self.pur, self.key = RandomPurple()
        self.encrypted = self.pur.encrypt(self.text)
        self.decrypted 
    
    def decrypt(self, key):
        depur = Purple97().from_key_sheet(key)
        return depur.decrypt(self.encrypted)
            
    def score(self, key):
        grade = 0
        decrypted = self.decrypt(key)
        return self.grade(decrypted, self.bigrams)
        pass
    
    def run(self, iterations=10000):
        current_key = self.key
        current_score = self.score(f"{current_key[0]}-{current_key[1]},{current_key[2]},{current_key[3]}-{sw_fast_slow[current_key[4]]}")
        
        for i in range(iterations):
            # Propose a new key by randomly changing one part of the current key
            new_key = current_key[:]
            part_to_change = random.randint(0, 4)
            if part_to_change == 4:  # change switch setting
                new_key[part_to_change] = (random.randint(-1,1) + new_key[part_to_change]+6) % 6 + 1
            else:  # change one of the wheels
                new_key[part_to_change] = (random.randint(-1,1) + new_key[part_to_change]+25)%25+1
            
            new_key_str = f"{new_key[0]}-{new_key[1]},{new_key[2]},{new_key[3]}-{sw_fast_slow[new_key[4]]}"
            new_score = self.score(new_key_str)
            
            # Accept the new key based on the acceptance probability
            if new_score > current_score or random.random() < math.exp((new_score - current_score) / 1.0):  # Simulated annealing temperature
                current_key = new_key
                current_score = new_score
                print(f"New score: {current_score}, Key: {new_key_str}",end="\r")
                if new_score > self.best_score:
                    self.best_score = new_score
                    self.best_text = self.decrypt(new_key_str)
                    print(f"New best score: {self.best_score}, Key: {new_key_str}, Text: {self.best_text}")
           


if __name__ == "__main__":
    try:
        bigrams = load_bigram()
        if bigrams is None:
            bigrams = prepare_bigram_scores()
            save_bigram(bigrams)
    except:
        bigrams = prepare_bigram_scores()
        save_bigram(bigrams)
    text = "This is an example text with normal typing. Hello enigma machine. This is purple machine."
    text = filter(text)
    pur, key = RandomPurple()
    print(f"Key: {key}")
    encrypted = pur.encrypt(text)
    print(f"Encrypted: {encrypted}")
    best_text = ""
    best_score = -float('inf')
    temp = input("choose mode: 1 for brute force, 2 for genetic algorithm: ")
    if temp == "1":
        for i in tqdm.tqdm(range(1,pow(25,4)), desc="Decyphering"):
            for m in range(1, 6):
                key = f"{i%25+1}-{i//25%25+1},{i//625%25+1},{i//15625%25+1}-{sw_fast_slow[m]}"
                depur = Purple97.from_key_sheet(key)
                decrypted = depur.decrypt(encrypted)
                score = grade(decrypted, bigrams)
                if score > best_score:
                    best_score = score
                    best_text = decrypted
                    print(f"Best score: {best_score}, key: {key}, text: {best_text}")
        print(f"Best score: {best_score}, text: {best_text}")
    else:
        mcmc = MCMC(encrypted, bigrams, grade)
        mcmc.run()
        print(f"Best score: {mcmc.best_score}, text: {mcmc.best_text}")