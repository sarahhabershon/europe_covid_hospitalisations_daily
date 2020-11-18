import pandas as pd 

#read in population and codes
pop = pd.read_csv("Europop.csv")
ecjrc_load = pd.read_csv("https://raw.githubusercontent.com/ec-jrc/COVID-19/master/data-by-country/jrc-covid-19-all-days-by-country.csv", parse_dates = ["Date"])

#set up ecjrc dataframe
ecjrc_load = ecjrc_load.drop(["lat", "lon"], axis = 1)
ecjrc_load = ecjrc_load.rename(columns={'NUTS': 'nuts'})

#remove countries where there is no hospitalisation data
ecjrc_load['sum'] = ecjrc_load['Hospitalized'].groupby(ecjrc_load['nuts']).transform('sum')
ecjrc_load = ecjrc_load[ecjrc_load["sum"] > 0]

#download latest hospitalisation figures as csv: https://coronavirus.data.gov.uk/details/healthcare, replace these files
uk_subt_load = pd.read_csv("uk_by_nation.csv", parse_dates = ["date"])
uk_nat_load = pd.read_csv("uk_total.csv", parse_dates = ["date"])

#add NUTS codes for UK - note that there is no nuts code for England; I have added that the population table as "UKXYZ" with the latest ONS population figure for England
uk_all = uk_subt_load.append(uk_nat_load)
uk_all = uk_all.rename(columns={"areaName": "CountryName", "date": "Date", "hospitalCases": "Hospitalized"}, errors="raise")
uk_all.loc[uk_all['CountryName'] == "Scotland", "nuts"] = "UKM"
uk_all.loc[uk_all['CountryName'] == "Wales", "nuts"] = "UKL"
uk_all.loc[uk_all['CountryName'] == "Northern Ireland", "nuts"] = "UKN"
uk_all.loc[uk_all['CountryName'] == "United Kingdom", "nuts"] = "UK"
uk_all.loc[uk_all['CountryName'] == "England", "nuts"] = "UKXYZ"

#add UK to the dataframe
ecjrc_load = ecjrc_load.append(uk_all)

#match with population table
matched = pd.merge(ecjrc_load,
                pop,
                on = "nuts",
                how = "inner")

#get the rolling average
matched["rolling_hosp"] = matched.groupby("nuts")['Hospitalized'].rolling(7).mean().reset_index(0,drop=True)
matched["rolling_hosp_per_100000"] = 100000*(matched["rolling_hosp"]/matched["population"])


#remove null values
matched = matched.dropna(axis=0, subset=["rolling_hosp"])

matched_hosp = matched[["Date", "CountryName", "Hospitalized", "rolling_hosp", "population", "rolling_hosp_per_100000"]]

matched_hosp.to_csv("rolling_hospitalisations.csv")