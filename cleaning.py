import pandas as pd

raw = pd.read_csv("data/raw_data.csv")
df = raw.copy()
log = {}

# --- Profile ---
log["rows_before"], log["cols_before"] = df.shape
log["nulls_before"] = int(df.isna().sum().sum())
log["dupe_rows_before"] = int(df.duplicated().sum())
log["dupe_ids_before"] = int(df["PassengerId"].duplicated().sum())
print("Missing per column:\n", df.isna().sum()[lambda s: s > 0])

# --- Duplicates ---
df = df.drop_duplicates().drop_duplicates(subset="PassengerId")

# --- Inconsistent text ---
for c in ["Name", "Sex", "Embarked", "Ticket", "Cabin"]:
    df[c] = df[c].astype("string").str.strip()
df["Sex"] = df["Sex"].str.lower()
df["Embarked"] = df["Embarked"].str.upper()

# --- Missing values ---
df["Age_Missing"] = df["Age"].isna()                       # keep a flag
df["Title"] = df["Name"].str.extract(r",\s*([^.]+)\.", expand=False).str.strip()
df["Title"] = df["Title"].replace({"Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs"})
rare = df["Title"].value_counts()[lambda s: s < 10].index
df["Title"] = df["Title"].replace(dict.fromkeys(rare, "Rare"))
df["Age"] = df["Age"].fillna(df.groupby("Title")["Age"].transform("median"))
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
df["Has_Cabin"] = df["Cabin"].notna()
df["Cabin"] = df["Cabin"].fillna("Unknown")

# --- Data types ---
df["Survived"] = df["Survived"].astype("bool")
for c in ["Pclass", "Sex", "Embarked", "Title"]:
    df[c] = df[c].astype("category")
df["Age"] = df["Age"].round(1)

# --- Validation ---
assert df[["Age", "Embarked", "Fare"]].isna().sum().sum() == 0
assert (df["Age"] > 0).all() and (df["Fare"] >= 0).all()

log["rows_after"], log["cols_after"] = df.shape
log["nulls_after"] = int(df.isna().sum().sum())
log["dupe_rows_after"] = int(df.duplicated().sum())
df.to_csv("data/cleaned_data.csv", index=False)
for k, v in log.items(): print(k, v)
print(df.dtypes)
