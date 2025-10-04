
import pandas as pd
import numpy as np
from functools import partial


# Example user data
data = {
    "user_id": [1, 2, 3, 4, 5, 5],  
    "name": ["ones", "jamel", "mezen", "amel", "Eve", "adam"],
    "age": [25, 30, np.nan, 22, 29, 29],
    "join_date": ["2022-01-15", "2021-12-01", "2023-02-20", "invalid_date", "2023-06-10", "2023-06-10"],
    "score": ["85", "90", "80", "NaN", "95", "95"]
}

# Save to CSV
df_raw = pd.DataFrame(data)
df_raw.to_csv("users.csv", index=False)

print(" Example CSV file 'users.csv' created successfully!\n")



series_example = pd.Series(
    [100, 200, 300],
    index=["A", "B", "C"],
    name="Custom Series"
)
print(" Pandas Series with custom index:")
print(series_example, "\n")


#  Create a Pandas DataFrame


columns = ["user_id", "name", "age", "join_date", "score"]
df = pd.read_csv("users.csv", usecols=columns)
print(" DataFrame created from CSV:")
print(df, "\n")


#  Inspect the DataFrame


print(" Data Types:")
print(df.dtypes, "\n")

print(" Head (first 3 rows):")
print(df.head(3), "\n")

print(" Tail (last 2 rows):")
print(df.tail(2), "\n")

print(" Summary Statistics:")
print(df.describe(include="all"), "\n")


print(" Rows 1 to 3 (using iloc):")
print(df.iloc[1:4], "\n")

print(" Select specific columns (name and age):")
print(df[["name", "age"]], "\n")





print("🔹 Rows where age > 25:")
print(df[df["age"] > 25], "\n")

print("🔹 Rows where age is between 20 and 30:")
print(df[df["age"].between(20, 30)], "\n")

# Demonstrate duplicated

print(" Duplicated rows:")
print(df[df.duplicated()], "\n")

print(" Number of unique user IDs:", df["user_id"].nunique(), "\n")

print(" Drop duplicates based on user_id:")
df_no_dupes = df.drop_duplicates(subset=["user_id"])
print(df_no_dupes, "\n")


# 8️  conversion


df["score"] = pd.to_numeric(df["score"], errors="coerce")  # safely convert to numeric
df["join_date"] = pd.to_datetime(df["join_date"], errors="coerce")  # safely convert to datetime

print("Data types after safe conversion:")
print(df.dtypes, "\n")


#  missing data using 


def fill_missing_age(age):
    """Replace missing ages with a default value of 25."""
    return 25 if pd.isna(age) else age

df["age"] = df["age"].apply(fill_missing_age)

print(" After filling missing age values:")
print(df, "\n")



def clean_types(df):
    """Ensure correct data types for numeric and datetime columns."""
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["join_date"] = pd.to_datetime(df["join_date"], errors="coerce")
    return df

df_cleaned = df.pipe(clean_types)

print(" After cleaning pipeline:")
print(df_cleaned.dtypes, "\n")

print("Null counts after cleaning:")
print(df_cleaned.isnull().sum(), "\n")



def drop_low_scores(df, threshold):
    """Drop rows where score < threshold."""
    return df[df["score"] >= threshold]

# Use partial() to fix the threshold argument in pipe
df_final = df_cleaned.pipe(partial(drop_low_scores, threshold=85))

print(" Final DataFrame (scores >= 85):")
print(df_final, "\n")

print(" Data processing pipeline completed successfully!")
