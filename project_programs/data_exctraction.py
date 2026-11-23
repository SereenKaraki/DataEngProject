import pandas as pd
import requests
import json

url = "https://api.restcountries.com/countries/v5"

# setting up the API request
# response_fields accepts the country feautures we need

# the limit takes in the limit of the number of countries we can retrieve with each API requests, Countries REST
#only accepts a 100 countries per each request

# offset tells the API where to start retrieving countries and how many countries to skip with each call
# we start with 0 as we want it to retrieve from the start
params = {
    "response_fields": "names.common,codes.alpha_3,region,population,area.kilometers,languages,currencies,borders",
    "limit": 100,
    "offset": 0
}

# headers accept the API key that will allow us to make requests
headers = {"Authorization": "Bearer rc_live_4d9fbaf925a24212a15b65cddb89225e"}

countries = []

while True:
    response = requests.get(url, headers=headers, params=params) # sends the API request
    json_data = response.json() # converts the API response into a Python object
    data = json_data["data"] # accessing the values associated with the 'data' key retrieved from the API

    countries.extend(data["objects"])  # data['objects'] accesses the list of countries stored under the 'objects' key
                                      # and then are added to the countries list

    if not data["meta"]["more"]: # indentifies whether more country records are available to be pulled
        break                    # breaks the loops if no more country records are left ( we retrieved all the countries )

    params["offset"] += 100 # skips the previously retrieved 100 countries, so 1st call: 0-100  2md call: 100-200  3rd call: 200-254

print("Total countries:", len(countries))

df = pd.json_normalize(countries, sep="_")

# converts lists into comma-separated strings( csv ) and flattens the json fields into a structured tabular dataset
df["borders"] = df["borders"].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")

df["currencies"] = df["currencies"].apply(lambda x: ", ".join(c["name"] for c in x) if isinstance(x, list) else "")

df["languages"] = df["languages"].apply(lambda x: ", ".join(l["bcp47"] for l in x) if isinstance(x, list) else "")

df = df[[
    "names_common",
    "codes_alpha_3",
    "region",
    "population",
    "area_kilometers",
    "borders",
    "currencies",
    "languages"
]]

raw_countries = df.to_dict(orient="records")

with open("raw_countries_.json", "w", encoding="utf-8") as file:
    json.dump(raw_countries, file, indent=4, ensure_ascii=False)

df = df.set_index("names_common")

print(df.head())
