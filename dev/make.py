import os
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

__dir = os.path.dirname(os.path.realpath(__file__))

def query_wikidata(queryPath: str) -> pd.DataFrame:
    endpoint = "https://query.wikidata.org/sparql"

    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)

    with open(queryPath, "r") as f:
        query = f.read()
    sparql.setQuery(query)

    country_data_raw = sparql.query().convert()
    return pd.json_normalize(country_data_raw["results"]["bindings"])

df_raw = query_wikidata(__dir + "/current_population.sparql")
df = df_raw[["countryLabel.value", "latestPopulation.value"]]

_transform = {
    "countryLabel.value": "country",
    "latestPopulation.value": "population"
}

df = df.rename(columns=_transform)
df.to_csv(os.path.join(__dir, "../population.csv"), index=False)

df_raw = query_wikidata(__dir + "/spoken_languages.sparql")
groups = df_raw.groupby("itemLabel.value")
result_df = pd.DataFrame()

for key, group in groups:
    max = group["date.value"].max()
    group = group.drop(group[group["date.value"] != max].index)
    group["speakers"] = pd.to_numeric(group["speakers.value"]).sum()
    result_df = pd.concat([result_df, group], ignore_index=False)
df = result_df[["itemLabel.value", "speakers"]].drop_duplicates()

_transform = {
    "itemLabel.value": "language"
}

df = df.rename(columns=_transform)
df.to_csv(os.path.join(__dir, "../remote_data/speakers.csv"), index=False)

df = df.query("speakers > 100_000_000")
df.to_csv(os.path.join(__dir, "../remote_data/speakers_revised.csv"), index=False)