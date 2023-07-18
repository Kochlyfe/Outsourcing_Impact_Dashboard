


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

import plotly.express as px
from plotly.colors import sequential


# Define a custom color scale with more variations, ending in red
custom_color_scale = [
    (i, color) for i, color in zip(
        range(0, 110, 10),
        sequential.Viridis
    )
] + [(100, 'red')]  # Red for the highest value





####HEALTHY CAKES####


la_df = pd.read_csv("https://raw.githubusercontent.com/BenGoodair/Outsourcing_Impact_Dashboard/main/Data/dashboard_LA_data.csv")
la_df_long = pd.read_csv("https://raw.githubusercontent.com/BenGoodair/Outsourcing_Impact_Dashboard/main/Data/dashboard_LA_data_long.csv")
# alter the mh ID to be "mental health"
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as colors

la_df.sort_values(by='geog_n', ascending=True, inplace=True)


import geopandas as gpd
df2021 = la_df[la_df['year'] == 2021]

df2021.loc[df2021['New_geog_code'] == 'E06000060', 'New_geog_code'] = 'E10000002'

# Rename columns
uaboundaries = gpd.read_file("https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_and_Unitary_Authorities_December_2019_GCB_UK_2022/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson")
uaboundaries = uaboundaries.rename(columns={"ctyua19cd": "New_geog_code", "ctyua19nm": "lad19nm", "ctyua19nmw": "lad19nmw"})

# Filter out unwanted data
uaboundaries = uaboundaries[~uaboundaries["lad19nm"].isin(["Wales", "Scotland"])]
uaboundaries = uaboundaries[uaboundaries["New_geog_code"].str.startswith('E')]

df2021 = df2021[['New_geog_code','geog_n','CLA_Mar', 'per_for_profit', 'Private_spend', 'Total_spend']]


merged = uaboundaries.set_index('New_geog_code').join(df2021.set_index('New_geog_code'))
#merged = merged.reset_index()
#merged.head()


#customdata = np.stack((df2021['geog_n'], df2021['CLA_Mar'], df2021['per_for_profit'], df2021['Private_spend'], df2021['Total_spend']), axis=-1)

merged = merged.dropna(subset=['geog_n'])

min_value = merged['per_for_profit'].min()
max_value = merged['per_for_profit'].max()

merged['Private_spend'] = merged['Private_spend'] / 1000000

merged = merged.round(decimals=2)


map = px.choropleth_mapbox(merged, geojson=merged.geometry, locations=merged.index, color='per_for_profit',
                            color_continuous_scale='ylorrd', center={"lat": 52.9781, "lon": -1.82360},
                            custom_data=['geog_n','CLA_Mar', 'per_for_profit', 'Private_spend', 'Total_spend'],
                            mapbox_style='open-street-map',
                            hover_name = 'geog_n', zoom=6)

map.update_traces(hovertemplate='Local Authority: %{customdata[0]}<br>Number of children in care: %{customdata[1]}<br>Percent of children in FP placement: %{customdata[2]}<br>Total expenditure (Ms): %{customdata[4]}<br>For-profit expenditure (Ms): %{customdata[3]}')

#map.show()
 


####outcomes####

#outcomes_df = la_df_long

#outcomes_df = outcomes_df.groupby(['year']).mean().reset_index()

##### provider bars #####

provider_df = pd.read_csv("https://raw.githubusercontent.com/BenGoodair/Outsourcing_Impact_Dashboard/main/Data/dashboard_provider_data.csv")

# Convert date column to datetime format
provider_df["date"] = pd.to_datetime(provider_df["Registration.date"], format="%d/%m/%Y")

# Extract month and year from the date
provider_df["month"] = provider_df["date"].dt.strftime("%m/%y")

# Calculate time in months from March 1, 2023
provider_df["time"] = (provider_df["date"] - pd.to_datetime("2021-12-30")).dt.days // 30

# Filter rows with Provision.type as "Children's home" and select relevant columns
provider_df = provider_df.loc[provider_df["Provision.type"] == "Children's home", ["time", "Sector", "URN"]].drop_duplicates()

# Map Sector values to desired categories
provider_df["Sector"] = provider_df["Sector"].map({
    "Private": "For-profit",
    "Local Authority": "Local Authority",
    "Health Authority": "Local Authority",
    "Voluntary": "Third Sector"
})

# Group by time and Sector, calculate the count (nobs), and set Sector as a categorical variable
provider_df = provider_df.groupby(["time", "Sector"]).size().reset_index(name="nobs")
provider_df["Sector"] = pd.Categorical(provider_df["Sector"], categories=["For-profit", "Local Authority", "Third Sector"])

# Generate a DataFrame with all unique Sector values and repeated time values
all_sectors = pd.DataFrame({"Sector": provider_df["Sector"].unique()})
all_sectors = all_sectors.loc[all_sectors.index.repeat(594)].reset_index(drop=True)
all_sectors["time"] = all_sectors.groupby("Sector").cumcount() - 593
all_sectors["er"] = 1

# Merge provider_df with all_sectors to fill missing combinations
provider_df = pd.merge(all_sectors, provider_df, on=["Sector", "time"], how="left")
provider_df["nobs"] = provider_df["nobs"].fillna(0)

# Calculate cumulative sum of nobs within each Sector group
#think this isn't working

provider_df.sort_values(by='time', ascending=True, inplace=True)


provider_df["cumulative"] = provider_df.groupby("Sector")["nobs"].cumsum()


#print(provider_df)

# Filter rows with time greater than -157 and set cumulative as NA for time greater than -11
provider_df = provider_df[provider_df['time'] >= -211]

colors = ["#D20E46", "#EABB0E", "#C7F00E"]

# # Create the bar graph
# bar = px.bar(provider_df[provider_df['time'] == -157], x='Sector', y='cumulative')

# # Customize the appearance with the color palette
# bar.update_traces(marker_color=colors)

# bar.update_layout(title='Cumulative Data by Sector',
#                   xaxis_title='Sector',
#                   yaxis_title='Cumulative',
#                   plot_bgcolor='rgba(0,0,0,0)',
#                   paper_bgcolor='rgba(0,0,0,0)',
#                   font=dict(color='black'),
#                   bargap=0.15)

# # Show the graph
# bar.show()

import plotly.express as px
import plotly.graph_objects as go















































####Dashboard####
#app = Dash(__name__)
import json
import dash 
from dash import dash_table
from dash import State
import reverse_geocoder as rg
from dash.dependencies import Input, Output, State, MATCH



app = dash.Dash(external_stylesheets=[dbc.themes.LUX,  'https://cdnjs.cloudflare.com/ajax/libs/rc-slider/9.7.2/rc-slider.min.css'])


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
                dbc.NavLink("Links To Resources", href="/page-3", active="exact"),
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
                html.Li("Methane Leaks: Interactive map showcasing highest methane emissions and nearby energy sites."),
                html.Li("Rising Methane Emmissions: Graphical representations and visualizations of localised methane data trends."),
                html.Li("Methane Map: See where and when methane emmissions are highest."),
                html.Li("Increasing risks of methane-related health: Graphical visualisation in trends of respiratory, mental health and methane mortalities."),
                html.Li("Counties at health-risk: Identify which counties have highest methane and worst health outcomes."),
                html.Li("Racial impacts of methane emmissions: Graphs presenting methane-related mortalities and racial inequalities."),
                html.Li("Links to Resources: Comprehensive list of resources, papers, and articles related to methane emissions and impacts on health."),
            ]),
            html.H4("How to Use"),
            html.P("Navigate through the tabs at the sidebar to access different sections of the dashboard. Each section provides specific information and visualizations related to methane levels and health impacts. Use the interactive components to explore the data and gain insights."),
            html.P("We encourage policymakers to utilize this dashboard as a resource for evidence-based decision-making. By considering the data, visualizations, and resources provided here, policymakers can better understand the magnitude of methane emissions and the potential health risks associated with it. Additionally, we recommend referring to the 'Links to Resources' section for further in-depth research and reports."),
            html.Hr(),
            html.H4("Important Note"),
            html.P("This dashboard is for informational purposes only and should not be used as the sole basis for policymaking. It is crucial to consult domain experts, conduct further analysis, and consider additional factors when making policy decisions."),
            html.Hr(),
            html.H5("For more information, please visit the following pages:"),
            dbc.Nav(
                [
                    dbc.NavLink("Outsourcing levels", href="/page-1", active="exact"),
                    dbc.NavLink("Quality Impacts", href="/page-2", active="exact"),
                    dbc.NavLink("Links to Resources", href="/page-3", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
            html.Hr(),
            html.P("Acknowledgements: we are grateful to the support from Nuffield Foundation who motivated this dashboard."),
            html.P("This dashboard was first developed by Carolin Kroeger, Dunja Matic and Ben Goodair - we are grateful to the input of all team members."),
        ], style={"padding": "2rem"})
    elif pathname == "/page-1":
        return html.Div([
            dcc.Tabs(id="page-1-tabs", value='tab-1', children=[
                dcc.Tab(label='Outsourcing levels', value='tab-1', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Outsourcing geographies', value='tab-2', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Childrens homes expansion', value='tab-3', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles),
            html.Div(id='page-1-tabs-content')
        ])
    elif pathname == "/page-2":
        return html.Div([
            dcc.Tabs(id="page-2-tabs", value='tab-4', children=[
                dcc.Tab(label='double drop', value='tab-4', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='scatter LAs', value='tab-5', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='LA profiles', value='tab-6', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Relationship to outsourcing', value='tab-7', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles),
            html.Div(id='page-2-tabs-content')
        ])
    elif pathname == "/page-3":
        return html.Div([
            dcc.Tabs(id="page-3-tabs", value='tab-8', children=[
                dcc.Tab(label='Data download', value='tab-9', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Data upload', value='tab-10',style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Educational resources', value='tab-9', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Contact and feedback', value='tab-10', style=tab_style, selected_style=tab_selected_style),
            ], style=tabs_styles),
            html.Div(id='page-3-tabs-content')
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
            html.H3('See For-profit outsourcing in your Local Authority:'),
            dcc.Dropdown(
                id='LA-dropdown',
                options=[{'label': geog_n, 'value': geog_n} for geog_n in la_df['geog_n'].unique()],
                value=None,
                placeholder='Select a Local Authority',
                style={'width': '600px', 'margin-bottom': '20px'}
            ),
            dcc.Graph(
                id='scatter-plot'
            )        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('See levels of outsourcing in your area:'),
            dcc.Graph(id='map',  figure=map, style={'height': '1000px'})
            ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Look at the rise in for-profit childrens homes'),
            dcc.Graph(id='bar', style={'height': '600px'}),
            html.H3('Select time period:'),
            dcc.Slider(
                id='date-slider',
                min=provider_df['time'].min(),
                max=provider_df['time'].max(),
                value=provider_df['time'].min(),
                marks={str(time): (str(2005 - (provider_df['time'].min() - int(time)) // 12) if (int(time) - provider_df['time'].min()) % 12 == 0 else '')
                    for time in provider_df['time'].unique()},
                step=None,
                drag_value=True  # Enable dragging the slider handle smoothly
            )
        ])

@app.callback(Output('page-2-tabs-content', 'children'), [Input('page-2-tabs', 'value')])
def render_page_2_content(tab):
    if tab == 'tab-4':
        return  html.Div([
            html.H3('See the increasing risk of death from methane exposure and related causes:'),
            dcc.Dropdown(
                id='LA_dropdown2',
                options=[{'label': geog_n, 'value': geog_n} for geog_n in la_df_long['geog_n'].unique()],
                value=None,
                placeholder='Select a Local Authority'
            ),
            dcc.Dropdown(
                id='variable-dropdown',
                options=[{'label': Variable, 'value': Variable} for Variable in la_df_long['Variable'].unique()],
                value=None,
                placeholder='Select a Variable'
            ),
            dcc.Graph(id='double-drop')
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.H3('Find out which counties have high emissions and mortalities:'),
            dcc.Graph(id='Health visualisation', figure=tab5_fig)

        ])
    elif tab == 'tab-6':
        return  html.Div([
            html.H3('Find out which counties have high emissions and mortalities:'),
            dcc.Dropdown(
                id='race-dropdown',
                options=[{'label': race, 'value': race} for race in tab6_df['Single Race 6'].unique()],
                value=None,
                placeholder='Select a race'
            ),
            dcc.Graph(id='tab6-plot')            
        ])




@app.callback(Output('page-3-tabs-content', 'children'), [Input('page-3-tabs', 'value')])
def render_page_3_content(tab):
    if tab == 'tab-8':
        return  html.Div([
            html.H3('Data Downloads:'),
            html.P('You can access to three different files: Data at the lat/lon scale, county scale or state scale:'),
            html.Ul([
                html.Li(html.A("Download Methane Data with latitude and longitude", href="https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/methane_final_lonlat.csv")),
                html.Li(html.A("Download Health Data for US Counties", href="https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/methane_final_county.csv")),
                html.Li(html.A("Download Health Data for US States", href="https://raw.githubusercontent.com/BenGoodair/Methane_Dashboard/main/methane_final_county.csv"))])  
         ])




@app.callback(Output('scatter-plot', 'figure'),[Input('LA-dropdown', 'value')])
def update_scatter_plot(selected_county):
    if selected_county is None:
        filtered_df = la_df[['geog_n','year' ,'per_for_profit']]
    else:
        filtered_df = la_df[la_df['geog_n'] == selected_county]

    fig = px.scatter(filtered_df, x='year', y='per_for_profit', color='per_for_profit', trendline='lowess',
                     color_continuous_scale='ylorrd')
    fig.update_traces(marker=dict(size=5))
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='For-profit placements (%)',
        title='For-profit outsourcing 2011-22',
        coloraxis_colorbar=dict(title='For-profit %')
    )
    
    return fig


# Create a separate DataFrame for x-axis categories
sectors = provider_df['Sector'].unique()


@app.callback(Output('bar', 'figure'), [Input('date-slider', 'value')])
def update_bar_graph(selected_date):
    provider_df_filtered = provider_df[provider_df['time'] == selected_date]
    provider_df_filtered = provider_df_filtered.sort_values(by=['Sector'], key=lambda x: x.map({sector: i for i, sector in enumerate(sectors)}))

    bar = px.bar(provider_df_filtered, x='Sector', y='cumulative')

    # Customize the appearance with the color palette
    bar.update_traces(marker_color=colors)

    bar.update_layout(
        title='Cumulative Data by Sector',
        xaxis_title='Sector',
        yaxis_title='Cumulative',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black'),
        bargap=0.15,
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(sectors))),
            ticktext=sectors
        ),
    )

    return bar



@app.callback(Output('double-drop', 'figure'), [Input('LA-dropdown2', 'value'), Input('variable-dropdown', 'value')])
def update_scatter_plot(selected_county, selected_variable):
    if selected_county is None:
        filtered_df_dd = la_df_long[['geog_n','year' ,'per_for_profit']]
    else:
        filtered_df_dd = la_df_long[la_df_long['geog_n'] == selected_county]

    if selected_variable is None:
        filtered_df_dd = la_df_long[la_df_long['Variable'] == 'CLA_Mar']
    else:
        filtered_df_dd = la_df_long[la_df_long['Variable'] == selected_variable]



    fig_dd = px.scatter(filtered_df_dd, x='year', y='Value', color='Value', trendline='lowess',
                     color_continuous_scale='ylorrd')
    fig_dd.update_traces(marker=dict(size=5))
    fig_dd.update_layout(
        xaxis_title='Year',
        yaxis_title='Value',
        title='Children in care outcomes 2011-22',
        coloraxis_colorbar=dict(title='Value')
    )
    
    return fig_dd


if __name__ == '__main__':
    app.run_server(host='localhost',port=8005)






# z1, z2, z3 = np.random.random((3, 7, 7))

# customdata = np.dstack((z2, z3))
# mycustomdata = np.dstack((hospitals["company_name"], hospitals["number_of_employees"]))
# mycustomdata = mycustomdata.T.tolist()



# mycustomdata = np.dstack((hospitals["company_name"], hospitals["phone_number"], hospitals["number_of_employees"], hospitals["previous_leaks_n"], hospitals["fossil_fuel_type"], hospitals["number_of_beds"])).T.tolist(),






























