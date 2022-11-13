import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from dash_bootstrap_templates import ThemeSwitchAIO
from pages.default_fig import default_fig

from datetime import datetime as dt
import glob
import pandas as pd
from sklearn.preprocessing import LabelEncoder
class_le = LabelEncoder()

from dataset import generate_device_change_table, generate_usage_count_table, date_list, dataset_list

template_theme2 = "flatly"
template_theme1 = "darkly"

dash.register_page(__name__)


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Dataset"),
            dcc.Dropdown(
                id="dataset-select",
                options=[{"label": i, "value": i} for i in dataset_list],
                value=dataset_list[0],
            ),
            html.Br(),
            html.P("Select Usage Range"),
            dcc.RangeSlider(
                id="usage-range-select",
                min=0,
                max=len(date_list)-1,
                step=None,
                marks={i: date_list[i] for i in range(len(date_list))},
                value=[0, len(date_list)-1]
            ),
            html.Br(),
            html.P("Select Device Range"),
            dcc.RangeSlider(
                id="date-range-select",
                min=0,
                max=len(date_list)-1,
                step=None,
                marks={i: date_list[i] for i in range(len(date_list))},
                value=[0, len(date_list)-1]
            ),
            html.Br(),
            html.Div(
                id="reset-btn-outer",
                children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
            ),
        ],
    )


layout = dbc.Container(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    id="left-column",
                    width=4,
                    children=[
                        generate_control_card()
                    ]
                ),
                dbc.Col(
                    id="right-column",
                    width=8,
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    width=8,
                                    children=[
                                        dcc.Graph(
                                            id="reten_rate-graph", 
                                            figure=default_fig
                                        )
                                    ],
                                ),
                                dbc.Col(
                                    width=4,
                                    children=[
                                        dcc.Graph(
                                            id="device_change-graph", 
                                            figure=default_fig
                                        )
                                    ]
                                )    
                            ]
                        ),
                        dcc.Graph(id="drop_reten-graph", figure=default_fig)
                    ]
                )
            ]        
        )
    ],
    fluid=True
) 


@callback(
    Output("device_change-graph", "figure"),
    Input("date-range-select", "value"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
)
def update_device_change_pie(selected_date, toggle):
    template = template_theme1 if toggle else template_theme2
    df_device_change = generate_device_change_table(date_list[selected_date[0]], date_list[selected_date[1]])
    vc = df_device_change['drop_reten'].value_counts().reset_index()
    fig = px.pie(
        vc, 
        values='drop_reten',
        names='index',
        template=template
    )
    return fig


@callback(
    Output("drop_reten-graph", "figure"),
    Input("date-range-select", "value"),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
)
def update_drop_reten_sankey(selected_date, toggle):
    template = template_theme1 if toggle else template_theme2
    date1 = date_list[selected_date[0]]
    date2 = date_list[selected_date[1]]
    df_device_change = generate_device_change_table(date1, date2)
    df_device_change = df_device_change[df_device_change['drop_reten'].isin(['リテンション', '離脱'])]
    df_device_change['drop_reten'] = class_le.fit_transform(df_device_change['drop_reten'])
    return px.parallel_categories(
        df_device_change,
        dimensions=[date1, date2],
        color='drop_reten',
        template=template
    )