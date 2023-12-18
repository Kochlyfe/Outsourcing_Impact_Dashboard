from dash import html, dcc, Output, Input
from datasets import DataContainer
import plotly.express as px
import pandas as pd
import numpy as np


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

    @app.callback(Output("ofsted-plot", "figure"), Input("domain-dropdown", "value"))
    def update_ofsted_plot(selected_domain):
        filtered_active_chomes = active_chomes[
            active_chomes["Domain"] == selected_domain
        ]

        # Create a unique circle identifier for each 'Overall.experiences'
        filtered_active_chomes["Circle"] = filtered_active_chomes.groupby(
            "Rating"
        ).ngroup()

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

    @app.callback(
        Output("variable-dropdown5", "options"), Input("subcategory-dropdown5", "value")
    )
    def update_variable_options_dropdown5(selected_subcategory):
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
    def update_placement_plot(selected_county, selected_subcategory, selected_variable):
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
