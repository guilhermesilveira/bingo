from math import sqrt
from functools import partial
from parallel import run_multiple

from statsmodels.stats.proportion import proportion_confint
import pandas as pd

from bingo import quick_deck_match


def binomial_ic(count, nobs, method):
    return proportion_confint(count, nobs, method=method)


def normalize(data, cumulative=False):
    normalized = pd.Series(data).value_counts(
        normalize=True).sort_index() * 100

    if cumulative:
        normalized = normalized.cumsum()

    return normalized


def quick_deck_matches(n, accept_jokers=False, early_stop=100, max_decks=15, discard=0):
    return quick_deck_matches_on(n, range(1, max_decks), accept_jokers, early_stop, discard)


def quick_deck_matches_on(n, decks, accept_jokers=False, early_stop=100, discard=0):
    p = partial(quick_deck_match, n, accept_jokers=accept_jokers,
                early_stop=early_stop, discard=discard)
    results = run_multiple(p, decks)

    return pd.DataFrame(results, columns=["Deck count", "Results", "Successes", "N", "Probability"])


def partial_card_to_prob(d, total_runs):
    data = []
    for i, (decks, card, values) in d.iterrows():
        data.append(
            [decks, values, *confidence(values * total_runs / 100, total_runs)])
    return pd.DataFrame(data, columns=["Deck count", "Probability", "prob_l", "prob_r"])


def confidence(ups, n):
    if n == 0:
        return 0

    z = 1.96
    phat = float(ups) / n
    left = phat + z * z / (2 * n)
    right = z * sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)
    under = (1 + z * z / n)
    return ((left - right) / under), ((left + right) / under)
