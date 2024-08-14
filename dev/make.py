import os
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

__dir = os.path.dirname(os.path.realpath(__file__))

endpoint = "https://query.wikidata.org/sparql"

sparql = SPARQLWrapper(endpoint)
sparql.setReturnFormat(JSON)

with open(__dir + "/current_population.sparql", "r") as f:
    query = f.read()
sparql.setQuery(query)

country_data_raw = sparql.query().convert()
df_raw = pd.json_normalize(country_data_raw["results"]["bindings"])
df = df_raw[["itemLabel.value", "population.value"]]

_transform = {
    "itemLabel.value": "country",
    "population.value": "population"
}
df = df.rename(columns=_transform)
df.to_csv(os.path.join(__dir, "../population.csv"), index=False)