from collections import Counter
import math
import json
from purple.main import filter_plaintext, filter_whitespace
def filter(text:str):
    return filter_whitespace(filter_plaintext(text))
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