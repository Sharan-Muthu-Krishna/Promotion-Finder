import glob
import pandas as pd

files = glob.glob("../data/*_raw_data.csv")
print("Found files:", files)

dfs = []
for file in files:
    try:
        df = pd.read_csv(file)
        print(f"{file}: {len(df)} rows")
        if not df.empty:
            dfs.append(df)
        else:
            print(f"Skipped empty file: {file}")
    except Exception as e:
        print(f"Error reading {file}: {e}")

if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv("../data/raw_data.csv", index=False)
    print(f"\nCombined dataset has {len(combined_df)} rows.")
else:
    print("No data to combine.")
