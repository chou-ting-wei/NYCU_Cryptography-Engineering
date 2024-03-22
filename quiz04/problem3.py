import random
import numpy as np
from itertools import permutations

def naive_shuffle(cards):
    for i in range(len(cards)):
        n = random.randint(0, len(cards) - 1)
        cards[i], cards[n] = cards[n], cards[i]
    return cards

def fisher_yates_shuffle(cards):
    for i in range(len(cards) - 1, 0, -1):
        n = random.randint(0, i)
        cards[i], cards[n] = cards[n], cards[i]
    return cards

def shuffle_simulation_with_stats(shuffle_function, num_trials=1000000):
    card_set = [1, 2, 3, 4]
    all_permutations = list(permutations(card_set))
    combinations_count = {perm: 0 for perm in all_permutations}
    
    for _ in range(num_trials):
        shuffled_cards = shuffle_function(card_set.copy())
        combinations_count[tuple(shuffled_cards)] += 1

    counts = list(combinations_count.values())
    avg = np.mean(counts)
    std = np.std(counts)

    return combinations_count, avg, std

naive_results_stats, naive_avg, naive_std = shuffle_simulation_with_stats(naive_shuffle)
fisher_yates_results_stats, fisher_yates_avg, fisher_yates_std = shuffle_simulation_with_stats(fisher_yates_shuffle)

print("Naive algorithm:")
for combination in sorted(naive_results_stats):
    print(f"{combination}: {naive_results_stats[combination]}")
print(f"Average: {naive_avg}, Standard Deviation: {naive_std}")

print("\nFisher–Yates shuffle:")
for combination in sorted(fisher_yates_results_stats):
    print(f"{combination}: {fisher_yates_results_stats[combination]}")
print(f"Average: {fisher_yates_avg}, Standard Deviation: {fisher_yates_std}")
