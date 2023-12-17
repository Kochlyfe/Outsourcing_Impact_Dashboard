from dash import html, dcc


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
