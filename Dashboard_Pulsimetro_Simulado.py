import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import random
import threading
import time

# Almacenamiento de datos
data = {"Timestamp": [], "SpO2": [], "HeartRate": []}

# Variable para control de ejecución
running = True

# Generar datos ficticios
def generate_fake_data():
    while running:
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            spo2 = random.randint(90, 100)  # Simulación de SpO₂
            heart_rate = random.randint(60, 100)  # Simulación de frecuencia cardíaca
            data["Timestamp"].append(timestamp)
            data["SpO2"].append(spo2)
            data["HeartRate"].append(heart_rate)
            # Limitar el tamaño del historial
            if len(data["Timestamp"]) > 100:
                for key in data:
                    data[key] = data[key][-100:]
            time.sleep(1)  # Simular una lectura por segundo
        except Exception as e:
            print("Error:", e)

# Hilo para generar datos en segundo plano
thread = threading.Thread(target=generate_fake_data)
thread.daemon = True
thread.start()

# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout del dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Health Dashboard (Simulado)", className="text-center")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src="https://via.placeholder.com/100x100?text=O2", style={"width": "80px"}),
                html.H3("SpO₂ (%)", className="text-center"),
                html.H4(id="spo2-value", className="text-center")
            ], className="border p-3 text-center")
        ], width=6),
        dbc.Col([
            html.Div([
                html.Img(src="https://via.placeholder.com/100x100?text=HR", style={"width": "80px"}),
                html.H3("Heart Rate (BPM)", className="text-center"),
                html.H4(id="hr-value", className="text-center")
            ], className="border p-3 text-center")
        ], width=6)
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
    # Componente para actualización automática
    dcc.Interval(
        id="interval-component",
        interval=1000,  # Actualización cada 1000 ms (1 segundo)
        n_intervals=0  # Cuenta el número de intervalos (inicia en 0)
    )
], fluid=True)

# Callbacks para actualizar gráficos, tabla e indicadores
@app.callback(
    [Output("spo2-graph", "figure"),
     Output("hr-graph", "figure"),
     Output("spo2-value", "children"),
     Output("hr-value", "children"),
     Output("data-table", "children")],
    [Input("interval-component", "n_intervals")]  # Disparador automático
)
def update_dashboard(_):
    df = pd.DataFrame(data)
    if df.empty:
        return go.Figure(), go.Figure(), "-", "-", []

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

    # Indicadores
    current_spo2 = df["SpO2"].iloc[-1]
    current_hr = df["HeartRate"].iloc[-1]

    return spo2_fig, hr_fig, f"{current_spo2}%", f"{current_hr} BPM", table

# Ejecutar la aplicación
if __name__ == "__main__":
    try:
        app.run_server(debug=True)
    finally:
        # Asegurar que el hilo se detenga
        running = False
        thread.join()