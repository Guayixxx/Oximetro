from dash import dcc, html, Input, Output
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go

# Configuración del archivo CSV
CSV_FILE = "/home/juan-pablo/Documentos/BioIng/Oximetro/data.csv"

# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout del dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Health Dashboard", className="text-center")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="spo2-graph")
        ], width=6),
        dbc.Col([
            dcc.Graph(id="hr-graph")
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.H4("Histórico de Datos", className="text-center"),
            dbc.Table(id="data-table", bordered=True, striped=True, hover=True, responsive=True)
        ], width=12)
    ]),
    dcc.Interval(
        id="interval-component",
        interval=1000,  # Actualización cada 1000 ms (1 segundo)
        n_intervals=0
    )
], fluid=True)

# Callbacks para actualizar gráficos y tabla
@app.callback(
    [Output("spo2-graph", "figure"),
     Output("hr-graph", "figure"),
     Output("data-table", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_dashboard(n):
    # Leer datos del archivo CSV
    try:
        df = pd.read_csv(CSV_FILE)
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return go.Figure(), go.Figure(), []

    # Crear gráficos
    spo2_fig = go.Figure()
    spo2_fig.add_trace(go.Scatter(x=df["Timestamp"], y=df["SpO2"], mode="lines+markers", name="SpO₂"))
    spo2_fig.update_layout(title="SpO₂ (%)", xaxis_title="Time", yaxis_title="SpO₂ (%)")

    hr_fig = go.Figure()
    hr_fig.add_trace(go.Scatter(x=df["Timestamp"], y=df["HeartRate"], mode="lines+markers", name="Heart Rate"))
    hr_fig.update_layout(title="Heart Rate (BPM)", xaxis_title="Time", yaxis_title="BPM")

    # Crear tabla
    table_header = [html.Thead(html.Tr([html.Th("Timestamp"), html.Th("SpO₂"), html.Th("Heart Rate")]))]
    table_body = [html.Tbody([html.Tr([html.Td(row["Timestamp"]), html.Td(row["SpO2"]), html.Td(row["HeartRate"])]) for _, row in df.iterrows()])]
    table = table_header + table_body

    return spo2_fig, hr_fig, table

# Ejecutar la aplicación Dash
if __name__ == "__main__":
    app.run_server(debug=True)
