import dash
import pandas as pd
import plotly.express as px

from dash import dcc, html
from dash.dependencies import Input, Output

df = pd.read_csv('C:/Users/Mark/CodersLab-Course-Python-Data-Analysis/Projekt vizualizace/project_1_python.csv')

df["date"] = pd.to_datetime(df["date"])
df_final = df.loc[df.groupby("location")["date"].idxmax()]
df_final['ratio'] = df_final['total_cases'] / df_final['population']
df_final = df_final.dropna(subset=['ratio'])
df_final['ratio'] = df_final['ratio'].fillna(0)

labels = {
    'continent': 'Continent',
    'total_vaccinations': 'Total number of vaccinations',
    'location': 'Location',
    'total_cases': 'Total number of positive cases',
    'total_deaths': 'Total number of deaths',
    'total_tests': 'Total number of tests',
    'people_fully_vaccinated': 'Total number of vaccinated people'
}


available_metrics = {'total_cases' : 'Total number of positive cases',
                     'total_deaths' : 'Total number of deaths',
                     'total_vaccinations' : 'Total number of vaccinations',
                     'total_tests' : 'Total number of tests',
                     'people_fully_vaccinated' : 'Total number of vaccinated people'}
available_continents = sorted(df_final['continent'].dropna().unique())

app = dash.Dash()


app.layout = html.Div([
    html.H1('COVID-19 Global map', style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Continent:", style={"fontWeight": "bold", "marginRight": "10px"}),
        dcc.Dropdown(
            id='continent-dropdown',
            options=[{'label': c, 'value': c} for c in available_continents],
            value='Europe',
            clearable=False,
            style={'width': '200px'}
        ),

        html.Label("Select Metric:", style={"fontWeight": "bold", "marginLeft": "40px", "marginRight": "10px"}),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[{'label': labels[m], 'value': m} for m in available_metrics],
            value='total_cases',
            clearable=False,
            style={'width': '200px'}
        )
    ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'margin': '20px', 'flexWrap': 'wrap'}),

    html.Div([
        dcc.Graph(id='map-graph', style={'width': '90%', 'height': '800px'})
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'marginBottom': '40px'
    })
])



@app.callback(
    Output(component_id='map-graph', component_property='figure'),
    Input(component_id='continent-dropdown', component_property='value'),
    Input(component_id='metric-dropdown', component_property='value')
)
def update_map(selected_continent, selected_metric):

    filtered = df_final[df_final['continent'] == selected_continent]
    filtered = filtered.dropna(subset=[selected_metric])

    if filtered.empty:
        fig = px.scatter_geo()
        fig.update_layout(
            title=f"No data available for {labels[selected_metric]} in {selected_continent}",
            template="ggplot2",
            geo=dict(
                showland=True,
                landcolor="LightGray"
            )
        )
        return fig

    fig = px.scatter_geo(
        filtered,
        locations="location",
        locationmode="country names",
        color="continent",
        size=selected_metric,
        hover_name="location",
        hover_data={selected_metric: True},
        title=f"Covid 19 - {available_metrics[selected_metric]} in {selected_continent}",
        projection="natural earth",
        template="ggplot2",
        height=800,
        width=1400,
        labels={'continent' : 'Continent',
                'total_vaccinations' : 'Total number of vaccinations',
                'location' : 'Location',
                'total_cases' : 'Total number of positive cases',
                'total_deaths' : 'Total number of deaths',
                'total_tests' : 'Total number of tests',
                'people_fully_vaccinated' : 'Total number of vaccinated people'}
    )



    return fig



if __name__ == "__main__":
    app.run_server(debug=True)
