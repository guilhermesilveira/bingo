from bingo import shuffled_deck
from functools import partial
from parallel import run_multiple
import pandas as pd


def signed_card_bingo(betas: list[list[int]]):
    # Define alpha, the memorized sequence as a list from 1 to 52
    alpha = list(range(1, 53))
    iterations = 1

    while len(alpha) > 2:
        # Check first condition: someone has a signed card match or joker
        if any(beta[0] in [1, 0] for beta in betas):
            return iterations

        for i, beta in enumerate(betas):
            # Someone has a match with the second card
            if beta[0] == alpha[1]:
                for j in range(len(betas)):
                    # Someone has a match with the third card
                    if i != j and betas[j][0] == alpha[2]:
                        return -1

                # Perform a third deal: we update sequences
                # Discard the third item
                alpha = alpha[:2] + alpha[3:]
                # Discard first item from each participant
                betas = [beta[1:] for beta in betas]
                break  # Proceed to the next iteration

        # If none of the previous conditions were met
        # Do a second deal, discard the second item
        alpha = [alpha[0]] + alpha[2:]
        # Discard first item from each participant
        betas = [beta[1:] for beta in betas]

        iterations += 1

    # After exhausting alpha, all jokers were the bottom 2 betas
    return -1


def signed_runs(deck_count: int, runs: int):
    successes = 0
    for run in range(runs):
        decks = [shuffled_deck(True) for d in range(deck_count)]
        result = signed_card_bingo(decks)
        if result >= 0:
            successes += 1
    return [successes, successes, runs, successes / runs * 100]


def quick_signed_runs(decks: list[int], runs: int):
    p = partial(signed_runs, runs=runs)
    results = run_multiple(p, decks)
    results = pd.DataFrame(
        results, columns=["Deck count", "Success", "Result", "Runs", "Probability"])
    return results
