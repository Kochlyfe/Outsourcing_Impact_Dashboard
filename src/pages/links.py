from dash import html, dcc


def render_page(tab_style, tab_selected_style, tabs_styles):
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
