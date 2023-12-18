from dash import html, dcc, Output, Input
from datasets import DataContainer
import plotly.express as px


def render_page(tab_style, tab_selected_style, tabs_styles):
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


def register_callbacks(app, dataframes: DataContainer):
    active_chomes = dataframes.active_chomes
    outcomes_df = dataframes.outcomes_df
    placements_df = dataframes.placements_df
    variable_options = []
    variable_options2 = []

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
        Output("variable-dropdown4", "options"), Input("subcategory-dropdown4", "value")
    )
    def update_variable_options(selected_subcategory):
        if selected_subcategory:
            # Filter the DataFrame based on the selected subcategory
            filtered_df = outcomes_df[
                outcomes_df["subcategory"] == selected_subcategory
            ]

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
