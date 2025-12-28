import pandas as pd
import os

DB_FILE = "user_data.csv"

def initialize_db():
    if not os.path.exists(DB_FILE):
        df = pd.DataFrame(columns=["username", "balance", "high_score"])
        df.to_csv(DB_FILE, index=False)

def get_user(username):
    initialize_db()
    df = pd.read_csv(DB_FILE)
    if "username" not in df.columns:
        os.remove(DB_FILE)
        initialize_db()
        df = pd.read_csv(DB_FILE)
    user_row = df[df["username"] == username]
    return user_row.iloc[0].to_dict() if not user_row.empty else None

def save_user(username, balance, high_score):
    initialize_db()
    df = pd.read_csv(DB_FILE)
    if username in df["username"].values:
        df.loc[df["username"] == username, ["balance", "high_score"]] = [balance, high_score]
    else:
        new_row = pd.DataFrame([{"username": username, "balance": balance, "high_score": high_score}])
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

def get_top_players():
    initialize_db()
    df = pd.read_csv(DB_FILE)
    return df.sort_values(by="high_score", ascending=False).head(5)