# LIBRERIAS
import dash
from dash import Dash, dcc, html
import plotly.express as px
from base64 import b64encode
import io
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd

# creacion de la app
app = dash.Dash()
server = app.server
# carga de datos
df = pd.read_csv("Geo1.csv")
df.head()

# MAPA

mapbox_access_token = 'pk.eyJ1Ijoia2FyaW5haHYiLCJhIjoiY2w4aTg3MTFiMTB2YjNvbGxkZXhzNXdjayJ9.n0w3xjXITgv6gKqxWBc9Nw'
fig_mapa = go.Figure(go.Scattermapbox(
    lon=df['LONGITUD'],
    lat=df['LATITUD'],
    mode='markers',
    text=df['ID_SUCURSAL'],
    marker=go.scattermapbox.Marker(
        size=df['ID_SUCURSAL'] / 50000,
        color=df['ID_SUCURSAL'] / 50000
    )
))

fig_mapa.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=17.542336,
            lon=-99.502249
        ),
        pitch=0,
        zoom=2
    ),
)

# CREACION DE GRAFICOS
# buscador


app.layout = html.Div([
    html.Div([
        html.Label('Estado'),
        dcc.Dropdown(id='Buscador',
                     options=[{'label': i, 'value': i} for i in df['ESTADO'].unique()],
                     )], style={'width': '100%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='barplot_ventas_seg')
    ], style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='barplot_beneficio_cat')
    ], style={'width': '33%', 'float': 'center', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='mapa_ventas', figure=fig_mapa)
    ], style={'width': '100%'})

])


@app.callback(Output('barplot_ventas_seg', 'figure'),
              [Input('Buscador', 'value')])
def actualizar_graph_seg(seleccion):
    filtered_df = df[(df["ESTADO"] == seleccion)]

    df_agrupado = filtered_df.groupby("NOM_SUCURSAL")["NUM_OPERACIONES"].agg("sum").to_frame(
        name="Operaciones").reset_index()

    return {
        'data': [go.Bar(x=df_agrupado["NOM_SUCURSAL"],
                        y=df_agrupado["Operaciones"]
                        )],
        'layout': go.Layout(
            title="Numero de Operaciones por cada Sucursal",
            xaxis={'title': "NOM_SUCURSAL"},
            yaxis={'title': "Operaciones Totales"},
            hovermode='closest'

        )}


@app.callback(Output('barplot_beneficio_cat', 'figure'),
              [Input('Buscador', 'value')])
def actualizar_graph_cat(seleccion):
    filtered_df = df[(df["ESTADO"] == seleccion)]

    df_agrupado = filtered_df.groupby("SEGMENTO_CLIENTE")["NUM_CLIENTES_SANTANDER"].agg("sum").to_frame(
        name="Cliente").reset_index()

    return {
        'data': [go.Bar(x=df_agrupado["SEGMENTO_CLIENTE"],
                        y=df_agrupado["Cliente"]
                        )],
        'layout': go.Layout(
            title="Numero de clientes por segmento de cliente",
            xaxis={'title': "SEGMENTO_CLIENTE"},
            yaxis={'title': "numero de clientes"},
            hovermode='closest')}


if __name__ == '__main__':
    app.run_server(debug=True)

