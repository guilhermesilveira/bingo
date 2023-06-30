import numpy as np
import pandas as pd

memorized = np.arange(1, 53)
copied = memorized.copy()
copied_jokers = np.array([0, 0, *memorized])


def shuffled_deck(accept_jokers):
    chosen = copied
    if accept_jokers:
        chosen = copied_jokers

    np.random.shuffle(chosen)
    return chosen


def first_match(accept_jokers=False):
    chosen = shuffled_deck(accept_jokers)
    for i, (f, s) in enumerate(zip(memorized, chosen[:52])):
        if f == s or s == 0:
            return i
    return -1


# Full search
def how_many_decks_match(deck_count):
    results = np.array([first_match() for i in range(deck_count)])
    return sum(results >= 0)


# Full search: With decks decks, running N times the simulation, what are the odds?
def n_how_many_decks_match(n, decks):
    results = np.array([how_many_decks_match(decks) for i in range(n)])
    prop = sum(results > 0) / n
    print(f"{decks} parsed.")
    return prop


# Represents a table with n decks in it, with a quick first search.
# All decks start shuffled
class Table:
    def __init__(self, n, accept_jokers):
        if accept_jokers:
            self.decks = [copied_jokers.copy() for i in range(n)]
        else:
            self.decks = [memorized.copy() for i in range(n)]
        self.shuffle()

    # shuffle all existing decks
    def shuffle(self):
        for deck in self.decks:
            np.random.shuffle(deck)

    # gets the first match within the decks
    def get_first_match(self, early_stop=100, discard=0):
        for i in range(discard, min(len(memorized), early_stop + discard)):
            for deck in self.decks:
                if deck[i] == memorized[i] or deck[i] == 0:
                    return i
        return -1


def quick_deck_match(n, decks, accept_jokers=False, early_stop=100, discard=0):
    table = Table(decks, accept_jokers)
    results = []
    for i in range(n):
        table.shuffle()
        result = table.get_first_match(early_stop=early_stop, discard=discard)
        results.append(result)

    results = pd.Series(np.array(results))
    successes = sum(results >= 0)
    successes_percentage = successes / n * 100
    return [results, successes, n, successes_percentage]
