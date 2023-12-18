from dash import html, dcc, Output, Input
import plotly.express as px

from datasets import DataContainer


def render_page(tab_style, tab_selected_style, tabs_styles):
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


def register_callbacks(app, dataframes: DataContainer):
    la_df = dataframes.la_df
    nobs_final = dataframes.nobs_final
    exitdata = dataframes.exitdata
    merged2 = dataframes.merged2

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

    @app.callback(Output("scatter-plot", "figure"), Input("LA-dropdown", "value"))
    def update_scatter_plot(selected_county):
        filtered_df = la_df[la_df["variable"] == "Private provision"][
            ["LA_Name", "year", "percent"]
        ]

        if selected_county is not None:
            filtered_df = filtered_df[la_df["LA_Name"] == selected_county]

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
    def update_scatter_plot2(selected_county, selected_expenditure):
        filtered_df_spend = la_df[
            (la_df["category"] == "Expenditure")
            & (la_df["subcategory"] == "For_profit")
            & (la_df["variable"] == selected_expenditure)
        ]

        if selected_county is not None:
            filtered_df_spend = filtered_df_spend[la_df["LA_Name"] == selected_county]

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
