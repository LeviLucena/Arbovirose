import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import random

# Importando o Bootstrap
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
                        'https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css']

# Geração de datas de janeiro de 2024 até a data atual
dates = pd.date_range(start='2024-01-01', end=pd.Timestamp.today(), freq='D')

# Geração de casos notificados aleatórios para cada data
notified_cases = [random.randint(5000, 10000) for _ in range(len(dates))]

# Geração de casos suspeitos aleatórios para cada data
suspected_cases = [random.randint(20, 5000) for _ in range(len(dates))]

# Geração de casos confirmados aleatórios para cada data
confirmed_cases = [random.randint(20, 5000) for _ in range(len(dates))]

# Geração de dados de distribuição de idade masculina
age_distribution_male = [random.randint(0, 90) for _ in range(1500)]

# Geração de dados de distribuição de idade feminina
age_distribution_female = [random.randint(0, 90) for _ in range(1000)]

# Geração de dados fictícios
municipios_sp = {
    "São Paulo": {
        "latitude": -23.5505,
        "longitude": -46.6333,
        "coordinates": [(-46.6333, -23.5505)]
    },
    "Guarulhos": {
        "latitude": -23.454,
        "longitude": -46.5333,
        "coordinates": [(-46.5333, -23.454)]
    },
    "Campinas": {
        "latitude": -22.9055,
        "longitude": -47.0608,
        "coordinates": [(-47.0608, -22.9055)]
    },
    "Santo André": {
        "latitude": -23.6734,
        "longitude": -46.5384,
        "coordinates": [(-46.5384, -23.6734)]
    },
    "São Bernardo do Campo": {
        "latitude": -23.6914,
        "longitude": -46.5364,
        "coordinates": [(-46.5364, -23.6914)]
    },
        "Osasco": {
        "latitude": -23.5329,
        "longitude": -46.7915,
        "coordinates": [(-46.7915, -23.5329)]
    },
    "Santo Amaro": {
        "latitude": -23.6459,
        "longitude": -46.6983,
        "coordinates": [(-46.6983, -23.6459)]
    },
    "São Caetano do Sul": {
        "latitude": -23.6229,
        "longitude": -46.5548,
        "coordinates": [(-46.5548, -23.6229)]
    },
    "São José dos Campos": {
        "latitude": -23.2237,
        "longitude": -45.9009,
        "coordinates": [(-45.9009, -23.2237)]
    },
    "Ribeirão Preto": {
        "latitude": -21.1699,
        "longitude": -47.8208,
        "coordinates": [(-47.8208, -21.1699)]
    },
    "Sorocaba": {
        "latitude": -23.5015,
        "longitude": -47.4587,
        "coordinates": [(-47.4587, -23.5015)]
    },
    "Mogi das Cruzes": {
        "latitude": -23.5225,
        "longitude": -46.1884,
        "coordinates": [(-46.1884, -23.5225)]
    },
    "Taboão da Serra": {
        "latitude": -23.6099,
        "longitude": -46.7833,
        "coordinates": [(-46.7833, -23.6099)]
    },
    "Jundiaí": {
        "latitude": -23.1857,
        "longitude": -46.8978,
        "coordinates": [(-46.8978, -23.1857)]
    },
    "Diadema": {
        "latitude": -23.6816,
        "longitude": -46.6205,
        "coordinates": [(-46.6205, -23.6816)]
    },
    "Piracicaba": {
        "latitude": -22.7242,
        "longitude": -47.6476,
        "coordinates": [(-47.6476, -22.7242)]
    },
    "Carapicuíba": {
        "latitude": -23.5235,
        "longitude": -46.8407,
        "coordinates": [(-46.8407, -23.5235)]
    },
    "Bauru": {
        "latitude": -22.3145,
        "longitude": -49.0609,
        "coordinates": [(-49.0609, -22.3145)]
    },
    "Itaquaquecetuba": {
        "latitude": -23.4868,
        "longitude": -46.3473,
        "coordinates": [(-46.3473, -23.4868)]
    },
    "Franca": {
        "latitude": -20.5352,
        "longitude": -47.4009,
        "coordinates": [(-47.4009, -20.5352)]
    },
    "Suzano": {
        "latitude": -23.5446,
        "longitude": -46.3117,
        "coordinates": [(-46.3117, -23.5446)]
    },
    "Ribeirão Pires": {
        "latitude": -23.7067,
        "longitude": -46.4116,
        "coordinates": [(-46.4116, -23.7067)]
    },
    "Barueri": {
        "latitude": -23.5107,
        "longitude": -46.8768,
        "coordinates": [(-46.8768, -23.5107)]
    },
    "Embu das Artes": {
        "latitude": -23.6486,
        "longitude": -46.8523,
        "coordinates": [(-46.8523, -23.6486)]
    },
    "São Vicente": {
        "latitude": -23.9574,
        "longitude": -46.3889,
        "coordinates": [(-46.3889, -23.9574)]
    },
    "São José do Rio Preto": {
        "latitude": -20.8114,
        "longitude": -49.3759,
        "coordinates": [(-49.3759, -20.8114)]
    },
    "Taubaté": {
        "latitude": -23.0264,
        "longitude": -45.5558,
        "coordinates": [(-45.5558, -23.0264)]
    },
    "Santos": {
        "latitude": -23.9535,
        "longitude": -46.333,
        "coordinates": [(-46.333, -23.9535)]
    },
    "Mauá": {
        "latitude": -23.6677,
        "longitude": -46.4613,
        "coordinates": [(-46.4613, -23.6677)]
    },
    "Praia Grande": {
        "latitude": -24.0058,
        "longitude": -46.4022,
        "coordinates": [(-46.4022, -24.0058)]
    },
    "São Carlos": {
        "latitude": -22.0174,
        "longitude": -47.8861,
        "coordinates": [(-47.8861, -22.0174)]
    },
    "Jacareí": {
        "latitude": -23.3052,
        "longitude": -45.9662,
        "coordinates": [(-45.9662, -23.3052)]
    },
    "Presidente Prudente": {
        "latitude": -22.1256,
        "longitude": -51.3894,
        "coordinates": [(-51.3894, -22.1256)]
    },
    "Americana": {
        "latitude": -22.7374,
        "longitude": -47.3331,
        "coordinates": [(-47.3331, -22.7374)]
    },
    "Guarujá": {
        "latitude": -23.9935,
        "longitude": -46.2564,
        "coordinates": [(-46.2564, -23.9935)]
    },
    "Araraquara": {
        "latitude": -21.7845,
        "longitude": -48.178,
        "coordinates": [(-48.178, -21.7845)]
    },
    "Barretos": {
        "latitude": -20.5571,
        "longitude": -48.5671,
        "coordinates": [(-48.5671, -20.5571)]
    },
    "Itapevi": {
        "latitude": -23.5489,
        "longitude": -46.932,
        "coordinates": [(-46.932, -23.5489)]
    },
    "Itu": {
        "latitude": -23.2544,
        "longitude": -47.2926,
        "coordinates": [(-47.2926, -23.2544)]
    },
    "Araçatuba": {
        "latitude": -21.2076,
        "longitude": -50.4401,
        "coordinates": [(-50.4401, -21.2076)]
    },
    "Botucatu": {
        "latitude": -22.8853,
        "longitude": -48.4437,
        "coordinates": [(-48.4437, -22.8853)]
    },
    "Marília": {
        "latitude": -22.2125,
        "longitude": -49.9451,
        "coordinates": [(-49.9451, -22.2125)]
    },
    "São João da Boa Vista": {
        "latitude": -21.9727,
        "longitude": -46.7963,
        "coordinates": [(-46.7963, -21.9727)]
    },
    "Jaú": {
        "latitude": -22.2936,
        "longitude": -48.5592,
        "coordinates": [(-48.5592, -22.2936)]
    },
    "Limeira": {
        "latitude": -22.5646,
        "longitude": -47.4012,
        "coordinates": [(-47.4012, -22.5646)]
    }
    # Adicione mais municípios conforme necessário
}

# Cores para cada classificação de atividade
atividade_colors = {
    "Atividade Aumentada": "red",
    "Transmissão": "orange",
    "Atenção": "yellow",
    "Baixo Risco": "green"
}

# Classificação de atividade aleatória para cada município fictício
atividade_por_municipio = {municipio: random.choice(list(atividade_colors.keys())) for municipio in municipios_sp}

# Inicialização do Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Layout do aplicativo
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Arbovirose'),

    html.Div(children='''
        Casos de arbovirose em São Paulo de janeiro de 2024 até a data atual.
    '''),

    html.Div([
        html.Div([
            html.Div([
                html.I(className='fas fa-user-plus fa-2x', style={'color': 'orange'}),
                html.H3('Casos Suspeitos', className='text-muted', style={'text-align': 'center'})
            ], className='card-body', style={'text-align': 'center'}),
            html.H4(id='suspected-counter', children='0', className='card-text', style={'text-align': 'center'})
        ], className='col'),

        html.Div([
            html.Div([
                html.I(className='fas fa-user-check fa-2x', style={'color': 'green'}),
                html.H3('Casos Confirmados', className='text-muted', style={'text-align': 'center'})
            ], className='card-body', style={'text-align': 'center'}),
            html.H4(id='confirmed-counter', children='0', className='card-text', style={'text-align': 'center'})
        ], className='col'),

        html.Div([
            html.Div([
                html.I(className='fas fa-bell fa-2x', style={'color': 'blue'}),
                html.H3('Casos Notificados', className='text-muted', style={'text-align': 'center'})
            ], className='card-body', style={'text-align': 'center'}),
            html.H4(id='notified-counter', children='0', className='card-text', style={'text-align': 'center'})
        ], className='col')
    ], className='row justify-content-center'),

    dcc.Graph(
        id='suspected-vs-confirmed',
        figure={
            'data': [
                go.Scatter(
                    x=dates,
                    y=suspected_cases,
                    mode='lines+markers',
                    marker=dict(color='orange'),  # Definindo a cor para laranja
                    name='Casos Suspeitos'
                ),
                go.Scatter(
                    x=dates,
                    y=confirmed_cases,
                    marker=dict(color='green'),  # Definindo a cor para verde
                    mode='lines+markers',
                    name='Casos Confirmados'
                )
            ],
            'layout': go.Layout(
                title='Casos Suspeitos vs Confirmados ao longo do tempo',
                xaxis={'title': 'Data'},
                yaxis={'title': 'Número de Casos'}
            )
        }
    ),

    dcc.Graph(
        id='notified-cases',
        figure={
            'data': [
                go.Bar(
                    x=dates,
                    y=notified_cases
                )
            ],
            'layout': go.Layout(
                title='Casos Notificados por Período',
                xaxis={'title': 'Data'},
                yaxis={'title': 'Número de Casos Notificados'}
            )
        }
    ),

     dcc.Graph(
        id='arbovirose-types',
        figure={
            'data': [
                go.Bar(
                    x=dates,
                    y=[random.randint(50, 5000) for _ in range(len(dates))],
                    name='Dengue'
                ),
                go.Bar(
                    x=dates,
                    y=[random.randint(50, 5000) for _ in range(len(dates))],
                    name='Chikungunya'
                ),
                go.Bar(
                    x=dates,
                    y=[random.randint(50, 5000) for _ in range(len(dates))],
                    name='Zika'
                )
            ],
            'layout': go.Layout(
                title='Casos de Arbovirose por Tipo ao Longo do Tempo',
                xaxis={'title': 'Data'},
                yaxis={'title': 'Número de Casos'},
                barmode='stack'
            )
        }
    ),

    dcc.Graph(
        id='age-distribution',
        figure={
            'data': [
                go.Bar(
                    x=list(range(0, 91)),
                    y=[age_distribution_male.count(age) for age in range(0, 91)],
                    name='Masculino'
                ),
                go.Bar(
                    x=list(range(0, 91)),
                    y=[age_distribution_female.count(age) for age in range(0, 91)],
                    name='Feminino'
                )
            ],
            'layout': go.Layout(
                title='Distribuição de Casos por Idade e Gênero',
                xaxis={'title': 'Idade'},
                yaxis={'title': 'Número de Casos'},
                barmode='stack'
            )
        }
    ),

    dcc.Graph(
        id='gender-distribution',
        figure={
            'data': [
                go.Pie(
                    labels=['Masculino', 'Feminino'],
                    values=[len(age_distribution_male), len(age_distribution_female)]
                )
            ],
            'layout': go.Layout(
                title='Distribuição de Casos por Gênero'
            )
        }
    ),

    html.Div(children=[
        html.H1(children=''),

        dcc.Graph(
            id='arbovirose-heatmap',
            figure={
                'data': [
                    go.Scattermapbox(
                        lat=[municipios_sp[municipio]['latitude'] for municipio in municipios_sp],
                        lon=[municipios_sp[municipio]['longitude'] for municipio in municipios_sp],
                        mode='markers',
                        marker=dict(
                            size=10,
                            color=[  # Cores com base na classificação de atividade de arbovirose
                                'red' if atividade_por_municipio[municipio] == 'Atividade Aumentada'
                                else 'orange' if atividade_por_municipio[municipio] == 'Transmissão'
                                else 'yellow' if atividade_por_municipio[municipio] == 'Atenção'
                                else 'green'  # Baixo Risco
                                for municipio in municipios_sp
                            ],
                            opacity=0.8
                        ),
                        text=[f'Município: {municipio}<br>Atividade: {atividade_por_municipio[municipio]}' for
                              municipio in municipios_sp.keys()],
                    )
                ],
                'layout': go.Layout(
                    title='Mapa de Calor - Atividade de Arbovirose em Municípios de SP',
                    mapbox=dict(
                        center=dict(lat=-23.5505, lon=-46.6333),  # Centralizado em São Paulo
                        zoom=8,  # Zoom inicial
                        style='open-street-map'  # Estilo do mapa
                    )
                )
            }
        )
    ])
])

@app.callback(
    [Output('suspected-counter', 'children'),
     Output('confirmed-counter', 'children'),
     Output('notified-counter', 'children')],
    [Input('suspected-vs-confirmed', 'figure'),
     Input('notified-cases', 'figure')]
)
def update_counters(suspected_vs_confirmed_figure, notified_cases_figure):
    # Calcula o número total de casos suspeitos
    total_suspected = sum(suspected_vs_confirmed_figure['data'][0]['y'])
    # Calcula o número total de casos confirmados
    total_confirmed = sum(suspected_vs_confirmed_figure['data'][1]['y'])
    # Calcula o número total de casos notificados
    total_notified = sum(notified_cases_figure['data'][0]['y'])

    return total_suspected, total_confirmed, total_notified

if __name__ == '__main__':
    app.run_server(debug=True)
