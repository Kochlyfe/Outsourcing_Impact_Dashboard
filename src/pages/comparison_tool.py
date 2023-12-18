from dash import html, dcc, Output, Input
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go

from datasets import DataContainer


def render_page(tab_style, tab_selected_style, tabs_styles):
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


def register_callbacks(app, dataframes: DataContainer):
    outcomes_df = dataframes.outcomes_df
    expenditures_df = dataframes.expenditures_df
    placements_df = dataframes.placements_df

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
                    dcc.Dropdown(
                        id="variable-dropdown6", placeholder="Select Variable"
                    ),
                    dcc.Graph(id="compare_plot"),
                ]
            )
        else:
            raise PreventUpdate

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
                filtered_df = outcomes_df  # Default to Outcomes DataFrame if dataset is not selected

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
        if (
            not selected_local_authorities
            or not selected_dataset
            or not selected_variable
        ):
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
