from dash import html
import dash_bootstrap_components as dbc


def render_page():
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
                    dbc.NavLink("Outsourcing levels", href="/page-1", active="exact"),
                    dbc.NavLink("Quality Impacts", href="/page-2", active="exact"),
                    dbc.NavLink("Comparison tool", href="/page-3", active="exact"),
                    dbc.NavLink("Further Resources", href="/page-4", active="exact"),
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
