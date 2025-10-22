import pandas as pd

# Read file safely (skip broken lines)
df = pd.read_csv(
    'jumia_reviews.csv',
    on_bad_lines='skip',     # skip malformed lines
    quoting=1,               # ensure proper quoting
    encoding='utf-8'
)

# Optional: check number of rows before/after
print("Total valid rows:", len(df))

# Re-save with correct quoting
df.to_csv('jumia_reviews_clean.csv', index=False, quoting=1)
print("Clean CSV saved as jumia_reviews_clean.csv")
