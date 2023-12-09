import pandas as pd

from utils import csv_path

ProviderData = pd.read_csv(
    "https://raw.githubusercontent.com/BenGoodair/childrens_social_care_data/main/Final_Data/outputs/Provider_data.csv",
    encoding="ISO-8859-1",
)

# Assuming you have your data in a DataFrame called ProviderData
ProviderData["date"] = pd.to_datetime(
    ProviderData["Registration.date"], format="%d/%m/%Y"
)
ProviderData["month"] = ProviderData["date"].dt.strftime("%m/%y")
ProviderData["time"] = (
    ProviderData["date"] - pd.to_datetime("2022-12-01")
).dt.days // 30

Providernobs = ProviderData.loc[
    ProviderData["Provision.type"] == "Children's home", ["time", "Sector", "URN"]
].drop_duplicates()
Providernobs = Providernobs.sort_values(by="time")
nobsByIdih = Providernobs.groupby(["time", "Sector"]).size().reset_index(name="nobs")
nobsprive = nobsByIdih[nobsByIdih["Sector"] == "Private"]
nobsvol = nobsByIdih[nobsByIdih["Sector"] == "Voluntary"]
nobsla = nobsByIdih[nobsByIdih["Sector"] == "Local Authority"]

# Assuming you have a variable cbPalette defined somewhere
# and it's a list of colors
cbPalette = ["color1", "color2", "color3"]

all = nobsla[["Sector"]].drop_duplicates()
all = all.loc[all.index.repeat(596)].reset_index(drop=True)
all["time"] = range(-595, 1)
all["er"] = 1
nobsla = pd.merge(nobsla, all, on=["Sector", "time"], how="outer").sort_values(
    by="time"
)
nobsla["nobs"].fillna(0, inplace=True)
nobsla["cumulative"] = nobsla["nobs"].cumsum()

all = nobsvol[["Sector"]].drop_duplicates()
all = all.loc[all.index.repeat(596)].reset_index(drop=True)
all["time"] = range(-595, 1)
all["er"] = 1
nobsvol = pd.merge(nobsvol, all, on=["Sector", "time"], how="outer").sort_values(
    by="time"
)
nobsvol["nobs"].fillna(0, inplace=True)
nobsvol["cumulative"] = nobsvol["nobs"].cumsum()

all = nobsprive[["Sector"]].drop_duplicates()
all = all.loc[all.index.repeat(596)].reset_index(drop=True)
all["time"] = range(-595, 1)
all["er"] = 1
nobsprive = pd.merge(nobsprive, all, on=["Sector", "time"], how="outer").sort_values(
    by="time"
)
nobsprive["nobs"].fillna(0, inplace=True)
nobsprive["cumulative"] = nobsprive["nobs"].cumsum()

nobs = pd.concat([nobsla, nobsvol, nobsprive])
nobs["Sector"] = nobs["Sector"].replace(
    {
        "Private": "For-profit",
        "Local Authority": "Local Authority",
        "Voluntary": "Third Sector",
    }
)

nobs = nobs[nobs["time"] > -227]  # Jan 2004

nobs["Local.authority"] = "All"


Providernobs = ProviderData[
    (ProviderData["Provision.type"] == "Children's home")
    & (~ProviderData["Local.authority"].isna())
]
Providernobs = Providernobs[
    ["time", "Sector", "URN", "Local.authority"]
].drop_duplicates()

nobsByIdih = (
    Providernobs.groupby(["time", "Local.authority", "Sector"])
    .size()
    .reset_index(name="nobs")
)

nobsprive = nobsByIdih[nobsByIdih["Sector"] == "Private"]
nobsvol = nobsByIdih[nobsByIdih["Sector"] == "Voluntary"]
nobsla = nobsByIdih[nobsByIdih["Sector"] == "Local Authority"]

unique_local_authorities = nobsla["Local.authority"].unique()
times = list(range(-595, 1))
all_data = pd.DataFrame(
    {
        "Sector": "Private",
        "Local.authority": [
            local_authority
            for local_authority in unique_local_authorities
            for _ in times
        ],
        "time": [time for _ in unique_local_authorities for time in times],
        "er": 1,
    }
)


nobsprive = pd.merge(
    all_data, nobsprive, on=["Sector", "time", "Local.authority"], how="left"
)
nobsprive = nobsprive.sort_values("time").fillna(0)  # Fill NaNs with 0
nobsprive["cumulative"] = nobsprive.groupby("Local.authority")["nobs"].cumsum()


all_data["Sector"] = "Local Authority"
nobsla = pd.merge(
    all_data, nobsla, on=["Sector", "time", "Local.authority"], how="left"
)
nobsla = nobsla.sort_values("time").fillna(0)  # Fill NaNs with 0
nobsla["cumulative"] = nobsla.groupby("Local.authority")["nobs"].cumsum()

all_data["Sector"] = "Voluntary"
nobsvol = pd.merge(
    all_data, nobsvol, on=["Sector", "time", "Local.authority"], how="left"
)
nobsvol = nobsvol.sort_values("time").fillna(0)  # Fill NaNs with 0
nobsvol["cumulative"] = nobsvol.groupby("Local.authority")["nobs"].cumsum()

nobs2 = pd.concat([nobsla, nobsvol, nobsprive], ignore_index=True)
nobs2["Sector"] = pd.Categorical(
    nobs2["Sector"], categories=["Private", "Local Authority", "Voluntary"]
)
nobs2["Sector"] = nobs2["Sector"].cat.rename_categories(
    ["For-profit", "Local Authority", "Third Sector"]
)

nobs2 = nobs2[nobs2["time"] > -227]  # Jan 2004


nobs_fin = pd.concat([nobs2, nobs])

nobs_fin["Homes or places"] = "Homes"


Providernobs = ProviderData.loc[
    ProviderData["Provision.type"] == "Children's home",
    ["time", "Sector", "URN", "Places"],
].drop_duplicates()
Providernobs = Providernobs.sort_values(by="time")
nobsByIdih = Providernobs.groupby(["time", "Sector"])["Places"].sum().reset_index()
nobsprive = nobsByIdih[nobsByIdih["Sector"] == "Private"]
nobsvol = nobsByIdih[nobsByIdih["Sector"] == "Voluntary"]
nobsla = nobsByIdih[nobsByIdih["Sector"] == "Local Authority"]

# Assuming you have a variable cbPalette defined somewhere
# and it's a list of colors
cbPalette = ["color1", "color2", "color3"]

all = nobsla[["Sector"]].drop_duplicates()
all = all.loc[all.index.repeat(596)].reset_index(drop=True)
all["time"] = range(-595, 1)
all["er"] = 1
nobsla = pd.merge(nobsla, all, on=["Sector", "time"], how="outer").sort_values(
    by="time"
)
nobsla["Places"].fillna(0, inplace=True)
nobsla["cumulative"] = nobsla["Places"].cumsum()

all = nobsvol[["Sector"]].drop_duplicates()
all = all.loc[all.index.repeat(596)].reset_index(drop=True)
all["time"] = range(-595, 1)
all["er"] = 1
nobsvol = pd.merge(nobsvol, all, on=["Sector", "time"], how="outer").sort_values(
    by="time"
)
nobsvol["Places"].fillna(0, inplace=True)
nobsvol["cumulative"] = nobsvol["Places"].cumsum()

all = nobsprive[["Sector"]].drop_duplicates()
all = all.loc[all.index.repeat(596)].reset_index(drop=True)
all["time"] = range(-595, 1)
all["er"] = 1
nobsprive = pd.merge(nobsprive, all, on=["Sector", "time"], how="outer").sort_values(
    by="time"
)
nobsprive["Places"].fillna(0, inplace=True)
nobsprive["cumulative"] = nobsprive["Places"].cumsum()

nobs = pd.concat([nobsla, nobsvol, nobsprive])
nobs["Sector"] = nobs["Sector"].replace(
    {
        "Private": "For-profit",
        "Local Authority": "Local Authority",
        "Voluntary": "Third Sector",
    }
)

nobs = nobs[nobs["time"] > -227]  # Jan 2004

nobs["Local.authority"] = "All"


Providernobs = ProviderData[
    (ProviderData["Provision.type"] == "Children's home")
    & (~ProviderData["Local.authority"].isna())
]
Providernobs = Providernobs[
    ["time", "Sector", "URN", "Local.authority", "Places"]
].drop_duplicates()

nobsByIdih = (
    Providernobs.groupby(["time", "Local.authority", "Sector"])["Places"]
    .sum()
    .reset_index()
)


nobsprive = nobsByIdih[nobsByIdih["Sector"] == "Private"]
nobsvol = nobsByIdih[nobsByIdih["Sector"] == "Voluntary"]
nobsla = nobsByIdih[nobsByIdih["Sector"] == "Local Authority"]

unique_local_authorities = nobsla["Local.authority"].unique()
times = list(range(-595, 1))
all_data = pd.DataFrame(
    {
        "Sector": "Private",
        "Local.authority": [
            local_authority
            for local_authority in unique_local_authorities
            for _ in times
        ],
        "time": [time for _ in unique_local_authorities for time in times],
        "er": 1,
    }
)


nobsprive = pd.merge(
    all_data, nobsprive, on=["Sector", "time", "Local.authority"], how="left"
)
nobsprive = nobsprive.sort_values("time").fillna(0)  # Fill NaNs with 0
nobsprive["cumulative"] = nobsprive.groupby("Local.authority")["Places"].cumsum()


all_data["Sector"] = "Local Authority"
nobsla = pd.merge(
    all_data, nobsla, on=["Sector", "time", "Local.authority"], how="left"
)
nobsla = nobsla.sort_values("time").fillna(0)  # Fill NaNs with 0
nobsla["cumulative"] = nobsla.groupby("Local.authority")["Places"].cumsum()

all_data["Sector"] = "Voluntary"
nobsvol = pd.merge(
    all_data, nobsvol, on=["Sector", "time", "Local.authority"], how="left"
)
nobsvol = nobsvol.sort_values("time").fillna(0)  # Fill NaNs with 0
nobsvol["cumulative"] = nobsvol.groupby("Local.authority")["Places"].cumsum()

nobs2 = pd.concat([nobsla, nobsvol, nobsprive], ignore_index=True)
nobs2["Sector"] = pd.Categorical(
    nobs2["Sector"], categories=["Private", "Local Authority", "Voluntary"]
)
nobs2["Sector"] = nobs2["Sector"].cat.rename_categories(
    ["For-profit", "Local Authority", "Third Sector"]
)

nobs2 = nobs2[nobs2["time"] > -227]  # Jan 2004


nobs_fin2 = pd.concat([nobs2, nobs])

nobs_fin2["Homes or places"] = "Places"


nobs_final = pd.concat([nobs_fin, nobs_fin2]).sort_values(by="Local.authority")

nobs_final.to_csv(csv_path("nobs"), index=False, header=True, encoding="utf-8")
