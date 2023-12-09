import pandas as pd

from utils import csv_path

exitdata = pd.read_csv(
    "https://raw.githubusercontent.com/BenGoodair/childrens_social_care_data/main/Final_Data/outputs/enter_exit.csv",
    encoding="ISO-8859-1",
)


exitdata["Date"] = pd.to_datetime(exitdata["Date"], format="%d/%m/%Y")
exitdata["year"] = exitdata["Date"].dt.strftime("%Y")
exitdata["Sector"] = exitdata["Sector"].replace(
    {
        "Private": "For-profit",
        "Local Authority": "Local Authority",
        "Health Authority": "Local Authority",
        "Voluntary": "Third Sector",
    }
)
exitdata["leave_join"] = exitdata["leave_join"].replace(
    {"Leave": "Exits", "Join": "Entries"}
)


exitdata["Places"] = pd.to_numeric(exitdata["Places"], errors="coerce")
exitdata["childrens_homes"] = 1

exitdata = (
    exitdata.groupby(["Sector", "year", "leave_join", "Local.authority"])
    .agg(childrens_homes=("childrens_homes", "sum"), Places=("Places", "sum"))
    .reset_index()
)

all = (
    exitdata.groupby(["Sector", "year", "leave_join"])
    .agg(childrens_homes=("childrens_homes", "sum"), Places=("Places", "sum"))
    .reset_index()
)

all["Local.authority"] = "All"

exitdata = pd.concat([exitdata, all])


exitdata = pd.melt(
    exitdata,
    id_vars=["Sector", "Local.authority", "year", "leave_join"],
    value_vars=["childrens_homes", "Places"],
    var_name="Homes_or_places",
    value_name="value",
)

exitdata["Homes_or_places"] = exitdata["Homes_or_places"].replace(
    {"childrens_homes": "Children's homes"}
)


# exitdata.columns.tolist()


exitdata = exitdata[(exitdata["year"] != "2007") & (exitdata["year"] != "2008")]


# Convert 'value' column to numeric if needed
exitdata["value"] = pd.to_numeric(exitdata["value"], errors="coerce")

# Grouping by specified columns and calculating net change
grouped = (
    exitdata.groupby(["year", "Local.authority", "Homes_or_places", "Sector"])
    .apply(
        lambda x: x.loc[x["leave_join"] == "Entries", "value"].sum()
        - x.loc[x["leave_join"] == "Exits", "value"].sum()
    )
    .reset_index(name="value")
)

grouped["leave_join"] = "Net change"

grouped = grouped[
    (grouped["year"] != "2015")
    & (grouped["year"] != "2016")
    & (grouped["year"] != "2014")
]

# Creating a new DataFrame with the 'Net change' values
exitdata = pd.concat([exitdata, grouped])


exitdata = exitdata.sort_values(by="year")
exitdata = exitdata.sort_values(by="Local.authority")


exitdata["year"] = pd.Categorical(
    exitdata["year"],
    categories=[
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2023",
    ],
)

exitdata.to_csv(csv_path("exits"), index=False, header=True, encoding="utf-8")
