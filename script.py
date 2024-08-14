import pandas as pd

df = pd.read_csv("population.csv")

sum = df["population"].sum()

print(f"Total population: {sum}")

df = pd.read_csv("remote_data/speakers_revised.csv")
df["percentage"] = df["speakers"] / sum * 100

df.to_csv("results.csv", index=False)
print(df.head(10))