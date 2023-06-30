
def prob_table_to_latex(df, name: str):
    cols = ["Probability", "prob_l", "prob_r"]
    temp = df.set_index("Deck count")[cols].copy().reset_index()
    temp.columns = ["Decks", "Probability", "CI lower", "CI upper"]
    temp["Decks"] = temp["Decks"].astype(int)
    temp = temp.set_index("Decks")
    formatter = '{:,.3f}'.format
    temp["Probability"] = (temp["Probability"]).apply(formatter) + "%"
    temp["CI lower"] = (temp["CI lower"] * 100).apply(formatter) + "%"
    temp["CI upper"] = (temp["CI upper"] * 100).apply(formatter) + "%"
    print(temp.to_latex(label=f"tbl:{name}", position="tb"))

