from requests import get
import pandas as pd




nations = ["England", "Northern Ireland", "Wales", "Scotland"]

def get_data(x):
    endpoint = (
    'https://api.coronavirus.data.gov.uk/v1/data?'
    'filters=areaType=nation;areaName=' + x + '&'
    'structure={"date":"date","Hospitalized":"hospitalCases"}'
)

    response = get(endpoint, timeout=10)
    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: { response.text }')
        
    return response.json()



for nation in nations:
    print(nation)
    data = get_data(nation)
    nation_data = data["data"]
    df = pd.DataFrame(nation_data)
    df["CountryName"] = nation
    df = df.rename(columns={'date': 'Date'})
    print(df)



    # Nation data (England, Northern Ireland, Scotland, and Wales)