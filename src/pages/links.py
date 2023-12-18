from dash import html, dcc, Output, Input


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


def register_callbacks(app):
    @app.callback(
        Output("page-4-tabs-content", "children"), [Input("page-4-tabs", "value")]
    )
    def render_page_4_content(tab):
        if tab == "tab-10":
            return html.Div(
                [
                    html.H1("Data Downloads:"),
                    html.H3("Our cleaned data is available here:"),
                    html.Ul(
                        [
                            html.Li(
                                html.A(
                                    "All data for LAs (large file warning)",
                                    href="https://raw.githubusercontent.com/BenGoodair/childrens_social_care_data/main/Final_Data/outputs/dashboard_data.csv",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "All data for providers",
                                    href="https://raw.githubusercontent.com/BenGoodair/childrens_social_care_data/main/Final_Data/outputs/Provider_data.csv",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "Full coding library for how data was produced",
                                    href="https://github.com/BenGoodair/childrens_social_care_data/tree/main",
                                )
                            ),
                        ]
                    ),
                    html.H3("Original data is available at these locations:"),
                    html.Ul(
                        [
                            html.Li(
                                html.A(
                                    "Outcomes for children in care",
                                    href="https://www.gov.uk/government/statistics/outcomes-for-children-in-need-including-children-looked-after-by-local-authorities-in-england-2021-to-2022",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "Placements for children in care",
                                    href="https://www.gov.uk/government/statistics/children-looked-after-in-england-including-adoption-2021-to-2022",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "Expenditure on children in care",
                                    href="https://explore-education-statistics.service.gov.uk/find-statistics/la-and-school-expenditure/2021-22",
                                )
                            ),
                        ]
                    ),
                ]
            )
        elif tab == "tab-11":
            return html.Div(
                [
                    html.H1("Links to Resources"),
                    html.H3("Research from our team"),
                    html.H6("Research on outsourcing of children's social care"),
                    html.Ul(
                        [
                            html.Li(
                                html.A(
                                    "Do for-profit childrens homes outperform council-run homes?",
                                    href="https://www.sciencedirect.com/science/article/pii/S0277953622006293",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "Does outsourcing correspond with better or worse quality placements for children?",
                                    href="https://www.sciencedirect.com/science/article/pii/S0277953622006293",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "Why do Local Authorities outsource services?",
                                    href="https://www.sciencedirect.com/science/article/pii/S0277953621001763",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "Do Local Authorities achieve market stewardship?",
                                    href="https://ora.ox.ac.uk/objects/uuid:4465898b-0b98-4c08-aa84-feb89aa54280/files/sqz20st49v",
                                )
                            ),
                        ]
                    ),
                    html.H6("Research on outsourcing of adult's social care"),
                    html.Ul(
                        [
                            html.Li(
                                html.A(
                                    "Did for-profit nursing homes perform well during COVID-19 outbreaks?",
                                    href="https://pubmed.ncbi.nlm.nih.gov/37118328/",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "What are the issues with ownership in the adult social care sector?",
                                    href="https://www.thelancet.com/journals/lanhl/article/PIIS2666-7568(22)00040-X/fulltext?msclkid=014e07e2ab8211ec8",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "Do for-profit care homes outperform others in Scotland?",
                                    href="https://bmjopen.bmj.com/content/9/2/e022975",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "Do for-profit care homes break fewer regulations than others in Scotland?",
                                    href="https://journals.sagepub.com/doi/full/10.1177/08997640211001448",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "What happens when investment firms take over care homes?",
                                    href="https://s3.eu-central-1.amazonaws.com/eu-st01.ext.exlibrisgroup.com/44SUR_INST/storage/alma/1C/69/8B/17/1D/46/D6/A0/69/BD/51/B8/09/AD/93/D6/UNISON-CUSP%20report%20%28final%29.pdf?response-content-type=application%2Fpdf&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231108T143557Z&X-Amz-SignedHeaders=host&X-Amz-Expires=119&X-Amz-Credential=AKIAJN6NPMNGJALPPWAQ%2F20231108%2Feu-central-1%2Fs3%2Faws4_request&X-Amz-Signature=dd661f07699e6063a691afea28b63c2c29fd15e66caaf7875a65b59c11d91e60",
                                )
                            ),
                        ]
                    ),
                    html.H6("Research on outsourcing of healthcare"),
                    html.Li(
                        html.A(
                            "What is the impact of outsourcing healthcare services on quality of care?",
                            href="https://www.thelancet.com/journals/lanpub/article/PIIS2468-2667(22)00133-5/fulltext?trk=organization_guest_main-feed-card_feed-article-content",
                        )
                    ),
                    html.Li(
                        html.A(
                            "Why do NHS commissioners outsource healthcare services?",
                            href="https://www.sciencedirect.com/science/article/pii/S0168851023002269?via%3Dihub",
                        )
                    ),
                    html.H3("Project Information"),
                    html.Ul(
                        [
                            html.Li(
                                html.A(
                                    "We are incredibly grateful for the support of Nuffield Foundation for funding this project, you can view our project homepage here:",
                                    href="https://www.nuffieldfoundation.org/project/evidencing-the-outsourcing-of-social-care-provision-in-england",
                                )
                            ),
                            html.Li(
                                html.A(
                                    "The project has been funded by the Nuffield Foundation, but the view expressed are those of the authors and not necessarily the Foundation. Visit: www.nuffieldfoundation.org",
                                    href="https://www.nuffieldfoundation.org",
                                )
                            ),
                        ]
                    ),
                ]
            )
        elif tab == "tab-12":
            return html.Div(
                [
                    html.H3("Meet the team:"),
                    html.Ul(
                        [
                            html.Li(
                                [
                                    html.Img(
                                        src="https://github.com/BenGoodair/Outsourcing_Impact_Dashboard/blob/main/Images/anders_bach-mortensen.jpg?raw=true",
                                        style={"width": "100px", "height": "100px"},
                                    ),
                                    html.Div(
                                        [
                                            html.H4("Anders"),
                                            html.P(
                                                "Anders is a social scientist with expertise on outsourcing, social care services and systematic review methods."
                                            ),
                                            html.P(
                                                "Anders was national champion fencer in his youth - he now uses skills of precision in interpretting complex statistical models."
                                            ),
                                        ],
                                        style={
                                            "display": "inline-block",
                                            "vertical-align": "top",
                                        },
                                    ),
                                ]
                            ),
                            html.Li(
                                [
                                    html.Img(
                                        src="https://github.com/BenGoodair/Outsourcing_Impact_Dashboard/blob/main/Images/Michelle.jpg?raw=true",
                                        style={"width": "100px", "height": "100px"},
                                    ),
                                    html.Div(
                                        [
                                            html.H4("Michelle"),
                                            html.P(
                                                "Michelle is a Research Assistant Professor with the U-M Institute for Firearm Injury Prevention."
                                            ),
                                            html.P(
                                                "Michelle's favourite colour is the same as Hilary Clinton's"
                                            ),
                                        ],
                                        style={
                                            "display": "inline-block",
                                            "vertical-align": "top",
                                        },
                                    ),
                                ]
                            ),
                            html.Li(
                                [
                                    html.Img(
                                        src="https://github.com/BenGoodair/Outsourcing_Impact_Dashboard/blob/main/Images/christine.jpg?raw=true",
                                        style={"width": "100px", "height": "100px"},
                                    ),
                                    html.Div(
                                        [
                                            html.H4("Christine"),
                                            html.P(
                                                "Christine is a political economist who specialises in postgrowth economics and the privatisation of social care."
                                            ),
                                            html.P(
                                                "Christine once told Emma Watson that her shoelaces were undone."
                                            ),
                                        ],
                                        style={
                                            "display": "inline-block",
                                            "vertical-align": "top",
                                        },
                                    ),
                                ]
                            ),
                            html.Li(
                                [
                                    html.Img(
                                        src="https://github.com/BenGoodair/Methane_Dashboard/blob/main/ben.jpg?raw=true",
                                        style={"width": "100px", "height": "100px"},
                                    ),
                                    html.Div(
                                        [
                                            html.H4("Ben"),
                                            html.P(
                                                "Ben is a social researcher identifying the impacts of privatization on health and social care systems."
                                            ),
                                            html.P(
                                                "Ben will embroider any form of data visualisation he thinks worthy of the thread."
                                            ),
                                        ],
                                        style={
                                            "display": "inline-block",
                                            "vertical-align": "top",
                                        },
                                    ),
                                ]
                            ),
                            html.Li(
                                [
                                    html.Img(
                                        src="https://github.com/BenGoodair/Outsourcing_Impact_Dashboard/blob/main/Images/jane.png?raw=true",
                                        style={"width": "100px", "height": "100px"},
                                    ),
                                    html.Div(
                                        [
                                            html.H4("Jane"),
                                            html.P(
                                                "Jane is Professor of Evidence Based Intervention and Policy Evaluation at the Department of Social Policy and Intervention, University of Oxford."
                                            ),
                                            html.P(
                                                "Jane once owned a stick insect call Stephen."
                                            ),
                                        ],
                                        style={
                                            "display": "inline-block",
                                            "vertical-align": "top",
                                        },
                                    ),
                                ]
                            ),
                        ]
                    ),
                    html.H3("Partner with us:"),
                    html.H6("Join our team to continue this work"),
                    html.P(
                        "We are looking for partners with policy, industrial or lived experiences to join our happy community!"
                    ),
                    html.Ul(
                        [
                            html.Li(
                                "We can write a funding application to ensure labor compensated and valued."
                            ),
                            html.Li(
                                "We want new directions and ideas, bring your creativity!"
                            ),
                            html.Li(
                                "We want to have fun and work in a respectful, supportive, and positive way."
                            ),
                        ]
                    ),
                    html.H3("Contact and feedback"),
                    html.H6("Help us improve this dashboard for your needs!"),
                    html.P(
                        "All our work is completely open access and reproducible, we'd love to work with you to apply this work to other data"
                    ),
                    html.Ul(
                        [
                            html.Li("Email us at: benjamin.goodair@spi.ox.ac.uk"),
                            html.Li("Tweet us at: @BenGoodair"),
                            html.Li("Find us at: DSPI, Oxford, United Kingdom"),
                        ]
                    ),
                ]
            )
