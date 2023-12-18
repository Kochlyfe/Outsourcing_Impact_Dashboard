from dash import html, dcc, Output, Input

import dash_bootstrap_components as dbc
import dash

from pages import welcome
import pages.outsourcing_levels as ol
import pages.quality_impacts as qi
import pages.comparison_tool as ct
import pages.links as l
from datasets import DataContainer

### Init datasets
data_container = DataContainer.load_data()
dataframes_tuple = data_container.get_dataframes_as_namedtuple()

(
    la_df,
    nobs_final,
    exitdata,
    merged2,
    active_chomes,
    outcomes_df,
    placements_df,
    expenditures_df,
) = dataframes_tuple

####Dashboard####
app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
ol.register_callbacks(app, data_container)
qi.register_callbacks(app, data_container)
ct.register_callbacks(app, data_container)
l.register_callbacks(app)

server = app.server

tabs_styles = {"height": "44px"}
tab_style = {
    "borderBottom": "1px solid #d6d6d6",
    "padding": "6px",
    "fontWeight": "bold",
}

tab_selected_style = {
    "borderTop": "1px solid #d6d6d6",
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "#119DFF",
    "color": "white",
    "padding": "6px",
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "transform": "scale(0.67)",  # Adjust the scale factor as needed
    "transform-origin": "top left",
    "height": "150%",  # Approximately compensating for 33% scale-down
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "11rem",
    "margin-right": "16rem",
    "transform": "scale(0.67)",  # Adjust the scale factor as needed
    "transform-origin": "top left",
    "padding": "2rem 1rem",
    "width": "125%",  # Approximately compensating for 33% scale-down
    "height": "150%",  # Approximately compensating for 33% scale-down
}

sidebar = html.Div(
    [
        html.H2("Outsourcing Impacts Tracker", className="display-7"),
        html.Hr(),
        html.P(
            "Welcome to a dashboard detailing the impacts of outsourcing in England's children social care sector.",
            className="lead",
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Outsourcing levels", href="/page-1", active="exact"),
                dbc.NavLink("Quality Impacts", href="/page-2", active="exact"),
                dbc.NavLink("Comparison tool", href="/page-3", active="exact"),
                dbc.NavLink("Links To Resources", href="/page-4", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)


watermark = html.Div(
    "Under-development; Not for dissemination",
    style={
        "position": "fixed",
        "bottom": "50%",  # Adjust the vertical position
        "right": "50%",  # Adjust the horizontal position
        "transform": "translate(50%, 50%) rotate(-45deg)",  # Rotate and position
        "color": "rgba(255, 0, 0, 0.4)",
        "fontSize": "70px",  # Increase the font size for better visibility
        "zIndex": "9999",
    },
)


# Incorporate the watermark into your layout
app.layout = html.Div([dcc.Location(id="url"), sidebar, content, watermark])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    path_mapping = {
        "/": welcome.render_page,
        "/page-1": lambda: ol.render_page(tab_style, tab_selected_style, tabs_styles),
        "/page-2": lambda: qi.render_page(tab_style, tab_selected_style, tabs_styles),
        "/page-3": lambda: ct.render_page(tab_style, tab_selected_style, tabs_styles),
        "/page-4": lambda: l.render_page(tab_style, tab_selected_style, tabs_styles),
    }

    render_page = path_mapping.get(pathname)

    if render_page is not None:
        return render_page()

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(debug=True)
