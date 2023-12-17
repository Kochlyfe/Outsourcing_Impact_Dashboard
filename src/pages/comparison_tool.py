from dash import html, dcc


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
