import os
import pandas as pd
import re

DATA_PATH = "./data/raw_data.csv"
OUTPUT_PATH = "./data/labeled_data.csv"

# Promotion patterns
PROMO_PATTERNS = [
    r"\bup to \d+% off\b",
    r"\b\d+% off\b",
    r"\bflat \d+% off\b",
    r"\bdiscount\b",
    r"\bsale\b",
    r"\boffer\b",
    r"\bsave\b",
    r"\bdeal\b",
    r"\bclearance\b",
    r"\bexclusive\b",
    r"\blimited time\b",
    r"\bbuy one get one\b",
    r"\bmega sale\b",
    r"\bflash sale\b",
    r"\bdeal of the day\b",
    r"\bspecial price\b",
    r"\bbest offer\b",
]

# Non-promotion phrases that look like promo but are not
NON_PROMO_EXCEPTIONS = [
    r"\bnew arrivals\b",
    r"\bjust launched\b",
    r"\bcoming soon\b",
    r"\bnew collection\b",
]

def contains_promo(text):
    if not isinstance(text, str):
        return 0
    text = text.lower()

    # Check for Non-Promo exceptions first (strict match)
    for pattern in NON_PROMO_EXCEPTIONS:
        if re.search(pattern, text):
            return 0

    # Check promo patterns
    for pattern in PROMO_PATTERNS:
        if re.search(pattern, text):
            return 1

    return 0

def preprocess():
    df = pd.read_csv(DATA_PATH)
    df.drop_duplicates(subset=["text"], inplace=True)
    df = df[df["text"].notnull() & (df["text"].str.strip() != "")]
    df["is_promotional"] = df["text"].apply(contains_promo)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Labeled data saved to {OUTPUT_PATH}")
    print(f"Total rows: {len(df)}, Promotional rows: {df['is_promotional'].sum()}")

if __name__ == "__main__":
    preprocess()
