import dash
import pandas as pd
import plotly.express as px

from dash import dcc, html
from dash.dependencies import Input, Output

df = pd.read_csv('C:/Users/Mark/CodersLab-Course-Python-Data-Analysis/Projekt vizualizace/project_1_python.csv')

df["date"] = pd.to_datetime(df["date"])
df.dtypes



app = dash.Dash()


app.layout = html.Div([
        html.H1('COVID-19 data',
        style={'text-align':'center'}),

        html.Div([
            html.Label("Choose country:", style={"fontWeight": "bold"}),
            dcc.Dropdown(
                id='input-1',
                options=[{'label': country, 'value': country} for country in sorted(df['location'].unique())],
                value=['Czechia'],
                multi=True,
                placeholder='Choose country'
            )
        ], style={'width': '60%', 'margin': 'auto'}),

        html.Div([
            dcc.Graph(id='graph-1', style={"width": "50%"}),
            dcc.Graph(id='graph-2', style={"width": "50%"})
        ], style={"display": "flex"})

])



@app.callback(
    [Output(component_id='graph-1', component_property='figure'),
     Output(component_id='graph-2', component_property='figure')],
    Input(component_id='input-1', component_property='value')
)
def update_graphs(selected_countries):
    if not selected_countries:
        return dash.no_update, dash.no_update

    filtered = df[df['location'].isin(selected_countries)]

    fig_cases = px.line(
        filtered,
        x='date',
        y='total_cases',
        color='location',
        title=f'📈 Number of COVID-19 cases over time in {', '.join(selected_countries)}',
        labels={'total_cases': 'Number of COVID-19 cases', 'location': 'Country', 'date': 'Date'}
    )

    fig_deaths = px.line(
        filtered,
        x='date',
        y='total_deaths',
        color='location',
        title=f'☠️ Number of COVID-19 deaths over time in {', '.join(selected_countries)}',
        labels={'total_deaths': 'Number of COVID-19 deaths', 'location': 'Country', 'date': 'Date'}
    )

    return fig_cases, fig_deaths



if __name__ == "__main__":
    app.run_server(debug=True)