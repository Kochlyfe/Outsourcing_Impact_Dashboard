from dash import html, dcc


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
