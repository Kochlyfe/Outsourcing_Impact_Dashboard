import pandas as pd
import geopandas as gpd

from utils import csv_path, geojson_path


la_df = pd.read_csv(
    "https://raw.githubusercontent.com/BenGoodair/childrens_social_care_data/main/Final_Data/outputs/dashboard_data.csv"
)
la_df["percent"] = pd.to_numeric(la_df["percent"], errors="coerce")
la_df.sort_values(by="LA_Name", ascending=True, inplace=True)

df2022 = la_df[la_df["year"] == 2022]

# Rename columns
uaboundaries = gpd.read_file(
    "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_December_2022_UK_BUC/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
)
uaboundaries = uaboundaries.rename(
    columns={"CTYUA22CD": "LA_Code", "CTYUA22NM": "lad19nm", "CTYUA22NMW": "lad19nmw"}
)

# Filter out unwanted data
uaboundaries = uaboundaries[~uaboundaries["lad19nm"].isin(["Wales", "Scotland"])]
uaboundaries = uaboundaries[uaboundaries["LA_Code"].str.startswith("E")]


merged = uaboundaries.set_index("LA_Code").join(df2022.set_index("LA_Code"))
# merged = merged.reset_index()
# merged.head()


# customdata = np.stack((df2021['geog_n'], df2021['CLA_Mar'], df2021['per_for_profit'], df2021['Private_spend'], df2021['Total_spend']), axis=-1)

merged = merged.dropna(subset=["LA_Name"])

merged = merged.round(decimals=2)

merged2 = merged[
    (merged["variable"] == "Private provision")
    | (
        (merged["variable"] == "Total Children Looked After")
        & (merged["subcategory"] == "For_profit")
    )
    | ((merged["variable"] == "Places") & (merged["subcategory"] == "Private"))
]

merged2.loc[
    (merged2["variable"] == "Places") & (merged2["subcategory"] == "Private"),
    "variable",
] = "For-profit Children's Homes Places (%, 2023)"
merged2.loc[
    merged2["variable"] == "Private provision", "variable"
] = "For-profit Placements (%, 2022)"
merged2.loc[
    (merged2["variable"] == "Total Children Looked After")
    & (merged2["subcategory"] == "For_profit"),
    "variable",
] = "For-profit Expenditure (%, 2022)"

outcomes_df = la_df[
    (la_df["subcategory"] == "health and criminalisation")
    | (la_df["subcategory"] == "ks2")
    | (la_df["subcategory"] == "ks4")
    | (la_df["subcategory"] == "key stage 2")
    | (la_df["subcategory"] == "key stage 4")
    | (la_df["subcategory"] == "school absence")
    | (la_df["subcategory"] == "school exclusion")
    | (la_df["subcategory"] == "missing incidents")
    | (la_df["subcategory"] == "Reason episode ceased")
    | (la_df["category"] == "care leavers")
]


# outcomes_df['variable'].value_counts()
# outcomes_df[outcomes_df['category'] == 'care leavers']['year'].value_counts().sort_index()
# outcomes_df[(outcomes_df['category'] == 'care leavers') & (outcomes_df['year'] == 2014)]
# la_df[(la_df['category'] == 'Expenditure') & (la_df['year'] == 2014)]


outcomes_df = outcomes_df[
    (outcomes_df["variable"] == "sess_unauthorised")  # unauthorised absence
    | (outcomes_df["variable"] == "one_plus_sus")  # suspension
    | (outcomes_df["variable"] == "pupils_pa_10_exact")  # persitent absence
    | (outcomes_df["variable"] == "rwm_met_expected_standard")
    | (outcomes_df["variable"] == "gps_met_expected_standard")
    | (outcomes_df["variable"] == "writta_met_expected_standard")
    | (outcomes_df["variable"] == "read_met_expected_standard")
    | (outcomes_df["variable"] == "mat_met_expected_standard")
    | (outcomes_df["variable"] == "p8score")
    | (outcomes_df["variable"] == "att8")
    | (outcomes_df["variable"] == "Accommodation considered suitable")
    | (outcomes_df["variable"] == "Local authority not in touch with care leaver")
    | (outcomes_df["variable"] == "Total not in education employment or training")
    | (
        outcomes_df["variable"]
        == "Not in education training or employment, owing to other reasons"
    )
    | (outcomes_df["variable"] == "Total information not known")
    | (outcomes_df["variable"] == "Independent living")
    | (outcomes_df["variable"] == "In custody")
    | (
        outcomes_df["variable"]
        == "Percentage of children who had a missing incident during the year"
    )
    | (
        outcomes_df["variable"]
        == "Percentage of children who were away from placement without authorisation during the year"
    )
    | (outcomes_df["subcategory"] == "Reason episode ceased")
    | (outcomes_df["subcategory"] == "health and criminalisation")
]


outcomes_df = outcomes_df[
    (outcomes_df["variable"] != "Total")
    & (outcomes_df["variable"] != "Total ages 0 to 4 years")
    & (outcomes_df["variable"] != "Total all ages")
    & (outcomes_df["variable"] != "Total ages 10 to 17 years")
    & (outcomes_df["variable"] != "Total ages 5 to 16 years")
]


outcomes_df["LA_Name"].value_counts()


outcomes_df.loc[outcomes_df["subcategory"] == "ks2", "subcategory"] = "Key stage 2"
outcomes_df.loc[
    outcomes_df["subcategory"] == "key stage 2", "subcategory"
] = "Key stage 2"
outcomes_df.loc[outcomes_df["subcategory"] == "ks4", "subcategory"] = "Key stage 4"
outcomes_df.loc[
    outcomes_df["subcategory"] == "key stage 4", "subcategory"
] = "Key stage 4"
outcomes_df.loc[
    outcomes_df["subcategory"] == "health and criminalisation", "subcategory"
] = "Health and criminalisation"
outcomes_df.loc[
    outcomes_df["subcategory"] == "school absence", "subcategory"
] = "School absence"
outcomes_df.loc[
    outcomes_df["subcategory"] == "school exclusion", "subcategory"
] = "School absence"
outcomes_df.loc[
    outcomes_df["subcategory"] == "19 to 21 years", "subcategory"
] = "Care leavers (19 to 21)"
outcomes_df.loc[
    outcomes_df["subcategory"] == "Aged 19 to 21", "subcategory"
] = "Care leavers (19 to 21)"
outcomes_df.loc[
    outcomes_df["subcategory"] == "Aged 17 to 18", "subcategory"
] = "Care leavers (17 to 18)"
outcomes_df.loc[
    outcomes_df["subcategory"] == "17 to 18 years", "subcategory"
] = "Care leavers (17 to 18)"


outcomes_df["subcategory"].value_counts()


outcomes_df.loc[
    outcomes_df["variable"] == "pupils_pa_10_exact", "variable"
] = "Persistent absence"
outcomes_df.loc[
    outcomes_df["variable"] == "sess_unauthorised", "variable"
] = "Unauthorised absent sessions"
outcomes_df.loc[
    outcomes_df["variable"] == "mat_met_expected_standard", "variable"
] = "Met expected grades (Maths)"
outcomes_df.loc[
    outcomes_df["variable"] == "gps_met_expected_standard", "variable"
] = "Met expected grades (Grammar, punctuation and spelling)"
outcomes_df.loc[
    outcomes_df["variable"] == "read_met_expected_standard", "variable"
] = "Met expected grades (Reading)"
outcomes_df.loc[
    outcomes_df["variable"] == "writta_met_expected_standard", "variable"
] = "Met expected grades (Writting)"
outcomes_df.loc[
    outcomes_df["variable"] == "rwm_met_expected_standard", "variable"
] = "Met expected grades (Reading, writing & maths)"
outcomes_df.loc[
    outcomes_df["variable"] == "p8score", "variable"
] = "Average progress 8 score"
outcomes_df.loc[
    outcomes_df["variable"] == "att8", "variable"
] = "Average attainment 8 score"
outcomes_df.loc[
    outcomes_df["variable"]
    == "Percentage of children who were away from placement without authorisation during the year",
    "variable",
] = "Away from placement during year"
outcomes_df.loc[
    outcomes_df["variable"]
    == "Percentage of children who had a missing incident during the year",
    "variable",
] = "Missing from placement during year"
outcomes_df.loc[
    outcomes_df["variable"] == "one_plus_sus", "variable"
] = "At least one suspension"
outcomes_df.loc[
    outcomes_df["variable"] == "Total information not known", "variable"
] = "Employment or education status not known"
outcomes_df.loc[
    outcomes_df["variable"]
    == "Not in education training or employment, owing to other reasons",
    "variable",
] = "Not in education training or employment, for other reasons than illness, pregnancy or parenthood"

outcomes_df.loc[
    outcomes_df["variable"] == "Away from placement during year", "percent"
] = outcomes_df["number"]
outcomes_df.loc[
    outcomes_df["variable"] == "Missing from placement during year", "percent"
] = outcomes_df["number"]


outcomes_df = outcomes_df.dropna(subset=["percent"])

outcomes_df["LA_Name"].value_counts()


# keep only LAs with a 100 obs

outcomes_df = outcomes_df[
    outcomes_df["LA_Name"].map(outcomes_df["LA_Name"].value_counts()) > 100
]

outcomes_df["percent"] = pd.to_numeric(outcomes_df["percent"], errors="coerce")


#####placements quality#####


placements_df = la_df[
    (
        la_df["subcategory"]
        == "Distance between home and placement and locality of placement"
    )
    | (la_df["subcategory"] == "Reason for placement change during the year")
    | (la_df["subcategory"] == "Place providers")
    | (la_df["subcategory"] == "Locality of placement")
    | (la_df["subcategory"] == "LA of placement")
    | (la_df["subcategory"] == "Distance between home and placement")
    | (la_df["subcategory"] == "Mid-year moves")
    | (la_df["subcategory"] == "placement stability")  # |
    # (la_df['subcategory'] == 'Placed inside the local authority boundary')
]


placements_df["variable"].value_counts()

placements_df = placements_df[
    (placements_df["variable"] != "Total")
    & (placements_df["variable"] != "Total placements changing")
    & (placements_df["variable"] != "Total children")
]


placements_df = placements_df.dropna(subset=["percent"])

placements_df["LA_Name"].value_counts()

placements_df = placements_df[
    placements_df["LA_Name"].map(placements_df["LA_Name"].value_counts()) > 104
]

placements_df["percent"] = pd.to_numeric(placements_df["percent"], errors="coerce")


variable_options = []  # No options if no subcategory is selected
variable_options2 = []  # No options if no subcategory is selected


Outcomes = outcomes_df
Expenditure = la_df[(la_df["category"] == "Expenditure")]
Expenditure.rename(columns={"subcategory": "newsubcatname", "variable": "newvarmame"})
Expenditure.rename(columns={"newsubcatname": "variable", "newvarmame": "subcategory"})
Placements = placements_df


Outcomes.to_csv(csv_path("outcomes"), index=False, header=True, encoding="utf-8")
Expenditure.to_csv(csv_path("expenditures"), index=False, header=True, encoding="utf-8")
Placements.to_csv(csv_path("placements"), index=False, header=True, encoding="utf-8")
la_df.to_csv(csv_path("la"), index=False, header=True, encoding="utf-8")
merged2.to_file(geojson_path("merged"), driver="GeoJSON")
