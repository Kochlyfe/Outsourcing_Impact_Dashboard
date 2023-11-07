


from dash import Dash, State, html, dash_table, dcc, callback, Output, Input
import pandas as pd


import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

#import cdstoolbox as ct
#import chart_studio.plotly as py

import chart_studio.plotly as py
import dash_bootstrap_components as dbc
import plotly.express as px

from plotly.colors import sequential


# # Define a custom color scale with more variations, ending in red
# custom_color_scale = [
#     (i, color) for i, color in zip(
#         range(0, 110, 10),
#         sequential.Viridis
#     )
# ] + [(100, 'red')]  # Red for the highest value



pd.set_option('display.max_rows', None)


####HEALTHY CAKES####


#la_df = pd.read_csv("https://raw.githubusercontent.com/BenGoodair/Outsourcing_Impact_Dashboard/main/Data/dashboard_LA_data.csv")
la_df = pd.read_csv("https://raw.githubusercontent.com/BenGoodair/childrens_social_care_data/main/Final_Data/outputs/dashboard_data.csv")
la_df['percent'] = pd.to_numeric(la_df['percent'], errors='coerce')
la_df.sort_values(by='LA_Name', ascending=True, inplace=True)


import plotly.colors as colors














####Need to come back to this when i Have children's homes % for each LA for the map####


import geopandas as gpd
df2022 = la_df[la_df['year'] == 2022]

#df2022[df2022['LA_Code'] == 'E06000017']
#df2022[(df2022['subcategory'] =='Private')]
#uaboundaries[uaboundaries['lad19nm'] == 'Rutland']



#df2022.loc[df2022['LA_Code'] == 'E06000060', 'LA_Code'] = 'E10000002'

# Rename columns
uaboundaries = gpd.read_file("https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_December_2022_UK_BUC/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson")
uaboundaries = uaboundaries.rename(columns={"CTYUA22CD": "LA_Code", "CTYUA22NM": "lad19nm", "CTYUA22NMW": "lad19nmw"})

# Filter out unwanted data
uaboundaries = uaboundaries[~uaboundaries["lad19nm"].isin(["Wales", "Scotland"])]
uaboundaries = uaboundaries[uaboundaries["LA_Code"].str.startswith('E')]



merged = uaboundaries.set_index('LA_Code').join(df2022.set_index('LA_Code'))
#merged = merged.reset_index()
#merged.head()


#customdata = np.stack((df2021['geog_n'], df2021['CLA_Mar'], df2021['per_for_profit'], df2021['Private_spend'], df2021['Total_spend']), axis=-1)

merged = merged.dropna(subset=['LA_Name'])

merged = merged.round(decimals=2)

merged2 = merged[(merged['variable'] == 'Private provision') | 
((merged['variable'] == 'Total Children Looked After') & (merged['subcategory'] == "For_profit"))|
((merged['variable'] == 'Places') & (merged['subcategory'] == "Private"))
]

merged2.loc[(merged2['variable'] == 'Places') & (merged2['subcategory'] == "Private"), 'variable'] = "For-profit Children's Homes Places (%, 2023)"
merged2.loc[merged2['variable'] == 'Private provision', 'variable'] = "For-profit Placements (%, 2022)"
merged2.loc[(merged2['variable'] == 'Total Children Looked After') & (merged2['subcategory'] == "For_profit"), 'variable'] = "For-profit Expenditure (%, 2022)"
   
































####outcomes####

#outcomes_df = la_df_long

#outcomes_df = outcomes_df.groupby(['year']).mean().reset_index()

##### provider bars #####

ProviderData = pd.read_csv("https://raw.githubusercontent.com/BenGoodair/childrens_social_care_data/main/Final_Data/outputs/Provider_data.csv", encoding='ISO-8859-1')
import pandas as pd

# Assuming you have your data in a DataFrame called ProviderData
ProviderData['date'] = pd.to_datetime(ProviderData['Registration.date'], format="%d/%m/%Y")
ProviderData['month'] = ProviderData['date'].dt.strftime('%m/%y')
ProviderData['time'] = (ProviderData['date'] - pd.to_datetime("2022-12-01")).dt.days // 30

Providernobs = ProviderData.loc[ProviderData['Provision.type'] == "Children's home", ["time", "Sector", "URN"]].drop_duplicates()
Providernobs = Providernobs.sort_values(by="time")
nobsByIdih = Providernobs.groupby(['time', 'Sector']).size().reset_index(name='nobs')
nobsprive = nobsByIdih[nobsByIdih['Sector'] == 'Private']
nobsvol = nobsByIdih[nobsByIdih['Sector'] == 'Voluntary']
nobsla = nobsByIdih[nobsByIdih['Sector'] == 'Local Authority']

# Assuming you have a variable cbPalette defined somewhere
# and it's a list of colors
cbPalette = ['color1', 'color2', 'color3']

all = nobsla[['Sector']].drop_duplicates()
all = all.loc[all.index.repeat(596)].reset_index(drop=True)
all['time'] = range(-595, 1)
all['er'] = 1
nobsla = pd.merge(nobsla, all, on=['Sector', 'time'], how='outer').sort_values(by="time")
nobsla['nobs'].fillna(0, inplace=True)
nobsla['cumulative'] = nobsla['nobs'].cumsum()

all = nobsvol[['Sector']].drop_duplicates()
all = all.loc[all.index.repeat(596)].reset_index(drop=True)
all['time'] = range(-595, 1)
all['er'] = 1
nobsvol = pd.merge(nobsvol, all, on=['Sector', 'time'], how='outer').sort_values(by="time")
nobsvol['nobs'].fillna(0, inplace=True)
nobsvol['cumulative'] = nobsvol['nobs'].cumsum()

all = nobsprive[['Sector']].drop_duplicates()
all = all.loc[all.index.repeat(596)].reset_index(drop=True)
all['time'] = range(-595, 1)
all['er'] = 1
nobsprive = pd.merge(nobsprive, all, on=['Sector', 'time'], how='outer').sort_values(by="time")
nobsprive['nobs'].fillna(0, inplace=True)
nobsprive['cumulative'] = nobsprive['nobs'].cumsum()

nobs = pd.concat([nobsla, nobsvol, nobsprive])
nobs['Sector'] = nobs['Sector'].replace({"Private": "For-profit", "Local Authority": "Local Authority", "Voluntary": "Third Sector"})

nobs = nobs[nobs['time'] > -227] #Jan 2004

nobs["Local.authority"]= "All"


Providernobs = ProviderData[(ProviderData['Provision.type'] == "Children's home") & (~ProviderData['Local.authority'].isna())]
Providernobs = Providernobs[['time', 'Sector', 'URN', 'Local.authority']].drop_duplicates()

nobsByIdih = Providernobs.groupby(['time', 'Local.authority', 'Sector']).size().reset_index(name='nobs')

nobsprive = nobsByIdih[nobsByIdih['Sector'] == "Private"]
nobsvol = nobsByIdih[nobsByIdih['Sector'] == "Voluntary"]
nobsla = nobsByIdih[nobsByIdih['Sector'] == "Local Authority"]

unique_local_authorities = nobsla['Local.authority'].unique()
times = list(range(-595, 1))
all_data = pd.DataFrame({
    'Sector': 'Private',
    'Local.authority': [local_authority for local_authority in unique_local_authorities for _ in times],
    'time': [time for _ in unique_local_authorities for time in times],
    'er': 1
})


nobsprive = pd.merge(all_data, nobsprive, on=['Sector', 'time', 'Local.authority'], how='left')
nobsprive = nobsprive.sort_values('time').fillna(0)  # Fill NaNs with 0
nobsprive['cumulative'] = nobsprive.groupby('Local.authority')['nobs'].cumsum()


all_data['Sector'] = 'Local Authority'
nobsla = pd.merge(all_data, nobsla, on=['Sector', 'time', 'Local.authority'], how='left')
nobsla = nobsla.sort_values('time').fillna(0)  # Fill NaNs with 0
nobsla['cumulative'] = nobsla.groupby('Local.authority')['nobs'].cumsum()

all_data['Sector'] = 'Voluntary'
nobsvol = pd.merge(all_data, nobsvol, on=['Sector', 'time', 'Local.authority'], how='left')
nobsvol = nobsvol.sort_values('time').fillna(0)  # Fill NaNs with 0
nobsvol['cumulative'] = nobsvol.groupby('Local.authority')['nobs'].cumsum()

nobs2 = pd.concat([nobsla, nobsvol, nobsprive], ignore_index=True)
nobs2['Sector'] = pd.Categorical(nobs2['Sector'], categories=['Private', 'Local Authority', 'Voluntary'])
nobs2['Sector'] = nobs2['Sector'].cat.rename_categories(['For-profit', 'Local Authority', 'Third Sector'])

nobs2 = nobs2[nobs2['time'] > -227] #Jan 2004


nobs_fin = pd.concat([nobs2, nobs])

nobs_fin['Homes or places']= "Homes"









Providernobs = ProviderData.loc[ProviderData['Provision.type'] == "Children's home", ["time", "Sector", "URN", "Places"]].drop_duplicates()
Providernobs = Providernobs.sort_values(by="time")
nobsByIdih = Providernobs.groupby(['time', 'Sector'])['Places'].sum().reset_index()
nobsprive = nobsByIdih[nobsByIdih['Sector'] == 'Private']
nobsvol = nobsByIdih[nobsByIdih['Sector'] == 'Voluntary']
nobsla = nobsByIdih[nobsByIdih['Sector'] == 'Local Authority']

# Assuming you have a variable cbPalette defined somewhere
# and it's a list of colors
cbPalette = ['color1', 'color2', 'color3']

all = nobsla[['Sector']].drop_duplicates()
all = all.loc[all.index.repeat(596)].reset_index(drop=True)
all['time'] = range(-595, 1)
all['er'] = 1
nobsla = pd.merge(nobsla, all, on=['Sector', 'time'], how='outer').sort_values(by="time")
nobsla['Places'].fillna(0, inplace=True)
nobsla['cumulative'] = nobsla['Places'].cumsum()

all = nobsvol[['Sector']].drop_duplicates()
all = all.loc[all.index.repeat(596)].reset_index(drop=True)
all['time'] = range(-595, 1)
all['er'] = 1
nobsvol = pd.merge(nobsvol, all, on=['Sector', 'time'], how='outer').sort_values(by="time")
nobsvol['Places'].fillna(0, inplace=True)
nobsvol['cumulative'] = nobsvol['Places'].cumsum()

all = nobsprive[['Sector']].drop_duplicates()
all = all.loc[all.index.repeat(596)].reset_index(drop=True)
all['time'] = range(-595, 1)
all['er'] = 1
nobsprive = pd.merge(nobsprive, all, on=['Sector', 'time'], how='outer').sort_values(by="time")
nobsprive['Places'].fillna(0, inplace=True)
nobsprive['cumulative'] = nobsprive['Places'].cumsum()

nobs = pd.concat([nobsla, nobsvol, nobsprive])
nobs['Sector'] = nobs['Sector'].replace({"Private": "For-profit", "Local Authority": "Local Authority", "Voluntary": "Third Sector"})

nobs = nobs[nobs['time'] > -227] #Jan 2004

nobs["Local.authority"]= "All"




Providernobs = ProviderData[(ProviderData['Provision.type'] == "Children's home") & (~ProviderData['Local.authority'].isna())]
Providernobs = Providernobs[['time', 'Sector', 'URN', 'Local.authority', 'Places']].drop_duplicates()

nobsByIdih = Providernobs.groupby(['time', 'Local.authority', 'Sector'])['Places'].sum().reset_index()


nobsprive = nobsByIdih[nobsByIdih['Sector'] == "Private"]
nobsvol = nobsByIdih[nobsByIdih['Sector'] == "Voluntary"]
nobsla = nobsByIdih[nobsByIdih['Sector'] == "Local Authority"]

unique_local_authorities = nobsla['Local.authority'].unique()
times = list(range(-595, 1))
all_data = pd.DataFrame({
    'Sector': 'Private',
    'Local.authority': [local_authority for local_authority in unique_local_authorities for _ in times],
    'time': [time for _ in unique_local_authorities for time in times],
    'er': 1
})


nobsprive = pd.merge(all_data, nobsprive, on=['Sector', 'time', 'Local.authority'], how='left')
nobsprive = nobsprive.sort_values('time').fillna(0)  # Fill NaNs with 0
nobsprive['cumulative'] = nobsprive.groupby('Local.authority')['Places'].cumsum()


all_data['Sector'] = 'Local Authority'
nobsla = pd.merge(all_data, nobsla, on=['Sector', 'time', 'Local.authority'], how='left')
nobsla = nobsla.sort_values('time').fillna(0)  # Fill NaNs with 0
nobsla['cumulative'] = nobsla.groupby('Local.authority')['Places'].cumsum()

all_data['Sector'] = 'Voluntary'
nobsvol = pd.merge(all_data, nobsvol, on=['Sector', 'time', 'Local.authority'], how='left')
nobsvol = nobsvol.sort_values('time').fillna(0)  # Fill NaNs with 0
nobsvol['cumulative'] = nobsvol.groupby('Local.authority')['Places'].cumsum()

nobs2 = pd.concat([nobsla, nobsvol, nobsprive], ignore_index=True)
nobs2['Sector'] = pd.Categorical(nobs2['Sector'], categories=['Private', 'Local Authority', 'Voluntary'])
nobs2['Sector'] = nobs2['Sector'].cat.rename_categories(['For-profit', 'Local Authority', 'Third Sector'])

nobs2 = nobs2[nobs2['time'] > -227] #Jan 2004


nobs_fin2 = pd.concat([nobs2, nobs])

nobs_fin2['Homes or places']= "Places"


nobs_final = pd.concat([nobs_fin, nobs_fin2]).sort_values(by="Local.authority")









# Assuming you have a ggplot equivalent in Python
# and a variable 'cbPalette' defined as a list of colors
# and 'nobs' as your DataFrame
#d = ggplot(nobs[nobs['time'] > -211], aes(x='time', y='cumulative', group='Sector', fill='Sector', colour='Sector')) + \
#    geom_point() + \
#    theme_minimal() + \
#    scale_color_manual(values=cbPalette[0:3]) + \
#    labs(x='Year', y="Number of Children's homes", title='Number of active children\'s homes', fill='Ownership', color='Ownership') + \
#    scale_x_continuous(breaks=[-7, -31, -55, -79, -103, -127, -151, -175, -199],
#                       labels=["2021", "2019", "2017", "2015", "2013", "2011", "2009", "2007", "2005"])



import plotly.express as px
import plotly.graph_objects as go
import numpy as np







active_chomes = pd.read_csv("https://raw.githubusercontent.com/BenGoodair/childrens_social_care_data/main/Final_Data/outputs/active_chomes_2023.csv", encoding='ISO-8859-1')





outcomes_df = la_df[
    (la_df['subcategory'] == 'health and criminalisation') |
    (la_df['subcategory'] == 'ks2') |
    (la_df['subcategory'] == 'ks4') |
    (la_df['subcategory'] == 'key stage 2') |
    (la_df['subcategory'] == 'key stage 4') |
    (la_df['subcategory'] == 'school absence') |
    (la_df['subcategory'] == 'school exclusion') |
    (la_df['subcategory'] == 'missing incidents') |
    (la_df['subcategory'] == 'Reason episode ceased') |
    (la_df['category'] == 'care leavers')
]


#outcomes_df['variable'].value_counts()
#outcomes_df[outcomes_df['category'] == 'care leavers']['year'].value_counts().sort_index()
#outcomes_df[(outcomes_df['category'] == 'care leavers') & (outcomes_df['year'] == 2014)]
#la_df[(la_df['category'] == 'Expenditure') & (la_df['year'] == 2014)]



outcomes_df = outcomes_df[
    (outcomes_df['variable'] == 'sess_unauthorised') | #unauthorised absence
    (outcomes_df['variable'] == 'one_plus_sus') | # suspension
    (outcomes_df['variable'] == 'pupils_pa_10_exact') | # persitent absence
    (outcomes_df['variable'] == 'rwm_met_expected_standard') | 
    (outcomes_df['variable'] == 'gps_met_expected_standard') | 
    (outcomes_df['variable'] == 'writta_met_expected_standard') | 
    (outcomes_df['variable'] == 'read_met_expected_standard') | 
    (outcomes_df['variable'] == 'mat_met_expected_standard') | 
    (outcomes_df['variable'] == 'p8score') | 
    (outcomes_df['variable'] == 'att8') | 
    (outcomes_df['variable'] == 'Accommodation considered suitable') | 
    (outcomes_df['variable'] == 'Local authority not in touch with care leaver') | 
    (outcomes_df['variable'] == 'Total not in education employment or training') | 
    (outcomes_df['variable'] == 'Not in education training or employment, owing to other reasons') | 
    (outcomes_df['variable'] == 'Total information not known') | 
    (outcomes_df['variable'] == 'Independent living') | 
    (outcomes_df['variable'] == 'In custody') | 
    (outcomes_df['variable'] == 'Percentage of children who had a missing incident during the year') | 
    (outcomes_df['variable'] == 'Percentage of children who were away from placement without authorisation during the year') | 
    (outcomes_df['subcategory'] == 'Reason episode ceased') |
    (outcomes_df['subcategory'] == 'health and criminalisation') 

]


outcomes_df = outcomes_df[
    (outcomes_df['variable'] != 'Total') &
    (outcomes_df['variable'] != 'Total ages 0 to 4 years') &
    (outcomes_df['variable'] != 'Total all ages') &
    (outcomes_df['variable'] != 'Total ages 5 to 16 years')
]



outcomes_df['LA_Name'].value_counts()



outcomes_df.loc[outcomes_df['subcategory'] == 'ks2', 'subcategory'] = "Key stage 2"
outcomes_df.loc[outcomes_df['subcategory'] == 'key stage 2', 'subcategory'] = "Key stage 2"
outcomes_df.loc[outcomes_df['subcategory'] == 'ks4', 'subcategory'] = "Key stage 4"
outcomes_df.loc[outcomes_df['subcategory'] == 'key stage 4', 'subcategory'] = "Key stage 4"
outcomes_df.loc[outcomes_df['subcategory'] == 'health and criminalisation', 'subcategory'] = "Health and criminalisation"
outcomes_df.loc[outcomes_df['subcategory'] == 'school absence', 'subcategory'] = "School absence"
outcomes_df.loc[outcomes_df['subcategory'] == 'school exclusion', 'subcategory'] = "School absence"
outcomes_df.loc[outcomes_df['subcategory'] == '19 to 21 years', 'subcategory'] = "Care leavers (19 to 21)"
outcomes_df.loc[outcomes_df['subcategory'] == 'Aged 19 to 21', 'subcategory'] = "Care leavers (19 to 21)"
outcomes_df.loc[outcomes_df['subcategory'] == 'Aged 17 to 18', 'subcategory'] = "Care leavers (17 to 18)"
outcomes_df.loc[outcomes_df['subcategory'] == '17 to 18 years', 'subcategory'] = "Care leavers (17 to 18)"


outcomes_df['subcategory'].value_counts()


outcomes_df.loc[outcomes_df['variable'] == 'pupils_pa_10_exact', 'variable'] = "Persistent absence"
outcomes_df.loc[outcomes_df['variable'] == 'sess_unauthorised', 'variable'] = "Unauthorised absent sessions"
outcomes_df.loc[outcomes_df['variable'] == 'mat_met_expected_standard', 'variable'] = "Met expected grades (Maths)"
outcomes_df.loc[outcomes_df['variable'] == 'gps_met_expected_standard', 'variable'] = "Met expected grades (Grammar, punctuation and spelling)"
outcomes_df.loc[outcomes_df['variable'] == 'read_met_expected_standard', 'variable'] = "Met expected grades (Reading)"
outcomes_df.loc[outcomes_df['variable'] == 'writta_met_expected_standard', 'variable'] = "Met expected grades (Writting)"
outcomes_df.loc[outcomes_df['variable'] == 'rwm_met_expected_standard', 'variable'] = "Met expected grades (Reading, writing & maths)"
outcomes_df.loc[outcomes_df['variable'] == 'p8score', 'variable'] = "Average progress 8 score"
outcomes_df.loc[outcomes_df['variable'] == 'att8', 'variable'] = "Average attainment 8 score"
outcomes_df.loc[outcomes_df['variable'] == 'Percentage of children who were away from placement without authorisation during the year', 'variable'] = "Away from placement during year"
outcomes_df.loc[outcomes_df['variable'] == 'Percentage of children who had a missing incident during the year', 'variable'] = "Missing from placement during year"
outcomes_df.loc[outcomes_df['variable'] == 'one_plus_sus', 'variable'] = "At least one suspension"
outcomes_df.loc[outcomes_df['variable'] == 'Total information not known', 'variable'] = "Employment or education status not known"
outcomes_df.loc[outcomes_df['variable'] == 'Not in education training or employment, owing to other reasons', 'variable'] = "Not in education training or employment, for other reasons than illness, pregnancy or parenthood"

outcomes_df.loc[outcomes_df['variable'] == "Away from placement during year", 'percent'] = outcomes_df['number']
outcomes_df.loc[outcomes_df['variable'] == "Missing from placement during year", 'percent'] = outcomes_df['number']


outcomes_df = outcomes_df.dropna(subset=['percent'])

outcomes_df['LA_Name'].value_counts()



#keep only LAs with a 100 obs

outcomes_df = outcomes_df[outcomes_df['LA_Name'].map(outcomes_df['LA_Name'].value_counts()) > 100]

outcomes_df['percent'] = pd.to_numeric(outcomes_df['percent'], errors='coerce')


#####placements quality#####


placements_df = la_df[
    (la_df['subcategory'] == 'Distance between home and placement and locality of placement') |
    (la_df['subcategory'] == 'Reason for placement change during the year') |
    #(la_df['subcategory'] == 'Placement') |
    (la_df['subcategory'] == 'Locality of placement') |
    (la_df['subcategory'] == 'LA of placement') |
    (la_df['subcategory'] == 'Distance between home and placement') |
    (la_df['subcategory'] == 'Mid-year moves') |
    (la_df['subcategory'] == 'placement stability') #|
    #(la_df['subcategory'] == 'Placed inside the local authority boundary') 
]


placements_df['variable'].value_counts()

placements_df = placements_df[
    (placements_df['variable'] != 'Total') &
    (placements_df['variable'] != 'Total placements changing') &
    (placements_df['variable'] != 'Total children')
]


placements_df = placements_df.dropna(subset=['percent'])

placements_df['LA_Name'].value_counts()

placements_df = placements_df[placements_df['LA_Name'].map(placements_df['LA_Name'].value_counts()) > 104]

placements_df['percent'] = pd.to_numeric(placements_df['percent'], errors='coerce')



variable_options = []  # No options if no subcategory is selected
variable_options2 = []  # No options if no subcategory is selected















































####Dashboard####
#app = Dash(__name__)
import json
import dash 
from dash import dash_table
from dash import State
import reverse_geocoder as rg
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate



app = dash.Dash(external_stylesheets=[dbc.themes.LUX])


#server = app.server

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Outsourcing Impacts Tracker", className="display-7"),
        html.Hr(),
        html.P(
            "Welcome to a dashboard detailing the impacts of outsourcing in England's children social care sector.", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Outsourcing levels", href="/page-1", active="exact"),
                dbc.NavLink("Quality Impacts", href="/page-2", active="exact"),
                dbc.NavLink("Local Authority Profiles", href="/page-3", active="exact"),
                dbc.NavLink("Links To Resources", href="/page-4", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)


app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div([
            html.H2("Welcome to the Outsourcing Impacts Tracker Dashboard", className="display-7"),
            html.Hr(),
            html.H4("Purpose of the Dashboard"),
            html.P("The Outsourcing Impacts Dashboard aims to provide policymakers with valuable insights into outsourcing levels and their impact on quality of social care services in England. By visualizing outsoucing levels, service quality data, and related information, this dashboard assists policymakers in making informed decisions to address the challenges posed by increasing need for social care."),
            html.H4("Key Features"),
            html.Ul([
                html.Li("For profit outsourcing trends: Graph showing increased number of children placed in for-profit providers."),
                html.Li("Outsourcing Geographies: Map representations and visualizations of localised outsourcing levels."),
                html.Li("For-profit children's homes: See a sliding visualisation of the rise of for-profit children's homes."),
                html.Li("Children in care outcomes: Select your variable and see the trend of outcomes in your area."),
            ]),
            html.H4("How to Use"),
            html.P("Navigate through the tabs at the sidebar to access different sections of the dashboard. Each section provides specific information and visualizations related to outsourcing levels and its impacts. Use the interactive components to explore the data and gain insights."),
            html.P("We encourage policymakers to utilize this dashboard as a resource for evidence-based decision-making. By considering the data, visualizations, and resources provided here, policymakers can better understand the magnitude of outsouring and the potential risks associated with it. Additionally, we recommend referring to the 'Links to Resources' section for further in-depth research and reports."),
            html.Hr(),
            html.H4("Important Note"),
            html.P("This dashboard is for informational purposes only and should not be used as the sole basis for policymaking. It is crucial to consult domain experts, conduct further analysis, and consider additional factors when making policy decisions."),
            html.Hr(),
            html.H5("For more information, please visit the following pages:"),
            dbc.Nav(
                [
                    dbc.NavLink("Outsourcing levels", href="/page-1", active="exact"),
                    dbc.NavLink("Quality Impacts", href="/page-2", active="exact"),
                    dbc.NavLink("Local authority profiles", href="/page-3", active="exact"),
                    dbc.NavLink("Further Resources", href="/page-4", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
            html.Hr(),
            html.P("Acknowledgements: we are grateful to the support from Nuffield Foundation who motivated this dashboard."),
            html.P("A proof-of-concept version of this dashboard was first developed by Carolin Kroeger, Dunja Matic and Ben Goodair - we are grateful to the input of all team members."),
        ], style={"padding": "2rem"})
    elif pathname == "/page-1":
        return html.Div([
            dcc.Tabs(id="page-1-tabs", value='tab-1', children=[
                dcc.Tab(label='Outsourced Placements', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Outsourced Spending', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Residential Care Providers', value='tab-3', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Outsourcing Geographies', value='tab-4', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles),
            html.Div(id='page-1-tabs-content')
        ])
    elif pathname == "/page-2":
        return html.Div([
            dcc.Tabs(id="page-2-tabs", value='tab-5', children=[
                dcc.Tab(label='Ofsted ratings', value='tab-5', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Children outcomes', value='tab-6', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Placement quality', value='tab-7', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles),
            html.Div(id='page-2-tabs-content')
        ])
    elif pathname == "/page-3":
        return html.Div([
            dcc.Tabs(id="page-3-tabs", value='tab-8', children=[
                dcc.Tab(label='Local authority profiles', value='tab-8', style=tab_style, selected_style=tab_selected_style),
                ], style=tabs_styles),
            html.Div(id='page-3-tabs-content')
        ])
    elif pathname == "/page-4":
        return html.Div([
            dcc.Tabs(id="page-4-tabs", value='tab-9', children=[
                dcc.Tab(label='Data download', value='tab-9', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Educational resources', value='tab-10', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Contact and feedback', value='tab-11', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles),
            html.Div(id='page-4-tabs-content')
        ])
   # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ],
        className="p-3 bg-light rounded-3",
    )


@app.callback(Output('page-1-tabs-content', 'children'), [Input('page-1-tabs', 'value')])
def render_page_1_content(tab):
    if tab == 'tab-1':
        return html.Div([
               html.H1("For-profit outsourcing of social care placements:"),
               html.H3("Select a Local Authority"),
               dcc.Dropdown(
                 id='LA-dropdown',
                 options=[
                     {'label': hop, 'value': hop} for hop in la_df[la_df['variable']=="Private provision"]['LA_Name'].unique()
                     ],
                placeholder='All Local Authorities',

                 value=None
                 ),
               dcc.Graph(id='scatter-plot'),
            ])
    elif tab == 'tab-2':
        return html.Div([
            html.H1('For-profit outsourcing of social care spending:'),
            html.Hr(),
            html.H3("Select a Local Authority"),
            dcc.Dropdown(
                id='LA-dropdown3',
                options=[
                     {'label': hop, 'value': hop} for hop in la_df[(la_df['category']=="Expenditure") & (la_df['subcategory']=="For_profit")]['LA_Name'].unique()
                     ],
                value=None,
                placeholder='All Local Authorities',
                style={'width': '600px', 'margin-bottom': '20px'}
            ),
            html.H3("Select an area of expenditure"),
            dcc.Dropdown(
                id='spend-dropdown',
                options=[
                     {'label': hop, 'value': hop} for hop in la_df[(la_df['category']=="Expenditure") & (la_df['subcategory']=="For_profit")]['variable'].unique()
                     ],
                value='Total Children Looked After',
                placeholder='Select an area of expenditure',
                style={'width': '600px', 'margin-bottom': '20px'}
            ),
            dcc.Graph(
                id='scatter-plot2'
            )
                           ])
    elif tab == 'tab-3':
        return html.Div([
            html.H1("Number of active children's homes and available places"),
            html.H3("Select a Local Authority"),
            dcc.Dropdown(
              id='local-authority-dropdown',
              options=[
                 {'label': la, 'value': la} for la in nobs_final['Local.authority'].unique()
              ],
              value=nobs_final['Local.authority'].unique()[0]
            ),
            html.H3("Select Number of Homes or Places"),
            dcc.Dropdown(
                 id='homes-or-places-dropdown',
                 options=[
                     {'label': hop, 'value': hop} for hop in nobs_final['Homes or places'].unique()
                 ],
                value=nobs_final['Homes or places'].unique()[0]
            ),
            dcc.Graph(id='child-homes-plot'),
            html.H6("*Estimates based on the registration date of children's homes inspected since 2018")
            ])
    elif tab == 'tab-4':
        return html.Div([
            html.H1("Outsourcing Geographies"),
            html.H3("Select a measure of outsourcing"),
            dcc.Dropdown(
              id='variable-dropdown',
              options=[
                 {'label': la, 'value': la} for la in merged2['variable'].unique()
              ],
              value=merged2['variable'].unique()[2]
            ),
            dcc.Graph(id='outsourcing-map',style={'height': '1000px'})])

@app.callback(Output('page-2-tabs-content', 'children'), [Input('page-2-tabs', 'value')])
def render_page_2_content(tab):
    if tab == 'tab-5':
        return  html.Div([
            html.H1('Ofsted ratings of active children homes:'),
            html.Hr(),
            html.H6('Select an inspection domain:'),
            html.Hr(),
            dcc.Dropdown(
                id='domain-dropdown',
                options=[{'label': geog_n, 'value': geog_n} for geog_n in active_chomes['Domain'].unique()],
                value='Overall.experiences.and.progress.of.children.and.young.people',
                placeholder='Select an inspection domain'
            ),
            html.Hr(),
            dcc.Graph(id='ofsted-plot',style={'height': '800px'})
        ])
    elif tab == 'tab-6':
        return html.Div([
            html.H1('Outcomes for children in care and care leavers'),
            html.H3('Select a Local Authority'),
            dcc.Dropdown(
                id='la-dropdown4',
                options=[{'label': geog_n, 'value': geog_n} for geog_n in outcomes_df['LA_Name'].unique()],
                value=None,
                placeholder='All'
            ),
            html.H3("Select a subcategory"),
            dcc.Dropdown(
                id='subcategory-dropdown4',
                options=[{'label': geog_n, 'value': geog_n} for geog_n in outcomes_df['subcategory'].unique()],
                value='Health and criminalisation',
                placeholder='Select a subcategory'
            ),

            html.H3("Select a variable"),
            dcc.Dropdown(
                id='variable-dropdown4',
                options=variable_options,  # Add this line to populate initial options
                placeholder='Select a variable',
            ),

            dcc.Graph(id='outcome_plot')

        ])
    elif tab == 'tab-7':
        return html.Div([
            html.H1('Quality of placements'),
            html.H3('Select a Local Authority'),
            dcc.Dropdown(
                id='la-dropdown5',
                options=[{'label': geog_n, 'value': geog_n} for geog_n in placements_df['LA_Name'].unique()],
                value=None,
                placeholder='All'
            ),
            html.H3("Select a subcategory"),
            dcc.Dropdown(
                id='subcategory-dropdown5',
                options=[{'label': geog_n, 'value': geog_n} for geog_n in placements_df['subcategory'].unique()],
                value='Locality of placement',
                placeholder='Select a subcategory'
            ),

            html.H3("Select a variable"),
            dcc.Dropdown(
                id='variable-dropdown5',
                options=variable_options2,  # Add this line to populate initial options
                placeholder='Select a variable',
            ),

            dcc.Graph(id='placement_plot')

        ])

@app.callback(Output('page-3-tabs-content', 'children'), [Input('page-3-tabs', 'value')])
def render_page_3_content(tab):
    if tab == 'tab-8':
        return html.Div([
            dcc.Dropdown(
                id='la-dropdown6',
                options=[{'label': la, 'value': la} for la in outcomes_df['LA_Name'].unique()],
                multi=True,
                placeholder='Select Local Authorities to compare'
           ),
            dcc.Dropdown(
                id='subcategory-dropdown6',
                options=[{'label': subcat, 'value': subcat} for subcat in outcomes_df['subcategory'].unique()],
                placeholder='Select Subcategory'
            ),
           dcc.Dropdown(
               id='variable-dropdown6',
               placeholder='Select Variable'
           ),
           dcc.Graph(id='compare_plot')
])
    else:
        raise PreventUpdate




@app.callback(Output('page-4-tabs-content', 'children'), [Input('page-4-tabs', 'value')])
def render_page_4_content(tab):
    if tab == 'tab-9':
        return  html.Div([
            html.H3('Data Downloads:'),
            html.P('You can access to three different files: Data at the lat/lon scale, county scale or state scale:'),
            html.Ul([
                html.Li(html.A("Download Data with for LAs", href="https://raw.githubusercontent.com/BenGoodair/Outsourcing_Impact_Dashboard/main/Data/dashboard_LA_data_long.csv"))])  
         ])
    elif tab == 'tab-10':
        return html.Div([
            html.H3("Links to Resources"),

            html.H6("Research on outsourcing of children's social care"),
            html.Ul([
                html.Li(html.A("Do for-profit childrens homes outperform council-run homes?", href="https://www.sciencedirect.com/science/article/pii/S0277953622006293")),
                html.Li(html.A("Does outsourcing correspond with better or worse quality placements for children?", href="https://www.sciencedirect.com/science/article/pii/S0277953622006293"))
            ]),

            html.H6("Research on outsourcing of adult's social care"),
            html.H6("Research on outsourcing of healthcare"),
            html.H6("Research from outside the UK")
        ])
    elif tab == 'tab-11':
        return html.Div([
            html.H3("Meet the team:"),
            html.Ul([
                html.Li([
                    html.Img(src="https://github.com/BenGoodair/Outsourcing_Impact_Dashboard/blob/main/anders_bach-mortensen.jpg?raw=true", style={"width": "100px", "height": "100px"}),
                    html.Div([
                        html.H4("Anders"),
                        html.P("Anders is a social scientist with expertise on outsourcing, social care services and systematic review methods."),
                        html.P("Anders was national champion fencer in his youth - he now uses skills of precision in interpretting complex statistical models.")
                    ], style={"display": "inline-block", "vertical-align": "top"})
                ]),
                html.Li([
                    html.Img(src="https://github.com/BenGoodair/Methane_Dashboard/blob/main/ben.jpg?raw=true", style={"width": "100px", "height": "100px"}),
                    html.Div([
                        html.H4("Ben"),
                        html.P("Ben is a social researcher identifying the impacts of privatization on health and social care systems."),
                        html.P("Ben will embroider any form of data visualisation he thinks worthy of the thread.")
                    ], style={"display": "inline-block", "vertical-align": "top"})
                ])
            ]),
            html.H3("Partner with us:"),
            html.H6("Join our team to continue this work"),
            html.P("We are looking for partners with policy, industrial or lived experiences to join our happy community!"),
            html.Ul([
                html.Li('We can write a funding application to ensure labor compensated and valued.'),
                html.Li('We want new directions and ideas, bring your creativity!'),
                html.Li('We want to have fun and work in a respectful, supportive, and positive way.')
            ]),
            html.H3("Contact and feedback"),
            html.H6("Help us improve this dashboard for your needs!"),
            html.P("All our work is completely open access and reproducible, we'd love to work with you to apply this work to other data"),
            html.Ul([
                html.Li('Email us at: benjamin.goodair@spi.ox.ac.uk'),
                html.Li('Tweet us at: @BenGoodair'),
                html.Li('Find us at: DSPI, Oxford, United Kingdom')
            ])
        ])




@app.callback(Output('scatter-plot', 'figure'),Input('LA-dropdown', 'value'))
def update_scatter_plot(selected_county):
 #    filtered_df = la_df[la_df['variable']=="Private provision"][la_df['LA_Name'] == selected_county]

    if selected_county is None:
        filtered_df = la_df[la_df['variable']=="Private provision"][['LA_Name','year' ,'percent']]
    else:
        filtered_df = la_df[la_df['variable']=="Private provision"][la_df['LA_Name'] == selected_county]

    fig1 = px.scatter(filtered_df, x='year', y='percent', color='percent', trendline='lowess',
                     color_continuous_scale='ylorrd')
    fig1.update_traces(marker=dict(size=5))
    fig1.update_layout(xaxis_title='Year',        yaxis_title='For-profit placements (%)',        title='Percent of children placed with for-profit providers 2011-22',        coloraxis_colorbar=dict(title='For-profit %')    )
    
    return fig1






@app.callback(Output('scatter-plot2', 'figure'), Input('LA-dropdown3', 'value'), Input('spend-dropdown', 'value'))

def update_scatter_plot(selected_county, selected_expenditure):
    if selected_county is None or selected_county == "":
        filtered_df_spend = la_df[(la_df['category'] == "Expenditure") & 
                                  (la_df['subcategory'] == "For_profit") & 
                                  (la_df['variable'] == selected_expenditure)]
    else:
        filtered_df_spend = la_df[(la_df['category'] == "Expenditure") & 
                                  (la_df['subcategory'] == "For_profit") & 
                                  (la_df['LA_Name'] == selected_county) & 
                                  (la_df['variable'] == selected_expenditure)]
    
    fig2 = px.scatter(filtered_df_spend, x='year', y='percent', color='percent', trendline='lowess',
                     color_continuous_scale='ylorrd')
    fig2.update_traces(marker=dict(size=5))
    fig2.update_layout(
        xaxis_title='Year',
        yaxis_title='For-profit expenditure (%)',
        title='Percent of expenditure on for-profit providers 2011-22',
        coloraxis_colorbar=dict(title='For-profit %')
    )
    
    return fig2


# Create a separate DataFrame for x-axis categories
sectors = nobs_final['Sector'].unique()


@app.callback(Output('child-homes-plot', 'figure'),Input('local-authority-dropdown', 'value'),Input('homes-or-places-dropdown', 'value'))
def update_plot(selected_local_authority, selected_homes_or_places):
    filtered_nobs = nobs_final[(nobs_final['Local.authority'] == selected_local_authority) & (nobs_final['Homes or places'] == selected_homes_or_places)]

    custom_colors = {"For-profit": "#1f77b4", "Local Authority": "#ff7f0e", "Third Sector": "#2ca02c"}


    fig = px.scatter(filtered_nobs, x='time', y='cumulative', color='Sector',
                     color_discrete_map=custom_colors)
    
    # Add a line trace
    line_data = filtered_nobs[filtered_nobs['time'] > -211].groupby(['time', 'Sector'])['cumulative'].sum().reset_index()
    for sector in line_data['Sector'].unique():
        sector_data = line_data[line_data['Sector'] == sector]
        fig.add_trace(go.Scatter(x=sector_data['time'], y=sector_data['cumulative'],
                                 mode='lines+markers', name=sector,
                                 line=dict(color=custom_colors[sector]),
                                 showlegend=False))  # Hide the legend for the line traces
        

    # Define custom tick values and labels for the x-axis
    custom_tick_values = [-11, -35, -59, -83, -107, -131, -155, -179, -203, -227]
    custom_tick_labels = ["2022", "2020", "2018", "2016", "2014", "2012", "2010", "2008", "2006", "2004"]

# Update the x-axis with the custom tick values and labels
    fig.update_xaxes(
    tickvals=custom_tick_values,
    ticktext=custom_tick_labels
)

    fig.update_layout(
        title=f"Number of active children's homes ({selected_local_authority}, {selected_homes_or_places})",
        xaxis_title='Year',
        yaxis_title=f"Number of Children's residential{selected_homes_or_places}",
    )
    return fig




@app.callback(Output('outsourcing-map', 'figure'),Input('variable-dropdown', 'value'))
def update_plot(selected_variable):

     

    filtered_merged = merged2[merged2['variable']==selected_variable]

    min_value = filtered_merged['variable'].min()
    max_value = filtered_merged['variable'].max()

    

    map = px.choropleth_mapbox(filtered_merged, geojson=filtered_merged.geometry, locations=filtered_merged.index, color='percent',
                            color_continuous_scale='ylorrd', center={"lat": 52.9781, "lon": -1.82360},
                            mapbox_style='open-street-map',
                            hover_name = 'LA_Name', zoom=6)

    
    return map






@app.callback(Output('ofsted-plot', 'figure'), Input('domain-dropdown', 'value'))
def update_scatter_plot(selected_domain):

    filtered_active_chomes =  active_chomes[active_chomes['Domain']==selected_domain]

    # Create a unique circle identifier for each 'Overall.experiences'
    filtered_active_chomes['Circle'] = filtered_active_chomes.groupby('Rating').ngroup()

    # Define the custom order for 'Overall.experiences'
    custom_order = [  'Inadequate','Requires improvement to be good', 'Good', 'Outstanding']

    # Create a Categorical data type with the desired order
    filtered_active_chomes['Overall_Experiences_Mapping'] = pd.Categorical(filtered_active_chomes['Rating'], categories=custom_order, ordered=True)

    # Define a function to add points within a circle
    def add_points_in_circle(group):
        radius = 0.9  # Adjust this value to control the radius of the circles

        # Calculate the number of points based on the total number of rows in the group
        num_points = len(group)

        # Generate random angles and radii within the circle for each group
        theta = np.linspace(0, 2 * np.pi, num_points)
        r = np.sqrt(np.random.uniform(0, 1, num_points)) * radius

        group['Jittered_x'] = group['Circle'] + r * np.cos(theta)
        group['Jittered_y'] = group['Overall_Experiences_Mapping'].cat.codes + r * np.sin(theta)
        return group

    # Apply the point addition function to each group
    filtered_active_chomes = filtered_active_chomes.groupby('Circle').apply(add_points_in_circle).reset_index(drop=True)

    # Create a bubble chart with perfectly filled huge bubbles filled with jittered points in both dimensions
    ofsted_fig = px.scatter(filtered_active_chomes, x='Jittered_x', y='Jittered_y',
                 color='Sector',
                 hover_name = 'Organisation.which.owns.the.provider',
                 custom_data=['Rating', 'Places', 'Registration.date', 'Local.authority', 'Sector'],
                 labels={'Sector': 'Sector'},
                 title="Active Children's Homes - as of March 2023")


    hover_template = """
    Owner: %{hovertext}<br>
    Sector: %{customdata[4]}<br>
    Rating: %{customdata[0]}<br>
    Places: %{customdata[1]}<br>
    Registration Date: %{customdata[2]}<br>
    Local Authority: %{customdata[3]}<br>
    """

    ofsted_fig.update_traces(hovertemplate=hover_template)


    # Update the size and opacity of the bubbles
    marker_size = 6
    ofsted_fig.update_traces(marker=dict(size=marker_size, opacity=0.7))

    # Remove the axes, background, and labels
    ofsted_fig.update_xaxes(showline=False, showgrid=False, showticklabels=False, title_text='')
    ofsted_fig.update_yaxes(showline=False, showgrid=False, showticklabels=False, title_text='')
    ofsted_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)'  # Set the background color to transparent
    )

    for group, group_data in filtered_active_chomes.groupby('Circle'):
        # Calculate the position for the label above the group
        x_label = group_data['Jittered_x'].mean()
        y_label = group_data['Jittered_y'].max() + 0.12  # Adjust the vertical position as needed

        # Get the mode (most common category) for the 'Overall_Experiences_Mapping' in the group
        rating = group_data['Overall_Experiences_Mapping'].mode().iloc[0]

        # Add a text annotation to the figure
        ofsted_fig.add_annotation(
            x=x_label,
            y=y_label,
            text=rating,
            showarrow=False,
            font=dict(size=16),
            opacity=0.9
        )


    return ofsted_fig



variable_options = []  # No options if no subcategory is selected

@app.callback(Output('variable-dropdown4', 'options'), Input('subcategory-dropdown4', 'value'))
def update_variable_options(selected_subcategory):
    if selected_subcategory:
        # Filter the DataFrame based on the selected subcategory
        filtered_df = outcomes_df[outcomes_df['subcategory'] == selected_subcategory]

        # Get the unique variable options from the filtered DataFrame
        variable_options = [{'label': variable, 'value': variable} for variable in filtered_df['variable'].unique()]
    else:
        variable_options = []  # No options if no subcategory is selected

    return variable_options








@app.callback(Output('outcome_plot', 'figure'), Input('la-dropdown4', 'value'), Input('subcategory-dropdown4', 'value'), Input('variable-dropdown4', 'value'))
def update_outcome_plot(selected_county, selected_subcategory, selected_variable):
    print("Selected County:", selected_county)
    print("Selected Subcategory:", selected_subcategory)
    print("Selected Variable:", selected_variable)

    # Filter the data based on the selected values
    if selected_county is None or selected_county == "":
        filtered_df_outcome = outcomes_df[(outcomes_df['subcategory'] == selected_subcategory) & 
                                          (outcomes_df['variable'] == selected_variable)].copy()
    else:
        filtered_df_outcome = outcomes_df[(outcomes_df['subcategory'] == selected_subcategory) & 
                                          (outcomes_df['LA_Name'] == selected_county) & 
                                          (outcomes_df['variable'] == selected_variable)].copy()

    print("Filtered Data:")
    print(filtered_df_outcome)

    outcome_plot = px.scatter(filtered_df_outcome, x='year', y='percent', color='percent', trendline='lowess',color_continuous_scale='ylorrd')
    outcome_plot.update_traces(marker=dict(size=5))
    outcome_plot.update_layout(
        xaxis_title='Year',
        yaxis_title='(%)',
        title='Outcomes for children in care',
        coloraxis_colorbar=dict(title=selected_variable)
    )

    return outcome_plot




variable_options2 = []  # No options if no subcategory is selected

@app.callback(Output('variable-dropdown5', 'options'), Input('subcategory-dropdown5', 'value'))
def update_variable_options(selected_subcategory):
    if selected_subcategory:
        # Filter the DataFrame based on the selected subcategory
        filtered_df = placements_df[placements_df['subcategory'] == selected_subcategory]

        # Get the unique variable options from the filtered DataFrame
        variable_options2 = [{'label': variable, 'value': variable} for variable in filtered_df['variable'].unique()]
    else:
        variable_options2 = []  # No options if no subcategory is selected

    return variable_options2






@app.callback(Output('placement_plot', 'figure'), Input('la-dropdown5', 'value'), Input('subcategory-dropdown5', 'value'), Input('variable-dropdown5', 'value'))
def update_outcome_plot(selected_county, selected_subcategory, selected_variable):
    print("Selected County:", selected_county)
    print("Selected Subcategory:", selected_subcategory)
    print("Selected Variable:", selected_variable)

    # Filter the data based on the selected values
    if selected_county is None or selected_county == "":
        filtered_df_placement = placements_df[(placements_df['subcategory'] == selected_subcategory) & 
                                          (placements_df['variable'] == selected_variable)].copy()
    else:
        filtered_df_placement = placements_df[(placements_df['subcategory'] == selected_subcategory) & 
                                          (placements_df['LA_Name'] == selected_county) & 
                                          (placements_df['variable'] == selected_variable)].copy()

    #print("Filtered Data:")
    #print(filtered_df_placement)

    placement_plot = px.scatter(filtered_df_placement, x='year', y='percent', color='percent', trendline='lowess',color_continuous_scale='ylorrd')
    placement_plot.update_traces(marker=dict(size=5))
    placement_plot.update_layout(
        xaxis_title='Year',
        yaxis_title='(%)',
        title='Placements for children in care',
        coloraxis_colorbar=dict(title=selected_variable)
    )

    return placement_plot



variable_options3 = []  # No options if no subcategory is selected

@app.callback(Output('variable-dropdown6', 'options'), Input('subcategory-dropdown6', 'value'))
def update_variable_options(selected_subcategory):
    if selected_subcategory:
        # Filter the DataFrame based on the selected subcategory
        filtered_df = outcomes_df[outcomes_df['subcategory'] == selected_subcategory]

        # Get the unique variable options from the filtered DataFrame
        variable_options3 = [{'label': variable, 'value': variable} for variable in filtered_df['variable'].unique()]
    else:
        variable_options3 = []  # No options if no subcategory is selected

    return variable_options3



# Add a new callback to update the comparison plot
@app.callback(Output('compare_plot', 'figure'), Input('la-dropdown6', 'value'), Input('variable-dropdown6', 'value'))
def update_comparison_plot(selected_local_authorities, selected_variable):
    if not selected_local_authorities:
        raise PreventUpdate

    filtered_df = outcomes_df[(outcomes_df['variable'] == selected_variable) &
                              (outcomes_df['LA_Name'].isin(selected_local_authorities))]

    fig = px.scatter(filtered_df, x='year', y='percent', color='LA_Name')
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title=selected_variable,
        title=f'Comparison of {selected_variable} between {", ".join(selected_local_authorities)}',
    )

    # Add a line trace to the plot
    for la in selected_local_authorities:
        line_data = filtered_df[filtered_df['LA_Name'] == la].sort_values(by='year')
        fig.add_trace(go.Scatter(x=line_data['year'], y=line_data['percent'], mode='lines', name=la))

    return fig




if __name__ == '__main__':
    app.run_server(host='localhost',port=8005)






# z1, z2, z3 = np.random.random((3, 7, 7))

# customdata = np.dstack((z2, z3))
# mycustomdata = np.dstack((hospitals["company_name"], hospitals["number_of_employees"]))
# mycustomdata = mycustomdata.T.tolist()



# mycustomdata = np.dstack((hospitals["company_name"], hospitals["phone_number"], hospitals["number_of_employees"], hospitals["previous_leaks_n"], hospitals["fossil_fuel_type"], hospitals["number_of_beds"])).T.tolist(),



















































































































#app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
#
#
##app = dash.Dash(__name__)
#
#app.layout = html.Div([
#    html.H1("Number of active children's homes"),
#    dcc.Graph(id='scatter-plot'),
#    dcc.Dropdown(
#        id='LA-dropdown',
#        options=[
#            {'label': hop, 'value': hop} for hop in la_df['LA_Name'].unique()
#        ],
#        value=None
#    )
#])
#
#@app.callback(
#        Output('scatter-plot', 'figure'),
#        Input('LA-dropdown', 'value'))
#def update_scatter_plot(selected_county):
##    filtered_df = la_df[la_df['variable']=="Private provision"][la_df['LA_Name'] == selected_county]
#
#    if selected_county is None:
#        filtered_df = la_df[la_df['variable']=="Private provision"][['LA_Name','year' ,'percent']]
#    else:
#        filtered_df = la_df[la_df['variable']=="Private provision"][la_df['LA_Name'] == selected_county]
#
#    fig1 = px.scatter(filtered_df, x='year', y='percent', color='percent', trendline='lowess',
#                     color_continuous_scale='ylorrd')
#    fig1.update_traces(marker=dict(size=5))
#    fig1.update_layout(xaxis_title='Year',        yaxis_title='For-profit placements (%)',        title='Percent of children placed with for-profit providers 2011-22',        coloraxis_colorbar=dict(title='For-profit %')    )
#    
#    return fig1
#
#if __name__ == '__main__':
#    app.run_server(host='localhost',port=8005)
#
#
#








#
#@app.callback(Output('outcome_plot', 'figure'), Input('LA-dropdown4', 'value'), Input('subcategory-dropdown4', 'value'), Input('variable-dropdown4', 'value'))
#def update_scatter_plot(selected_county, selected_subcategory, selected_variable):
#    if selected_county is None or selected_county == "":
#
#
#
#
#filtered_df_outcome = outcomes_df[(outcomes_df['subcategory'] == 'Health and criminalisation') & (outcomes_df['variable'] == 'SDQ score is a cause for concern')]
#    else:
#        filtered_df_outcome = outcomes_df[(outcomes_df['subcategory'] == selected_subcategory) & 
#                                  (outcomes_df['LA_Name'] == selected_county) & 
#                                  (outcomes_df['variable'] == selected_variable)]
#    
#outcome_plot = px.scatter(filtered_df_outcome, x='year', y='percent', color='percent', trendline='lowess',color_continuous_scale='ylorrd')
#    outcome_plot.update_traces(marker=dict(size=5))
#    outcome_plot.update_layout(
#        xaxis_title='Year',
#        yaxis_title='For-profit expenditure (%)',
#        title='Outcomes for children in care',
#        coloraxis_colorbar=dict(title=selected_variable)
#    )
#    
#    return outcome_plot
#













