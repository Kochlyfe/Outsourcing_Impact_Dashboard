from dash import html, dcc, Output, Input
from dash.exceptions import PreventUpdate

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
