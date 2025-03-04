import os
from dash import html, dcc, Output, Input
import pandas as pd
import geopandas as gpd

import plotly.graph_objects as go
import numpy as np

import dash_bootstrap_components as dbc
import plotly.express as px
import dash
from dash.exceptions import PreventUpdate

### Init datasets
# Get the directory of the current script
dir_path = os.path.dirname(os.path.abspath(__file__))

# Define the paths to the CSV files relative to the script directory
la_df_path = os.path.join(dir_path, "..", "data", "processed", "la.csv")
nobs_final_path = os.path.join(dir_path, "..", "data", "processed", "nobs.csv")
exitdata_path = os.path.join(dir_path, "..", "data", "processed", "exits.csv")
merged2_path = os.path.join(dir_path, "..", "data", "processed", "merged.geojson")
active_chomes_path = os.path.join(
    dir_path, "..", "data", "processed", "active_chomes.csv"
)
outcomes_df_path = os.path.join(dir_path, "..", "data", "processed", "outcomes.csv")
placements_df_path = os.path.join(dir_path, "..", "data", "processed", "placements.csv")
expenditures_df_path = os.path.join(
    dir_path, "..", "data", "processed", "expenditures.csv"
)

# Read the CSV files
la_df = pd.read_csv(la_df_path)
nobs_final = pd.read_csv(nobs_final_path)
exitdata = pd.read_csv(exitdata_path)
merged2 = gpd.read_file(merged2_path)
active_chomes = pd.read_csv(active_chomes_path)
outcomes_df = pd.read_csv(outcomes_df_path)
placements_df = pd.read_csv(placements_df_path)
expenditures_df = pd.read_csv(expenditures_df_path)

####Dashboard####
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])


server = app.server

tabs_styles = {"height": "44px"}
tab_style = {
    "borderBottom": "1px solid #d6d6d6",
    "padding": "6px",
    "fontWeight": "bold",
}

tab_selected_style = {
    "borderTop": "1px solid #d6d6d6",
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "#119DFF",
    "color": "white",
    "padding": "6px",
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "transform": "scale(0.67)",  # Adjust the scale factor as needed
    "transform-origin": "top left",
    "height": "150%",  # Approximately compensating for 33% scale-down
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "11rem",
    "margin-right": "16rem",
    "transform": "scale(0.67)",  # Adjust the scale factor as needed
    "transform-origin": "top left",
    "padding": "2rem 1rem",
    "width": "125%",  # Approximately compensating for 33% scale-down
    "height": "150%",  # Approximately compensating for 33% scale-down
}

sidebar = html.Div(
    [
        html.H2("Outsourcing Impacts Tracker", className="display-7"),
        html.Hr(),
        html.P(
            "Welcome to a dashboard detailing the impacts of outsourcing in England's children social care sector.",
            className="lead",
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Outsourcing levels", href="/page-1", active="exact"),
                dbc.NavLink("Quality Impacts", href="/page-2", active="exact"),
                dbc.NavLink("Comparison tool", href="/page-3", active="exact"),
                dbc.NavLink("Links To Resources", href="/page-4", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)


watermark = html.Div(
    "Under-development; Not for dissemination",
    style={
        "position": "fixed",
        "bottom": "50%",  # Adjust the vertical position
        "right": "50%",  # Adjust the horizontal position
        "transform": "translate(50%, 50%) rotate(-45deg)",  # Rotate and position
        "color": "rgba(255, 0, 0, 0.4)",
        "fontSize": "70px",  # Increase the font size for better visibility
        "zIndex": "9999",
    },
)


# Incorporate the watermark into your layout
app.layout = html.Div([dcc.Location(id="url"), sidebar, content, watermark])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(
            [
                html.H2(
                    "Welcome to the Outsourcing Impacts Tracker Dashboard",
                    className="display-7",
                ),
                html.Hr(),
                html.H4("Purpose of the Dashboard"),
                html.P(
                    "The Outsourcing Impacts Dashboard aims to provide policymakers with valuable insights into outsourcing levels and their impact on quality of social care services in England. By visualizing outsoucing levels, service quality data, and related information, this dashboard assists policymakers in making informed decisions to address the challenges posed by increasing need for social care."
                ),
                html.H4("How to Use"),
                html.P(
                    "Navigate through the tabs at the sidebar to access different sections of the dashboard. Each section provides specific information and visualizations related to outsourcing levels and its impacts. Use the interactive components to explore the data and gain insights."
                ),
                html.P(
                    "We encourage policymakers to utilize this dashboard as a resource for evidence-based decision-making. By considering the data, visualizations, and resources provided here, policymakers can better understand the magnitude of outsouring and the potential risks associated with it. Additionally, we recommend referring to the 'Links to Resources' section for further in-depth research and reports."
                ),
                html.Hr(),
                html.H4("Important Note"),
                html.P(
                    "This dashboard is for informational purposes only and should not be used as the sole basis for policymaking. It is crucial to consult domain experts, conduct further analysis, and consider additional factors when making policy decisions."
                ),
                html.Hr(),
                html.H5("For more information, please visit the following pages:"),
                dbc.Nav(
                    [
                        dbc.NavLink(
                            "Outsourcing levels", href="/page-1", active="exact"
                        ),
                        dbc.NavLink("Quality Impacts", href="/page-2", active="exact"),
                        dbc.NavLink("Comparison tool", href="/page-3", active="exact"),
                        dbc.NavLink(
                            "Further Resources", href="/page-4", active="exact"
                        ),
                    ],
                    vertical=True,
                    pills=True,
                ),
                html.Hr(),
                html.Li(
                    [
                        html.Img(
                            src="https://github.com/BenGoodair/Outsourcing_Impact_Dashboard/blob/main/Images/Master-RGB-DarkGreen.png?raw=true",
                            style={"width": "150px", "height": "100px"},
                        ),
                        html.Div(
                            [
                                html.H4("Acknowledgements"),
                                html.P(
                                    "The Nuffield Foundation is an independent charitable trust with a mission to advance social well-being. It funds research that informs social policy, primarily in Education, Welfare, and Justice. The Nuffield Foundation is the founder and co-funder of the Nuffield Council on Bioethics, the Ada Lovelace Institute and the Nuffield Family Justice Observatory. The Foundation has funded this project, but the views expressed are those of the authors and not necessarily the Foundation. Website: www.nuffieldfoundation.org Twitter: @NuffieldFound"
                                ),
                                html.P(
                                    "A proof-of-concept version of this dashboard was first developed by Carolin Kroeger, Dunja Matic and Ben Goodair - we are grateful to the input of all team members."
                                ),
                            ],
                            style={"display": "inline-block", "vertical-align": "top"},
                        ),
                    ]
                ),
            ],
            style={"padding": "2rem"},
        )
    elif pathname == "/page-1":
        return html.Div(
            [
                dcc.Tabs(
                    id="page-1-tabs",
                    value="tab-1",
                    children=[
                        dcc.Tab(
                            label="Outsourced Placements",
                            value="tab-1",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Outsourced Spending",
                            value="tab-2",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Residential Care Providers",
                            value="tab-3",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Childrens homes exits/entries",
                            value="tab-4",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Outsourcing Geographies",
                            value="tab-5",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                    ],
                    style=tabs_styles,
                ),
                html.Div(id="page-1-tabs-content"),
            ]
        )
    elif pathname == "/page-2":
        return html.Div(
            [
                dcc.Tabs(
                    id="page-2-tabs",
                    value="tab-6",
                    children=[
                        dcc.Tab(
                            label="Ofsted ratings",
                            value="tab-6",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Children outcomes",
                            value="tab-7",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Placement quality",
                            value="tab-8",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                    ],
                    style=tabs_styles,
                ),
                html.Div(id="page-2-tabs-content"),
            ]
        )
    elif pathname == "/page-3":
        return html.Div(
            [
                dcc.Tabs(
                    id="page-3-tabs",
                    value="tab-9",
                    children=[
                        dcc.Tab(
                            label="Local authority comparison",
                            value="tab-9",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        #  dcc.Tab(label='Provider comparison', value='tab-10', style=tab_style, selected_style=tab_selected_style),
                    ],
                    style=tabs_styles,
                ),
                html.Div(id="page-3-tabs-content"),
            ]
        )
    elif pathname == "/page-4":
        return html.Div(
            [
                dcc.Tabs(
                    id="page-4-tabs",
                    value="tab-10",
                    children=[
                        dcc.Tab(
                            label="Data download",
                            value="tab-10",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Educational resources",
                            value="tab-11",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Contact and feedback",
                            value="tab-12",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                    ],
                    style=tabs_styles,
                ),
                html.Div(id="page-4-tabs-content"),
            ]
        )
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ],
        className="p-3 bg-light rounded-3",
    )


@app.callback(
    Output("page-1-tabs-content", "children"), [Input("page-1-tabs", "value")]
)
def render_page_1_content(tab):
    if tab == "tab-1":
        return html.Div(
            [
                html.H1("For-profit outsourcing of social care placements:"),
                html.H3("Select a Local Authority"),
                dcc.Dropdown(
                    id="LA-dropdown",
                    options=[
                        {"label": hop, "value": hop}
                        for hop in la_df[la_df["variable"] == "Private provision"][
                            "LA_Name"
                        ].unique()
                    ],
                    placeholder="All Local Authorities",
                    value=None,
                ),
                dcc.Graph(id="scatter-plot"),
            ]
        )
    elif tab == "tab-2":
        return html.Div(
            [
                html.H1("For-profit outsourcing of social care spending:"),
                html.Hr(),
                html.H3("Select a Local Authority"),
                dcc.Dropdown(
                    id="LA-dropdown3",
                    options=[
                        {"label": hop, "value": hop}
                        for hop in la_df[
                            (la_df["category"] == "Expenditure")
                            & (la_df["subcategory"] == "For_profit")
                        ]["LA_Name"].unique()
                    ],
                    value=None,
                    placeholder="All Local Authorities",
                    style={"width": "600px", "margin-bottom": "20px"},
                ),
                html.H3("Select an area of expenditure"),
                dcc.Dropdown(
                    id="spend-dropdown",
                    options=[
                        {"label": hop, "value": hop}
                        for hop in la_df[
                            (la_df["category"] == "Expenditure")
                            & (la_df["subcategory"] == "For_profit")
                        ]["variable"].unique()
                    ],
                    value="Total Children Looked After",
                    placeholder="Select an area of expenditure",
                    style={"width": "600px", "margin-bottom": "20px"},
                ),
                dcc.Graph(id="scatter-plot2"),
            ]
        )
    elif tab == "tab-3":
        return html.Div(
            [
                html.H1("Number of active children's homes and available places"),
                html.H3("Select a Local Authority"),
                dcc.Dropdown(
                    id="local-authority-dropdown",
                    options=[
                        {"label": la, "value": la}
                        for la in nobs_final["Local.authority"].unique()
                    ],
                    value=nobs_final["Local.authority"].unique()[0],
                ),
                html.H3("Select Number of Homes or Places"),
                dcc.Dropdown(
                    id="homes-or-places-dropdown",
                    options=[
                        {"label": hop, "value": hop}
                        for hop in nobs_final["Homes or places"].unique()
                    ],
                    value=nobs_final["Homes or places"].unique()[0],
                ),
                dcc.Graph(id="child-homes-plot"),
                html.H6(
                    "*Estimates based on the registration date of children's homes inspected since 2018"
                ),
            ]
        )
    elif tab == "tab-4":
        return html.Div(
            [
                html.H1("Children's homes entering or leaving the market"),
                html.H3("Exits or Entries"),
                dcc.Dropdown(
                    id="exit_entry_drop",
                    options=[
                        {"label": la, "value": la}
                        for la in exitdata["leave_join"].unique()
                    ],
                    value="Entries",
                ),
                html.H3("Select a Local Authority"),
                dcc.Dropdown(
                    id="exit-local-authority-dropdown",
                    options=[
                        {"label": la, "value": la}
                        for la in exitdata["Local.authority"].unique()
                    ],
                    value="All",
                ),
                html.H3("Select Number of Homes or Places"),
                dcc.Dropdown(
                    id="exit-homes-or-places-dropdown",
                    options=[
                        {"label": hop, "value": hop}
                        for hop in exitdata["Homes_or_places"].unique()
                    ],
                    value=exitdata["Homes_or_places"].unique()[0],
                ),
                dcc.Graph(id="exits_entries_plot"),
            ]
        )
    elif tab == "tab-5":
        return html.Div(
            [
                html.H1("Outsourcing Geographies"),
                html.H3("Select a measure of outsourcing"),
                dcc.Dropdown(
                    id="variable-dropdown",
                    options=[
                        {"label": la, "value": la}
                        for la in merged2["variable"].unique()
                    ],
                    value=merged2["variable"].unique()[2],
                ),
                dcc.Graph(id="outsourcing-map", style={"height": "1000px"}),
            ]
        )


@app.callback(
    Output("page-2-tabs-content", "children"), [Input("page-2-tabs", "value")]
)
def render_page_2_content(tab):
    if tab == "tab-6":
        return html.Div(
            [
                html.H1("Ofsted ratings of active children homes:"),
                html.Hr(),
                html.H6("Select an inspection domain:"),
                html.Hr(),
                dcc.Dropdown(
                    id="domain-dropdown",
                    options=[
                        {"label": geog_n, "value": geog_n}
                        for geog_n in active_chomes["Domain"].unique()
                    ],
                    value="Overall.experiences.and.progress.of.children.and.young.people",
                    placeholder="Select an inspection domain",
                ),
                html.Hr(),
                dcc.Graph(id="ofsted-plot", style={"height": "800px"}),
            ]
        )
    elif tab == "tab-7":
        return html.Div(
            [
                html.H1("Outcomes for children in care and care leavers"),
                html.H3("Select a Local Authority"),
                dcc.Dropdown(
                    id="la-dropdown4",
                    options=[
                        {"label": geog_n, "value": geog_n}
                        for geog_n in outcomes_df["LA_Name"].unique()
                    ],
                    value=None,
                    placeholder="All",
                ),
                html.H3("Select a subcategory"),
                dcc.Dropdown(
                    id="subcategory-dropdown4",
                    options=[
                        {"label": geog_n, "value": geog_n}
                        for geog_n in outcomes_df["subcategory"].unique()
                    ],
                    value="Health and criminalisation",
                    placeholder="Select a subcategory",
                ),
                html.H3("Select a variable"),
                dcc.Dropdown(
                    id="variable-dropdown4",
                    options=variable_options,  # Add this line to populate initial options
                    placeholder="Select a variable",
                ),
                dcc.Graph(id="outcome_plot"),
            ]
        )
    elif tab == "tab-8":
        return html.Div(
            [
                html.H1("Quality of placements"),
                html.H3("Select a Local Authority"),
                dcc.Dropdown(
                    id="la-dropdown5",
                    options=[
                        {"label": geog_n, "value": geog_n}
                        for geog_n in placements_df["LA_Name"].unique()
                    ],
                    value=None,
                    placeholder="All",
                ),
                html.H3("Select a subcategory"),
                dcc.Dropdown(
                    id="subcategory-dropdown5",
                    options=[
                        {"label": geog_n, "value": geog_n}
                        for geog_n in placements_df["subcategory"].unique()
                    ],
                    value="Locality of placement",
                    placeholder="Select a subcategory",
                ),
                html.H3("Select a variable"),
                dcc.Dropdown(
                    id="variable-dropdown5",
                    options=variable_options2,  # Add this line to populate initial options
                    placeholder="Select a variable",
                ),
                dcc.Graph(id="placement_plot"),
            ]
        )


@app.callback(
    Output("page-3-tabs-content", "children"), [Input("page-3-tabs", "value")]
)
def render_page_3_content(tab):
    if tab == "tab-9":
        return html.Div(
            [
                dcc.Dropdown(
                    id="la-dropdown6",
                    options=[
                        {"label": la, "value": la}
                        for la in outcomes_df["LA_Name"].unique()
                    ],
                    multi=True,
                    placeholder="Select Local Authorities to compare",
                ),
                dcc.Dropdown(
                    id="data-dropdown",
                    options=[
                        {"label": la, "value": la}
                        for la in ["Placements", "Expenditure", "Outcomes"]
                    ],
                    multi=False,
                    placeholder="Select Dataset",
                ),
                dcc.Dropdown(
                    id="subcategory-dropdown6",
                    options=[
                        {"label": subcat, "value": subcat}
                        for subcat in outcomes_df["subcategory"].unique()
                    ],
                    placeholder="Select Subcategory",
                ),
                dcc.Dropdown(id="variable-dropdown6", placeholder="Select Variable"),
                dcc.Graph(id="compare_plot"),
            ]
        )
    else:
        raise PreventUpdate


@app.callback(
    Output("page-4-tabs-content", "children"), [Input("page-4-tabs", "value")]
)
def render_page_4_content(tab):
    if tab == "tab-10":
        return html.Div(
            [
                html.H1("Data Downloads:"),
                html.H3("Our cleaned data is available here:"),
                html.Ul(
                    [
                        html.Li(
                            html.A(
                                "All data for LAs (large file warning)",
                                href="https://raw.githubusercontent.com/BenGoodair/childrens_social_care_data/main/Final_Data/outputs/dashboard_data.csv",
                            )
                        ),
                        html.Li(
                            html.A(
                                "All data for providers",
                                href="https://raw.githubusercontent.com/BenGoodair/childrens_social_care_data/main/Final_Data/outputs/Provider_data.csv",
                            )
                        ),
                        html.Li(
                            html.A(
                                "Full coding library for how data was produced",
                                href="https://github.com/BenGoodair/childrens_social_care_data/tree/main",
                            )
                        ),
                    ]
                ),
                html.H3("Original data is available at these locations:"),
                html.Ul(
                    [
                        html.Li(
                            html.A(
                                "Outcomes for children in care",
                                href="https://www.gov.uk/government/statistics/outcomes-for-children-in-need-including-children-looked-after-by-local-authorities-in-england-2021-to-2022",
                            )
                        ),
                        html.Li(
                            html.A(
                                "Placements for children in care",
                                href="https://www.gov.uk/government/statistics/children-looked-after-in-england-including-adoption-2021-to-2022",
                            )
                        ),
                        html.Li(
                            html.A(
                                "Expenditure on children in care",
                                href="https://explore-education-statistics.service.gov.uk/find-statistics/la-and-school-expenditure/2021-22",
                            )
                        ),
                    ]
                ),
            ]
        )
    elif tab == "tab-11":
        return html.Div(
            [
                html.H1("Links to Resources"),
                html.H3("Research from our team"),
                html.H6("Research on outsourcing of children's social care"),
                html.Ul(
                    [
                        html.Li(
                            html.A(
                                "Do for-profit childrens homes outperform council-run homes?",
                                href="https://www.sciencedirect.com/science/article/pii/S0277953622006293",
                            )
                        ),
                        html.Li(
                            html.A(
                                "Does outsourcing correspond with better or worse quality placements for children?",
                                href="https://www.sciencedirect.com/science/article/pii/S0277953622006293",
                            )
                        ),
                        html.Li(
                            html.A(
                                "Why do Local Authorities outsource services?",
                                href="https://www.sciencedirect.com/science/article/pii/S0277953621001763",
                            )
                        ),
                        html.Li(
                            html.A(
                                "Do Local Authorities achieve market stewardship?",
                                href="https://ora.ox.ac.uk/objects/uuid:4465898b-0b98-4c08-aa84-feb89aa54280/files/sqz20st49v",
                            )
                        ),
                    ]
                ),
                html.H6("Research on outsourcing of adult's social care"),
                html.Ul(
                    [
                        html.Li(
                            html.A(
                                "Did for-profit nursing homes perform well during COVID-19 outbreaks?",
                                href="https://pubmed.ncbi.nlm.nih.gov/37118328/",
                            )
                        ),
                        html.Li(
                            html.A(
                                "What are the issues with ownership in the adult social care sector?",
                                href="https://www.thelancet.com/journals/lanhl/article/PIIS2666-7568(22)00040-X/fulltext?msclkid=014e07e2ab8211ec8",
                            )
                        ),
                        html.Li(
                            html.A(
                                "Do for-profit care homes outperform others in Scotland?",
                                href="https://bmjopen.bmj.com/content/9/2/e022975",
                            )
                        ),
                        html.Li(
                            html.A(
                                "Do for-profit care homes break fewer regulations than others in Scotland?",
                                href="https://journals.sagepub.com/doi/full/10.1177/08997640211001448",
                            )
                        ),
                        html.Li(
                            html.A(
                                "What happens when investment firms take over care homes?",
                                href="https://s3.eu-central-1.amazonaws.com/eu-st01.ext.exlibrisgroup.com/44SUR_INST/storage/alma/1C/69/8B/17/1D/46/D6/A0/69/BD/51/B8/09/AD/93/D6/UNISON-CUSP%20report%20%28final%29.pdf?response-content-type=application%2Fpdf&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231108T143557Z&X-Amz-SignedHeaders=host&X-Amz-Expires=119&X-Amz-Credential=AKIAJN6NPMNGJALPPWAQ%2F20231108%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Signature=dd661f07699e6063a691afea28b63c2c29fd15e66caaf7875a65b59c11d91e60",
                            )
                        ),
                    ]
                ),
                html.H6("Research on outsourcing of healthcare"),
                html.Li(
                    html.A(
                        "What is the impact of outsourcing healthcare services on quality of care?",
                        href="https://www.thelancet.com/journals/lanpub/article/PIIS2468-2667(22)00133-5/fulltext?trk=organization_guest_main-feed-card_feed-article-content",
                    )
                ),
                html.Li(
                    html.A(
                        "Why do NHS commissioners outsource healthcare services?",
                        href="https://www.sciencedirect.com/science/article/pii/S0168851023002269?via%3Dihub",
                    )
                ),
                html.H3("Project Information"),
                html.Ul(
                    [
                        html.Li(
                            html.A(
                                "We are incredibly grateful for the support of Nuffield Foundation for funding this project, you can view our project homepage here:",
                                href="https://www.nuffieldfoundation.org/project/evidencing-the-outsourcing-of-social-care-provision-in-england",
                            )
                        ),
                        html.Li(
                            html.A(
                                "The project has been funded by the Nuffield Foundation, but the view expressed are those of the authors and not necessarily the Foundation. Visit: www.nuffieldfoundation.org",
                                href="https://www.nuffieldfoundation.org",
                            )
                        ),
                    ]
                ),
            ]
        )
    elif tab == "tab-12":
        return html.Div(
            [
                html.H3("Meet the team:"),
                html.Ul(
                    [
                        html.Li(
                            [
                                html.Img(
                                    src="https://github.com/BenGoodair/Outsourcing_Impact_Dashboard/blob/main/Images/anders_bach-mortensen.jpg?raw=true",
                                    style={"width": "100px", "height": "100px"},
                                ),
                                html.Div(
                                    [
                                        html.H4("Anders"),
                                        html.P(
                                            "Anders is a social scientist with expertise on outsourcing, social care services and systematic review methods."
                                        ),
                                        html.P(
                                            "Anders was national champion fencer in his youth - he now uses skills of precision in interpretting complex statistical models."
                                        ),
                                    ],
                                    style={
                                        "display": "inline-block",
                                        "vertical-align": "top",
                                    },
                                ),
                            ]
                        ),
                        html.Li(
                            [
                                html.Img(
                                    src="https://github.com/BenGoodair/Outsourcing_Impact_Dashboard/blob/main/Images/Michelle.jpg?raw=true",
                                    style={"width": "100px", "height": "100px"},
                                ),
                                html.Div(
                                    [
                                        html.H4("Michelle"),
                                        html.P(
                                            "Michelle is a Research Assistant Professor with the U-M Institute for Firearm Injury Prevention."
                                        ),
                                        html.P(
                                            "Michelle's favourite colour is the same as Hilary Clinton's"
                                        ),
                                    ],
                                    style={
                                        "display": "inline-block",
                                        "vertical-align": "top",
                                    },
                                ),
                            ]
                        ),
                        html.Li(
                            [
                                html.Img(
                                    src="https://github.com/BenGoodair/Outsourcing_Impact_Dashboard/blob/main/Images/christine.jpg?raw=true",
                                    style={"width": "100px", "height": "100px"},
                                ),
                                html.Div(
                                    [
                                        html.H4("Christine"),
                                        html.P(
                                            "Christine is a political economist who specialises in postgrowth economics and the privatisation of social care."
                                        ),
                                        html.P(
                                            "Christine once told Emma Watson that her shoelaces were undone."
                                        ),
                                    ],
                                    style={
                                        "display": "inline-block",
                                        "vertical-align": "top",
                                    },
                                ),
                            ]
                        ),
                        html.Li(
                            [
                                html.Img(
                                    src="https://github.com/BenGoodair/Methane_Dashboard/blob/main/ben.jpg?raw=true",
                                    style={"width": "100px", "height": "100px"},
                                ),
                                html.Div(
                                    [
                                        html.H4("Ben"),
                                        html.P(
                                            "Ben is a social researcher identifying the impacts of privatization on health and social care systems."
                                        ),
                                        html.P(
                                            "Ben will embroider any form of data visualisation he thinks worthy of the thread."
                                        ),
                                    ],
                                    style={
                                        "display": "inline-block",
                                        "vertical-align": "top",
                                    },
                                ),
                            ]
                        ),
                        html.Li(
                            [
                                html.Img(
                                    src="https://github.com/BenGoodair/Outsourcing_Impact_Dashboard/blob/main/Images/jane.png?raw=true",
                                    style={"width": "100px", "height": "100px"},
                                ),
                                html.Div(
                                    [
                                        html.H4("Jane"),
                                        html.P(
                                            "Jane is Professor of Evidence Based Intervention and Policy Evaluation at the Department of Social Policy and Intervention, University of Oxford."
                                        ),
                                        html.P(
                                            "Jane once owned a stick insect call Stephen."
                                        ),
                                    ],
                                    style={
                                        "display": "inline-block",
                                        "vertical-align": "top",
                                    },
                                ),
                            ]
                        ),
                    ]
                ),
                html.H3("Partner with us:"),
                html.H6("Join our team to continue this work"),
                html.P(
                    "We are looking for partners with policy, industrial or lived experiences to join our happy community!"
                ),
                html.Ul(
                    [
                        html.Li(
                            "We can write a funding application to ensure labor compensated and valued."
                        ),
                        html.Li(
                            "We want new directions and ideas, bring your creativity!"
                        ),
                        html.Li(
                            "We want to have fun and work in a respectful, supportive, and positive way."
                        ),
                    ]
                ),
                html.H3("Contact and feedback"),
                html.H6("Help us improve this dashboard for your needs!"),
                html.P(
                    "All our work is completely open access and reproducible, we'd love to work with you to apply this work to other data"
                ),
                html.Ul(
                    [
                        html.Li("Email us at: benjamin.goodair@spi.ox.ac.uk"),
                        html.Li("Tweet us at: @BenGoodair"),
                        html.Li("Find us at: DSPI, Oxford, United Kingdom"),
                    ]
                ),
            ]
        )


@app.callback(Output("scatter-plot", "figure"), Input("LA-dropdown", "value"))
def update_scatter_plot(selected_county):
    #    filtered_df = la_df[la_df['variable']=="Private provision"][la_df['LA_Name'] == selected_county]

    if selected_county is None:
        filtered_df = la_df[la_df["variable"] == "Private provision"][
            ["LA_Name", "year", "percent"]
        ]
    else:
        filtered_df = la_df[la_df["variable"] == "Private provision"][
            la_df["LA_Name"] == selected_county
        ]

    fig1 = px.scatter(
        filtered_df,
        x="year",
        y="percent",
        color="percent",
        trendline="lowess",
        color_continuous_scale="ylorrd",
    )
    fig1.update_traces(marker=dict(size=5))
    fig1.update_layout(
        xaxis_title="Year",
        yaxis_title="For-profit placements (%)",
        title="Percent of children placed with for-profit providers 2011-22",
        coloraxis_colorbar=dict(title="For-profit %"),
    )

    return fig1


@app.callback(
    Output("scatter-plot2", "figure"),
    Input("LA-dropdown3", "value"),
    Input("spend-dropdown", "value"),
)
def update_scatter_plot(selected_county, selected_expenditure):
    if selected_county is None or selected_county == "":
        filtered_df_spend = la_df[
            (la_df["category"] == "Expenditure")
            & (la_df["subcategory"] == "For_profit")
            & (la_df["variable"] == selected_expenditure)
        ]
    else:
        filtered_df_spend = la_df[
            (la_df["category"] == "Expenditure")
            & (la_df["subcategory"] == "For_profit")
            & (la_df["LA_Name"] == selected_county)
            & (la_df["variable"] == selected_expenditure)
        ]

    fig2 = px.scatter(
        filtered_df_spend,
        x="year",
        y="percent",
        color="percent",
        trendline="lowess",
        color_continuous_scale="ylorrd",
    )
    fig2.update_traces(marker=dict(size=5))
    fig2.update_layout(
        xaxis_title="Year",
        yaxis_title="For-profit expenditure (%)",
        title="Percent of expenditure on for-profit providers 2011-22",
        coloraxis_colorbar=dict(title="For-profit %"),
    )

    return fig2


# Create a separate DataFrame for x-axis categories
sectors = nobs_final["Sector"].unique()


@app.callback(
    Output("child-homes-plot", "figure"),
    Input("local-authority-dropdown", "value"),
    Input("homes-or-places-dropdown", "value"),
)
def update_plot(selected_local_authority, selected_homes_or_places):
    filtered_nobs = nobs_final[
        (nobs_final["Local.authority"] == selected_local_authority)
        & (nobs_final["Homes or places"] == selected_homes_or_places)
    ]

    custom_colors = {
        "For-profit": "#1f77b4",
        "Local Authority": "#ff7f0e",
        "Third Sector": "#2ca02c",
    }

    fig = px.scatter(
        filtered_nobs,
        x="time",
        y="cumulative",
        color="Sector",
        color_discrete_map=custom_colors,
    )

    # Add a line trace
    line_data = (
        filtered_nobs[filtered_nobs["time"] > -211]
        .groupby(["time", "Sector"])["cumulative"]
        .sum()
        .reset_index()
    )
    for sector in line_data["Sector"].unique():
        sector_data = line_data[line_data["Sector"] == sector]
        fig.add_trace(
            go.Scatter(
                x=sector_data["time"],
                y=sector_data["cumulative"],
                mode="lines+markers",
                name=sector,
                line=dict(color=custom_colors[sector]),
                showlegend=False,
            )
        )  # Hide the legend for the line traces

    # Define custom tick values and labels for the x-axis
    custom_tick_values = [-11, -35, -59, -83, -107, -131, -155, -179, -203, -227]
    custom_tick_labels = [
        "2022",
        "2020",
        "2018",
        "2016",
        "2014",
        "2012",
        "2010",
        "2008",
        "2006",
        "2004",
    ]

    # Update the x-axis with the custom tick values and labels
    fig.update_xaxes(tickvals=custom_tick_values, ticktext=custom_tick_labels)

    fig.update_layout(
        title=f"Number of active children's homes ({selected_local_authority}, {selected_homes_or_places})",
        xaxis_title="Year",
        yaxis_title=f"Number of Children's residential{selected_homes_or_places}",
    )
    return fig


@app.callback(
    Output("exits_entries_plot", "figure"),
    Input("exit_entry_drop", "value"),
    Input("exit-local-authority-dropdown", "value"),
    Input("exit-homes-or-places-dropdown", "value"),
)
def update_plot(
    selected_exits_entries, selected_local_authority, selected_homes_or_places
):
    filtered_exits = exitdata[
        (exitdata["leave_join"] == selected_exits_entries)
        & (exitdata["Local.authority"] == selected_local_authority)
        & (exitdata["Homes_or_places"] == selected_homes_or_places)
    ]

    custom_colors = {
        "For-profit": "#1f77b4",
        "Local Authority": "#ff7f0e",
        "Third Sector": "#2ca02c",
    }

    # Convert 'year' column to categorical with ordered levels
    filtered_exits["year"] = pd.Categorical(filtered_exits["year"], ordered=True)

    fig = px.bar(
        filtered_exits,
        x="year",
        y="value",
        color="Sector",
        barmode="group",
        color_discrete_map=custom_colors,
        category_orders={"year": filtered_exits["year"].sort_values().unique()},
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number",
        title="Childrens home entries or exits",
    )

    return fig


@app.callback(Output("outsourcing-map", "figure"), Input("variable-dropdown", "value"))
def update_plot(selected_variable):
    filtered_merged = merged2[merged2["variable"] == selected_variable]

    min_value = filtered_merged["variable"].min()
    max_value = filtered_merged["variable"].max()

    map = px.choropleth_mapbox(
        filtered_merged,
        geojson=filtered_merged.geometry,
        locations=filtered_merged.index,
        color="percent",
        color_continuous_scale="ylorrd",
        center={"lat": 52.9781, "lon": -1.82360},
        mapbox_style="open-street-map",
        hover_name="LA_Name",
        zoom=6,
    )

    return map


@app.callback(Output("ofsted-plot", "figure"), Input("domain-dropdown", "value"))
def update_scatter_plot(selected_domain):
    filtered_active_chomes = active_chomes[active_chomes["Domain"] == selected_domain]

    # Create a unique circle identifier for each 'Overall.experiences'
    filtered_active_chomes["Circle"] = filtered_active_chomes.groupby("Rating").ngroup()

    # Define the custom order for 'Overall.experiences'
    custom_order = [
        "Inadequate",
        "Requires improvement to be good",
        "Good",
        "Outstanding",
    ]

    # Create a Categorical data type with the desired order
    filtered_active_chomes["Overall_Experiences_Mapping"] = pd.Categorical(
        filtered_active_chomes["Rating"], categories=custom_order, ordered=True
    )

    # Define a function to add points within a circle
    def add_points_in_circle(group):
        radius = 0.9  # Adjust this value to control the radius of the circles

        # Calculate the number of points based on the total number of rows in the group
        num_points = len(group)

        # Generate random angles and radii within the circle for each group
        theta = np.linspace(0, 2 * np.pi, num_points)
        r = np.sqrt(np.random.uniform(0, 1, num_points)) * radius

        group["Jittered_x"] = group["Circle"] + r * np.cos(theta)
        group["Jittered_y"] = group[
            "Overall_Experiences_Mapping"
        ].cat.codes + r * np.sin(theta)
        return group

    # Apply the point addition function to each group
    filtered_active_chomes = (
        filtered_active_chomes.groupby("Circle")
        .apply(add_points_in_circle)
        .reset_index(drop=True)
    )

    # Create a bubble chart with perfectly filled huge bubbles filled with jittered points in both dimensions
    ofsted_fig = px.scatter(
        filtered_active_chomes,
        x="Jittered_x",
        y="Jittered_y",
        color="Sector",
        hover_name="Organisation.which.owns.the.provider",
        custom_data=[
            "Rating",
            "Places",
            "Registration.date",
            "Local.authority",
            "Sector",
        ],
        labels={"Sector": "Sector"},
        title="Active Children's Homes - as of March 2023",
    )

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
    ofsted_fig.update_xaxes(
        showline=False, showgrid=False, showticklabels=False, title_text=""
    )
    ofsted_fig.update_yaxes(
        showline=False, showgrid=False, showticklabels=False, title_text=""
    )
    ofsted_fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)"  # Set the background color to transparent
    )

    print(filtered_active_chomes["Circle"].unique())

    for group, group_data in filtered_active_chomes.groupby("Circle"):
        # Calculate the position for the label above the group
        x_label = group_data["Jittered_x"].mean()
        y_label = (
            group_data["Jittered_y"].max() + 0.12
        )  # Adjust the vertical position as needed

        # Get the mode (most common category) for the 'Overall_Experiences_Mapping' in the group
        rating = group_data["Overall_Experiences_Mapping"].value_counts().idxmax()

        # Add a text annotation to the figure
        ofsted_fig.add_annotation(
            x=x_label,
            y=y_label,
            text=rating,
            showarrow=False,
            font=dict(size=16),
            opacity=0.9,
        )

    return ofsted_fig


variable_options = []  # No options if no subcategory is selected


@app.callback(
    Output("variable-dropdown4", "options"), Input("subcategory-dropdown4", "value")
)
def update_variable_options(selected_subcategory):
    if selected_subcategory:
        # Filter the DataFrame based on the selected subcategory
        filtered_df = outcomes_df[outcomes_df["subcategory"] == selected_subcategory]

        # Get the unique variable options from the filtered DataFrame
        variable_options = [
            {"label": variable, "value": variable}
            for variable in filtered_df["variable"].unique()
        ]
    else:
        variable_options = []  # No options if no subcategory is selected

    return variable_options


@app.callback(
    Output("outcome_plot", "figure"),
    Input("la-dropdown4", "value"),
    Input("subcategory-dropdown4", "value"),
    Input("variable-dropdown4", "value"),
)
def update_outcome_plot(selected_county, selected_subcategory, selected_variable):
    print("Selected County:", selected_county)
    print("Selected Subcategory:", selected_subcategory)
    print("Selected Variable:", selected_variable)

    # Filter the data based on the selected values
    if selected_county is None or selected_county == "":
        filtered_df_outcome = outcomes_df[
            (outcomes_df["subcategory"] == selected_subcategory)
            & (outcomes_df["variable"] == selected_variable)
        ].copy()
    else:
        filtered_df_outcome = outcomes_df[
            (outcomes_df["subcategory"] == selected_subcategory)
            & (outcomes_df["LA_Name"] == selected_county)
            & (outcomes_df["variable"] == selected_variable)
        ].copy()

    print("Filtered Data:")
    print(filtered_df_outcome)

    outcome_plot = px.scatter(
        filtered_df_outcome,
        x="year",
        y="percent",
        color="percent",
        trendline="lowess",
        color_continuous_scale="ylorrd",
    )
    outcome_plot.update_traces(marker=dict(size=5))
    outcome_plot.update_layout(
        xaxis_title="Year",
        yaxis_title="(%)",
        title="Outcomes for children in care",
        coloraxis_colorbar=dict(title=selected_variable),
    )

    return outcome_plot


variable_options2 = []  # No options if no subcategory is selected


@app.callback(
    Output("variable-dropdown5", "options"), Input("subcategory-dropdown5", "value")
)
def update_variable_options(selected_subcategory):
    if selected_subcategory:
        # Filter the DataFrame based on the selected subcategory
        filtered_df = placements_df[
            placements_df["subcategory"] == selected_subcategory
        ]

        # Get the unique variable options from the filtered DataFrame
        variable_options2 = [
            {"label": variable, "value": variable}
            for variable in filtered_df["variable"].unique()
        ]
    else:
        variable_options2 = []  # No options if no subcategory is selected

    return variable_options2


@app.callback(
    Output("placement_plot", "figure"),
    Input("la-dropdown5", "value"),
    Input("subcategory-dropdown5", "value"),
    Input("variable-dropdown5", "value"),
)
def update_outcome_plot(selected_county, selected_subcategory, selected_variable):
    print("Selected County:", selected_county)
    print("Selected Subcategory:", selected_subcategory)
    print("Selected Variable:", selected_variable)

    # Filter the data based on the selected values
    if selected_county is None or selected_county == "":
        filtered_df_placement = placements_df[
            (placements_df["subcategory"] == selected_subcategory)
            & (placements_df["variable"] == selected_variable)
        ].copy()
    else:
        filtered_df_placement = placements_df[
            (placements_df["subcategory"] == selected_subcategory)
            & (placements_df["LA_Name"] == selected_county)
            & (placements_df["variable"] == selected_variable)
        ].copy()

    # print("Filtered Data:")
    # print(filtered_df_placement)

    placement_plot = px.scatter(
        filtered_df_placement,
        x="year",
        y="percent",
        color="percent",
        trendline="lowess",
        color_continuous_scale="ylorrd",
    )
    placement_plot.update_traces(marker=dict(size=5))
    placement_plot.update_layout(
        xaxis_title="Year",
        yaxis_title="(%)",
        title="Placements for children in care",
        coloraxis_colorbar=dict(title=selected_variable),
    )

    return placement_plot


variable_options4 = []  # No options if no subcategory is selected


@app.callback(
    Output("subcategory-dropdown6", "options"), Input("data-dropdown", "value")
)
def update_subcategory_options(selected_dataset):
    if selected_dataset:
        # Filter the DataFrame based on the selected dataset
        if selected_dataset == "Outcomes":
            filtered_df = outcomes_df
        elif selected_dataset == "Expenditure":
            filtered_df = expenditures_df
        elif selected_dataset == "Placements":
            filtered_df = placements_df
        else:
            filtered_df = (
                outcomes_df  # Default to Outcomes DataFrame if dataset is not selected
            )

            # Get the unique subcategory options from the filtered DataFrame
        subcategory_options = [
            {"label": subcategory, "value": subcategory}
            for subcategory in filtered_df["subcategory"].unique()
        ]
    else:
        subcategory_options = []  # No options if no dataset is selected

    return subcategory_options


@app.callback(
    Output("variable-dropdown6", "options"), Input("subcategory-dropdown6", "value")
)
def update_variable_options(selected_subcategory):
    if selected_subcategory:
        # Filter the DataFrame based on the selected subcategory
        if selected_subcategory in outcomes_df["subcategory"].unique():
            filtered_df = outcomes_df[
                outcomes_df["subcategory"] == selected_subcategory
            ]
        elif selected_subcategory in expenditures_df["subcategory"].unique():
            filtered_df = expenditures_df[
                expenditures_df["subcategory"] == selected_subcategory
            ]
        elif selected_subcategory in placements_df["subcategory"].unique():
            filtered_df = placements_df[
                placements_df["subcategory"] == selected_subcategory
            ]
        else:
            return []

            # Get the unique variable options from the filtered DataFrame
        variable_options = [
            {"label": variable, "value": variable}
            for variable in filtered_df["variable"].unique()
        ]
    else:
        variable_options = []  # No options if no subcategory is selected
    return variable_options


@app.callback(
    Output("compare_plot", "figure"),
    [
        Input("la-dropdown6", "value"),
        Input("data-dropdown", "value"),
        Input("subcategory-dropdown6", "value"),
        Input("variable-dropdown6", "value"),
    ],
)
def update_comparison_plot(
    selected_local_authorities,
    selected_dataset,
    selected_subcategory,
    selected_variable,
):
    if not selected_local_authorities or not selected_dataset or not selected_variable:
        return {"data": []}

    # Select the appropriate DataFrame based on the selected dataset and variable
    if selected_dataset == "Outcomes":
        filtered_df = outcomes_df[
            (outcomes_df["variable"] == selected_variable)
            & (outcomes_df["subcategory"] == selected_subcategory)
            & (outcomes_df["LA_Name"].isin(selected_local_authorities))
        ]
    elif selected_dataset == "Expenditure":
        filtered_df = expenditures_df[
            (expenditures_df["variable"] == selected_variable)
            & (expenditures_df["subcategory"] == selected_subcategory)
            & (expenditures_df["LA_Name"].isin(selected_local_authorities))
        ]
    elif selected_dataset == "Placements":
        filtered_df = placements_df[
            (placements_df["variable"] == selected_variable)
            & (placements_df["subcategory"] == selected_subcategory)
            & (placements_df["LA_Name"].isin(selected_local_authorities))
        ]
    else:
        return {"data": []}

    fig = px.scatter(filtered_df, x="year", y="percent", color="LA_Name")
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title=selected_variable,
        title=f'Comparison of {selected_variable} between {", ".join(selected_local_authorities)}',
    )

    # Add a line trace to the plot
    for la in selected_local_authorities:
        line_data = filtered_df[filtered_df["LA_Name"] == la].sort_values(by="year")
        fig.add_trace(
            go.Scatter(
                x=line_data["year"], y=line_data["percent"], mode="lines", name=la
            )
        )

    return fig


if __name__ == "__main__":
    app.run_server(debug=False)
