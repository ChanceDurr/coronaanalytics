import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


data = pd.read_csv("C:/Users/Chance/Desktop/corona/covid_19_data.csv")
data = data.rename({"Country/Region": "Country", "Province/State": "State"}, axis=1)
data["ObservationDate"] = pd.to_datetime(data["ObservationDate"])
data.sort_values("ObservationDate", inplace=True)

ext_style = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    {
        "href": "assets\style.css",
        "rel": "stylesheet"
    }
]

app = dash.Dash(__name__, external_stylesheets=ext_style)

app.title = "Corona Virus Cases"

state_options = [
    {'label': 'Alaska', 'value': 'Alaska'},
    {'label': 'Alabama', 'value': 'Alabama'},
    {'label': 'Arkansas', 'value': 'Arkansas'},
    {'label': 'Arizona', 'value': 'Arizona'},
    {'label': 'California', 'value': 'California'},
    {'label': 'Colorado', 'value': 'Colorado'},
    {'label': 'Connecticut', 'value': 'Connecticut'},
    {'label': 'Delaware', 'value': 'Delaware'},
    {'label': 'Florida', 'value': 'Florida'},
    {'label': 'Georgia', 'value': 'Georgia'},
    {'label': 'Hawaii', 'value': 'Hawaii'},
    {'label': 'Iowa', 'value': 'Iowa'},
    {'label': 'Idaho', 'value': 'Idaho'},
    {'label': 'Illinois', 'value': 'Illinois'},
    {'label': 'Indiana', 'value': 'Indiana'},
    {'label': 'Kansas', 'value': 'Kansas'},
    {'label': 'Kentucky', 'value': 'Kentucky'},
    {'label': 'Louisiana', 'value': 'Louisiana'},
    {'label': 'Massachusetts', 'value': 'Massachusetts'},
    {'label': 'Maryland', 'value': 'Maryland'},
    {'label': 'Maine', 'value': 'Maine'},
    {'label': 'Michigan', 'value': 'Michigan'},
    {'label': 'Minnesota', 'value': 'Minnesota'},
    {'label': 'Missouri', 'value': 'Missouri'},
    {'label': 'Mississippi', 'value': 'Mississippi'},
    {'label': 'Montana', 'value': 'Montana'},
    {'label': 'North Carolina', 'value': 'North Carolina'},
    {'label': 'North Dakota', 'value': 'North Dakota'},
    {'label': 'Nebraska', 'value': 'Nebraska'},
    {'label': 'New Hampshire', 'value': 'New Hampshire'},
    {'label': 'New Jersey', 'value': 'New Jersey'},
    {'label': 'New Mexico', 'value': 'New Mexico'},
    {'label': 'Nevada', 'value': 'Nevada'},
    {'label': 'New York', 'value': 'New York'},
    {'label': 'Ohio', 'value': 'Ohio'},
    {'label': 'Oklahoma', 'value': 'Oklahoma'},
    {'label': 'Oregon', 'value': 'Oregon'},
    {'label': 'Pennsylvania', 'value': 'Pennsylvania'},
    {'label': 'Rhode Island', 'value': 'Rhode Island'},
    {'label': 'South Carolina', 'value': 'South Carolina'},
    {'label': 'South Dakota', 'value': 'South Dakota'},
    {'label': 'Tennessee', 'value': 'Tennessee'},
    {'label': 'Texas', 'value': 'Texas'},
    {'label': 'Utah', 'value': 'Utah'},
    {'label': 'Virginia', 'value': 'Virginia'},
    {'label': 'Vermont', 'value': 'Vermont'},
    {'label': 'Washington', 'value': 'Washington'},
    {'label': 'Wisconsin', 'value': 'Wisconsin'},
    {'label': 'West Virginia', 'value': 'West Virginia'},
    {'label': 'Wyoming', 'value': 'Wyoming'}
]

app.layout = html.Div(
    children=[
        # Header
        html.Div(
            children=[
                html.P(children="😷", className="header-emoji"),
                html.H1(
                    children="Corona Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of Corona Cases in CA"
                    " and the number of cases in the US"
                    " between 2020 and 2021",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        # Graph content
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            dcc.Dropdown(
                                options = state_options,
                                value="California",
                                multi=False,
                                id="state_dropdown_choice"
                            ),
                            className="card"
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            
                            dcc.Graph(
                                id = "confirmed_graph",
                            ),
                            className="card"
                        ),
                        html.Div(
                            dcc.Graph(
                                id = "deaths_graph",
                            ),
                            className="card"
                        )
                    ],
                    className="graph-wrapper"
                ),
                # Pie charts for state total confirmed and deaths vs US as a whole
                html.Div(
                    children = [
                        html.Div(
                            dcc.Graph(
                                id="pie_chart_confirmed",
                            ),
                            className="card"
                        ),
                        html.Div(
                            dcc.Graph(
                                id="pie_chart_deaths",
                            ),
                            className="card"
                        ),
                    ],
                    className="pie-wrapper"
                )
            ],
            className="main-wrapper"
        )
    ],
    
)

# Change the confirmed cases graph when changing the state
@app.callback(
    Output(component_id="confirmed_graph", component_property="figure"),
    Input(component_id="state_dropdown_choice", component_property="value")
)
def update_confirmed(state_value):
    graph_data = data.query(f" Country == 'US' and State == '{state_value}'")


    return {
        "data": [
            {
                "x": graph_data["ObservationDate"],
                "y": graph_data["Confirmed"],
                "type": "line",
            },
        ],
        "layout": {
            "title": f"Confirmed Cases in {state_value}",
            "colorway": ["#E12D39"],
            "hline": {"x": "2020-12-25T00:00:00", "line_width": 3}
            },
        
    }

# Change the deaths graph when changing the state
@app.callback(
    Output(component_id="deaths_graph", component_property="figure"),
    Input(component_id="state_dropdown_choice", component_property="value")
)
def update_deaths(state_value):
    graph_data = data.query(f" Country == 'US' and State == '{state_value}'")


    return {
        "data": [
            {
                "x": graph_data["ObservationDate"],
                "y": graph_data["Deaths"],
                "type": "line",
            },
        ],
        "layout": {
            "title": f"Corona Deaths in {state_value}",
            "colorway": ["#E12D39"]
            },
    }
    
# Change the confirmed total pie chart for the selected state
@app.callback(
    Output(component_id="pie_chart_confirmed", component_property="figure"),
    Input(component_id="state_dropdown_choice", component_property="value")
)
def update_pie_confirmed(state_value):
    # Get the most recent date in case this csv is updated
    latest_date = str(data.ObservationDate.max()).split()[0]

    # Grab the total confirmed and deaths
    us_data = data.query(f" Country == 'US' and ObservationDate == '{latest_date}'")

    # Just do the 50 states
    exclude = [
           "Recovered",
           "Diamond Princess cruise ship",
           "Grand Princess", "Guam",
           "Northern Mariana Islands",
           "Virgin Islands", "Puerto Rico",
           "District of Columbia"
    ]

    us_data = us_data[~us_data["State"].isin(exclude)]

    # Get the total of the confirmed cases
    total_confirmed = us_data.Confirmed.sum()

    # Get the total confirmed for the last day for the selected state
    state_confirmed_total = us_data.query(f" State == '{state_value}' ").Confirmed.values[0]

    # Create a quick df for the plotly express pie figure
    d = {"names": [state_value, "US Total"], "values": [state_confirmed_total, total_confirmed]}
    df = pd.DataFrame(data=d)

    # Create the figure for the pie chart
    fig = px.pie(df, values="values", names="names", title=f"Confirmed Cases:<br>{state_value} vs. USA")

    # Return the fig to the dcc.graph
    return fig


# Change the death total pie chart for the selected state
@app.callback(
    Output(component_id="pie_chart_deaths", component_property="figure"),
    Input(component_id="state_dropdown_choice", component_property="value")
)
def update_pie_confirmed(state_value):
    # Get the most recent date in case this csv is updated
    latest_date = str(data.ObservationDate.max()).split()[0]

    # Grab the total confirmed and deaths
    us_data = data.query(f" Country == 'US' and ObservationDate == '{latest_date}'")

    # Just do the 50 states
    exclude = [
           "Recovered",
           "Diamond Princess cruise ship",
           "Grand Princess", "Guam",
           "Northern Mariana Islands",
           "Virgin Islands", "Puerto Rico",
           "District of Columbia"
    ]

    us_data = us_data[~us_data["State"].isin(exclude)]

    # Get the total of the confirmed cases
    total_deaths = us_data.Deaths.sum()

    # Get the total confirmed for the last day for the selected state
    state_deaths_total = us_data.query(f" State == '{state_value}' ").Deaths.values[0]

    # Create a quick df for the plotly express pie figure
    d = {"names": [state_value, "US Total"], "values": [state_deaths_total, total_deaths]}
    df = pd.DataFrame(data=d)

    # Create the figure for the pie chart
    fig = px.pie(df, values="values", names="names", title=f"Corona Virus Deaths:<br>{state_value} vs. USA")

    # Return the fig to the dcc.graph
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)