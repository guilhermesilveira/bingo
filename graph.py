import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from counting import normalize, confidence

sns.set(style="whitegrid", color_codes=True, font_scale=2)


def show_bar(data):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=data.index, y=data.values)


def show_line(data):
    plt.figure(figsize=(12, 6))
    ax = sns.lineplot(x=data.index, y=data.values)
    return ax


def print_prob_table(df):
    left = []
    right = []
    for i, (decks, results, successes, n, probability) in df.iterrows():
        r = confidence(successes, n)
        left.append(r[0])
        right.append(r[1])
    df["prob_l"] = left
    df["prob_r"] = right
    return df


def print_cumulative(df, calculate_prob=True, xticks=None, figsize=(12, 6), palette=None):
    if calculate_prob and (not "prob_l" in df.columns):
        print_prob_table(df)

    plt.figure(figsize=figsize)

    data = []
    for i, (decks, results, successes, n, probability, prob_l, prob_r) in df.iterrows():
        results[results == -1] = 53
        m1n = normalize(results, cumulative=True)
        for (card, value) in m1n.items():
            if card == 53:
                continue
            data.append([decks, card + 1, value])

    data = pd.DataFrame(data, columns=["decks", "card", "values"])
    ax = sns.lineplot(x="card", y="values", hue="decks", data=data, palette=palette)
    if xticks:
        plt.xticks(xticks)
    plt.xlabel("Card")
    plt.ylabel("Empirical %")
    return ax, data


def colorblind_palette(k):
    green = sns.color_palette("colorblind")[2]
    orange = sns.color_palette("colorblind")[3]
    sequential = sns.light_palette(green, n_colors=k * 2)[k // 2:][:k]
    return sequential, orange


def plot_all(df, field):
    pal = sns.color_palette("Greens_d", len(df))
    rank = df[field].argsort().argsort()
    pal = np.array(pal[::-1])[rank]

    plt.figure(figsize=(8, 6))
    sns.barplot(data=df, x='Deck count', y=field, palette=pal)
    plt.title(f"{field} x Deck Count")
