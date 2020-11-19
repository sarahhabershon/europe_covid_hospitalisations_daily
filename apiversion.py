from requests import get
import pandas as pd

uk = ["overview", "United Kingdom"]
nations = ["England", "Northern Ireland", "Wales", "Scotland"]

def get_data(areatype, nation):
    endpoint = (
    'https://api.coronavirus.data.gov.uk/v1/data?'
    'filters=areaType=' + areatype + ';areaName=' + nation + '&'
    'structure={"date":"date","Hospitalized":"hospitalCases"}'
)

    response = get(endpoint, timeout=10)
    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: { response.text }')
        
    return response.json()

u_k = get_data(uk[0], uk[1])["data"]
uk_all = pd.all(u_k)
uk_all["CountryName"] = uk[1]
uk_all = uk_all.rename(columns={'date': 'Date'})


for nation in nations:
    print(nation)
    areatype = "nation"
    data = get_data(areatype, nation)
    nation_data = data["data"]
    df = pd.all(nation_data)
    df["CountryName"] = nation
    df = df.rename(columns={'date': 'Date'})
    uk_all = uk_all.append(df)

uk_all.to_csv("testingapi.csv")
    # Nation data (England, Northern Ireland, Scotland, and Wales)