
import pandas as pd
import requests
import json

url = "https://api.restcountries.com/countries/v5"

params = {
    "response_fields": "names.common,region,population,area.kilometers,languages,currencies,borders",
    "limit": 100,
    "offset": 0
}

headers = {
    "Authorization": "Bearer rc_live_4d9fbaf925a24212a15b65cddb89225e"
}

countries = []

while True:
    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()
    data = json_data["data"]

    countries.extend(data["objects"])

    if not data["meta"]["more"]:
        break

    params["offset"] += 100

print("Total countries:", len(countries))


with open("raw_countries.json", "w", encoding="utf-8") as raw_file:
    json.dump(countries, raw_file, indent=4, ensure_ascii=False)

df = pd.json_normalize(countries, sep="_")

df["borders"] = df["borders"].apply(
    lambda x: ", ".join(x) if isinstance(x, list) else ""
)

df["currencies"] = df["currencies"].apply(
    lambda x: ", ".join(c["name"] for c in x) if isinstance(x, list) else ""
)

df["languages"] = df["languages"].apply(
    lambda x: ", ".join(l["bcp47"] for l in x) if isinstance(x, list) else ""
)

df = df[[
    "names_common",
    "region",
    "population",
    "area_kilometers",
    "borders",
    "currencies",
    "languages"
]]

flattened_countries = df.to_dict(orient="records")

with open("flattened_countries.json", "w", encoding="utf-8") as file:
    json.dump(flattened_countries, file, indent=4, ensure_ascii=False)

df = df.set_index("names_common")

print(df.head())
