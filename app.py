import dash
from dash import dcc, html
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import random

# ─────────────────────────────────────────────
# DADOS MOCK COM SAZONALIDADE REALISTA
# ─────────────────────────────────────────────
random.seed(42)
np.random.seed(42)

# Período completo
dates = pd.date_range(start='2024-01-01', end=pd.Timestamp.today(), freq='D')
n = len(dates)

# Sazonalidade: dengue/arbovírus explodem no verão (jan-mar) e diminuem no inverno
def seasonal_wave(dates, base, amplitude, noise_scale):
    day_of_year = np.array([d.timetuple().tm_yday for d in dates])
    # Pico no verão austral (~dia 30) e queda no inverno (~dia 200)
    seasonal = amplitude * np.cos(2 * np.pi * (day_of_year - 30) / 365)
    noise = np.random.normal(0, noise_scale, len(dates))
    values = base + seasonal + noise
    return np.clip(values, 10, None).astype(int)

suspected_cases  = seasonal_wave(dates, base=2500, amplitude=1800, noise_scale=300)
confirmed_cases  = seasonal_wave(dates, base=800,  amplitude=600,  noise_scale=120)
notified_cases   = seasonal_wave(dates, base=5000, amplitude=3500, noise_scale=500)

# Dados por arbovirose com padrão diferente
dengue_cases      = seasonal_wave(dates, base=1500, amplitude=1400, noise_scale=200)
chikungunya_cases = seasonal_wave(dates, base=600,  amplitude=300,  noise_scale=100)
zika_cases        = seasonal_wave(dates, base=200,  amplitude=100,  noise_scale=50)

# DataFrame principal
df = pd.DataFrame({
    'date': dates,
    'suspeitos': suspected_cases,
    'confirmados': confirmed_cases,
    'notificados': notified_cases,
    'dengue': dengue_cases,
    'chikungunya': chikungunya_cases,
    'zika': zika_cases,
})
df['semana_epi'] = df['date'].dt.isocalendar().week
df['mes']        = df['date'].dt.to_period('M')
df['ano']        = df['date'].dt.year

# Distribuição por idade e gênero com pico em adultos jovens
def bimodal_ages(n, peak1=25, peak2=60, std=12):
    half = n // 2
    a = np.random.normal(peak1, std, half)
    b = np.random.normal(peak2, std, n - half)
    return np.clip(np.concatenate([a, b]), 0, 90).astype(int)

age_male   = bimodal_ages(1800)
age_female = bimodal_ages(2200, peak1=28, peak2=55)

# ─────────────────────────────────────────────
# MUNICÍPIOS DE SP COM DADOS DE CASOS
# ─────────────────────────────────────────────
municipios_sp = {
    "São Paulo":              {"lat": -23.5505, "lon": -46.6333, "pop": 12_325_000},
    "Guarulhos":              {"lat": -23.4540, "lon": -46.5333, "pop": 1_392_000},
    "Campinas":               {"lat": -22.9055, "lon": -47.0608, "pop": 1_214_000},
    "São Bernardo do Campo":  {"lat": -23.6914, "lon": -46.5364, "pop": 844_000},
    "Santo André":            {"lat": -23.6734, "lon": -46.5384, "pop": 723_000},
    "Osasco":                 {"lat": -23.5329, "lon": -46.7915, "pop": 696_000},
    "São José dos Campos":    {"lat": -23.2237, "lon": -45.9009, "pop": 729_000},
    "Ribeirão Preto":         {"lat": -21.1699, "lon": -47.8208, "pop": 711_000},
    "Sorocaba":               {"lat": -23.5015, "lon": -47.4587, "pop": 683_000},
    "Mogi das Cruzes":        {"lat": -23.5225, "lon": -46.1884, "pop": 448_000},
    "Diadema":                {"lat": -23.6816, "lon": -46.6205, "pop": 420_000},
    "Jundiaí":                {"lat": -23.1857, "lon": -46.8978, "pop": 423_000},
    "Bauru":                  {"lat": -22.3145, "lon": -49.0609, "pop": 379_000},
    "Carapicuíba":            {"lat": -23.5235, "lon": -46.8407, "pop": 383_000},
    "Piracicaba":             {"lat": -22.7242, "lon": -47.6476, "pop": 406_000},
    "São José do Rio Preto":  {"lat": -20.8114, "lon": -49.3759, "pop": 465_000},
    "Santos":                 {"lat": -23.9535, "lon": -46.3330, "pop": 433_000},
    "Taubaté":                {"lat": -23.0264, "lon": -45.5558, "pop": 318_000},
    "Mauá":                   {"lat": -23.6677, "lon": -46.4613, "pop": 468_000},
    "Barueri":                {"lat": -23.5107, "lon": -46.8768, "pop": 261_000},
    "Praia Grande":           {"lat": -24.0058, "lon": -46.4022, "pop": 330_000},
    "Franca":                 {"lat": -20.5352, "lon": -47.4009, "pop": 352_000},
    "Suzano":                 {"lat": -23.5446, "lon": -46.3117, "pop": 305_000},
    "Itaquaquecetuba":        {"lat": -23.4868, "lon": -46.3473, "pop": 362_000},
    "Presidente Prudente":    {"lat": -22.1256, "lon": -51.3894, "pop": 228_000},
    "Americana":              {"lat": -22.7374, "lon": -47.3331, "pop": 241_000},
    "São Carlos":             {"lat": -22.0174, "lon": -47.8861, "pop": 254_000},
    "Araraquara":             {"lat": -21.7845, "lon": -48.1780, "pop": 238_000},
    "Ribeirão Pires":         {"lat": -23.7067, "lon": -46.4116, "pop": 119_000},
    "Marília":                {"lat": -22.2125, "lon": -49.9451, "pop": 240_000},
    "Botucatu":               {"lat": -22.8853, "lon": -48.4437, "pop": 148_000},
    "Araçatuba":              {"lat": -21.2076, "lon": -50.4401, "pop": 191_000},
    "Limeira":                {"lat": -22.5646, "lon": -47.4012, "pop": 301_000},
    "Jacareí":                {"lat": -23.3052, "lon": -45.9662, "pop": 232_000},
    "Guarujá":                {"lat": -23.9935, "lon": -46.2564, "pop": 309_000},
    "Embu das Artes":         {"lat": -23.6486, "lon": -46.8523, "pop": 270_000},
    "Taboão da Serra":        {"lat": -23.6099, "lon": -46.7833, "pop": 284_000},
    "Itapevi":                {"lat": -23.5489, "lon": -46.9320, "pop": 230_000},
    "São Vicente":            {"lat": -23.9574, "lon": -46.3889, "pop": 356_000},
    "Barretos":               {"lat": -20.5571, "lon": -48.5671, "pop": 118_000},
    "Jaú":                    {"lat": -22.2936, "lon": -48.5592, "pop": 139_000},
    "Itu":                    {"lat": -23.2544, "lon": -47.2926, "pop": 170_000},
    "São João da Boa Vista":  {"lat": -21.9727, "lon": -46.7963, "pop": 92_000},
    "Santo Amaro":            {"lat": -23.6459, "lon": -46.6983, "pop": 80_000},
    "São Caetano do Sul":     {"lat": -23.6229, "lon": -46.5548, "pop": 162_000},
}

# Casos e incidência por município
np.random.seed(99)
for m, data in municipios_sp.items():
    casos = int(np.random.gamma(shape=2, scale=data['pop'] / 5000))
    data['casos']      = max(casos, 10)
    data['incidencia'] = round(data['casos'] / data['pop'] * 100_000, 1)
    data['nivel']      = (
        'Epidemia'        if data['incidencia'] > 300 else
        'Alerta'          if data['incidencia'] > 150 else
        'Atenção'         if data['incidencia'] > 75  else
        'Baixo Risco'
    )

nivel_color = {
    'Epidemia':   '#e63946',
    'Alerta':     '#f4a261',
    'Atenção':    '#e9c46a',
    'Baixo Risco':'#2a9d8f',
}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def fmt_num(n):
    return f"{n:,.0f}".replace(',', '.')

def trend_pct(current, previous):
    if previous == 0:
        return 0
    return round((current - previous) / previous * 100, 1)

def moving_average(arr, window=7):
    return pd.Series(arr).rolling(window, min_periods=1).mean().values

# ─────────────────────────────────────────────
# TEMA / ESTILOS
# ─────────────────────────────────────────────
BG_DARK   = '#0d1117'
BG_CARD   = '#161b22'
BG_CARD2  = '#1c2128'
BORDER    = '#30363d'
TXT_MAIN  = '#e6edf3'
TXT_MUTED = '#8b949e'
ACCENT    = '#58a6ff'
GREEN     = '#3fb950'
ORANGE    = '#f78166'
YELLOW    = '#e3b341'
RED       = '#ff6b6b'
PURPLE    = '#bc8cff'

BASE_LEGEND = dict(bgcolor=BG_CARD, bordercolor=BORDER, borderwidth=1)

PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor=BG_CARD,
        plot_bgcolor=BG_CARD2,
        font=dict(color=TXT_MAIN, family='Inter, sans-serif'),
        xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zerolinecolor=BORDER),
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zerolinecolor=BORDER),
        margin=dict(l=40, r=20, t=50, b=40),
    )
)

def layout(**kwargs):
    """Mescla o template base com overrides sem duplicar chaves."""
    base = dict(PLOTLY_TEMPLATE['layout'])
    if 'legend' in kwargs:
        kwargs['legend'] = {**BASE_LEGEND, **kwargs['legend']}
    else:
        kwargs['legend'] = BASE_LEGEND
    base.update(kwargs)
    return base

card_style = {
    'backgroundColor': BG_CARD,
    'border': f'1px solid {BORDER}',
    'borderRadius': '12px',
    'padding': '20px',
}

# ─────────────────────────────────────────────
# APP
# ─────────────────────────────────────────────
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = 'Arbovirose SP — Dashboard Epidemiológico'

# ─────────────────────────────────────────────
# LAYOUT
# ─────────────────────────────────────────────
app.layout = html.Div(style={
    'backgroundColor': BG_DARK,
    'minHeight': '100vh',
    'fontFamily': 'Inter, sans-serif',
    'color': TXT_MAIN,
}, children=[

    # ── HEADER ──────────────────────────────
    html.Div(style={
        'backgroundColor': BG_CARD,
        'borderBottom': f'1px solid {BORDER}',
        'padding': '16px 32px',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'space-between',
    }, children=[
        html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '12px'}, children=[
            html.I(className='fas fa-mosquito', style={'color': ORANGE, 'fontSize': '28px'}),
            html.Div([
                html.H1('Arbovirose SP', style={'margin': 0, 'fontSize': '22px', 'fontWeight': 700}),
                html.Span('Dashboard Epidemiológico', style={'color': TXT_MUTED, 'fontSize': '13px'}),
            ]),
        ]),
        html.Div(style={'display': 'flex', 'alignItems': 'center', 'gap': '24px'}, children=[
            html.Div(style={'textAlign': 'right'}, children=[
                html.Div('Última Atualização', style={'color': TXT_MUTED, 'fontSize': '11px'}),
                html.Div(pd.Timestamp.today().strftime('%d/%m/%Y %H:%M'),
                         style={'fontSize': '13px', 'fontWeight': 600}),
            ]),
            html.Span('● AO VIVO', style={
                'color': GREEN, 'fontSize': '12px', 'fontWeight': 600,
                'backgroundColor': '#1a3a2a', 'padding': '4px 10px',
                'borderRadius': '20px', 'border': f'1px solid {GREEN}',
            }),
        ]),
    ]),

    # ── FILTROS ──────────────────────────────
    html.Div(style={
        'padding': '16px 32px',
        'backgroundColor': BG_CARD2,
        'borderBottom': f'1px solid {BORDER}',
        'display': 'flex',
        'gap': '20px',
        'flexWrap': 'wrap',
        'alignItems': 'center',
    }, children=[
        html.Div([
            html.Label('Período', style={'color': TXT_MUTED, 'fontSize': '12px', 'display': 'block', 'marginBottom': '4px'}),
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=dates[0].date(),
                max_date_allowed=dates[-1].date(),
                start_date=dates[max(0, len(dates)-90)].date(),
                end_date=dates[-1].date(),
                display_format='DD/MM/YYYY',
                style={'fontSize': '13px'},
            ),
        ]),
        html.Div([
            html.Label('Arbovirose', style={'color': TXT_MUTED, 'fontSize': '12px', 'display': 'block', 'marginBottom': '4px'}),
            dcc.Dropdown(
                id='disease-filter',
                options=[
                    {'label': 'Todas', 'value': 'all'},
                    {'label': 'Dengue', 'value': 'dengue'},
                    {'label': 'Chikungunya', 'value': 'chikungunya'},
                    {'label': 'Zika', 'value': 'zika'},
                ],
                value='all',
                clearable=False,
                style={'width': '180px', 'fontSize': '13px', 'backgroundColor': BG_CARD, 'color': TXT_MAIN},
            ),
        ]),
        html.Div([
            html.Label('Agregação', style={'color': TXT_MUTED, 'fontSize': '12px', 'display': 'block', 'marginBottom': '4px'}),
            dcc.RadioItems(
                id='aggregation',
                options=[
                    {'label': 'Diário', 'value': 'D'},
                    {'label': 'Semanal', 'value': 'W'},
                    {'label': 'Mensal', 'value': 'ME'},
                ],
                value='W',
                inline=True,
                style={'fontSize': '13px', 'color': TXT_MAIN},
                inputStyle={'marginRight': '4px', 'marginLeft': '12px'},
            ),
        ]),
    ]),

    # ── CONTEÚDO PRINCIPAL ──────────────────
    html.Div(style={'padding': '24px 32px'}, children=[

        # ── KPI CARDS ────────────────────────
        html.Div(style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
            'gap': '16px',
            'marginBottom': '24px',
        }, children=[
            # Suspeitos
            html.Div(style={**card_style, 'borderLeft': f'4px solid {YELLOW}'}, children=[
                html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start'}, children=[
                    html.Div([
                        html.Div('Suspeitos', style={'color': TXT_MUTED, 'fontSize': '12px', 'fontWeight': 500, 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.H2(id='kpi-suspeitos', style={'margin': '6px 0 0', 'fontSize': '28px', 'fontWeight': 700, 'color': YELLOW}),
                        html.Div(id='trend-suspeitos', style={'fontSize': '12px', 'marginTop': '4px'}),
                    ]),
                    html.I(className='fas fa-user-clock', style={'color': YELLOW, 'fontSize': '24px', 'opacity': '0.7'}),
                ]),
            ]),
            # Confirmados
            html.Div(style={**card_style, 'borderLeft': f'4px solid {ORANGE}'}, children=[
                html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start'}, children=[
                    html.Div([
                        html.Div('Confirmados', style={'color': TXT_MUTED, 'fontSize': '12px', 'fontWeight': 500, 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.H2(id='kpi-confirmados', style={'margin': '6px 0 0', 'fontSize': '28px', 'fontWeight': 700, 'color': ORANGE}),
                        html.Div(id='trend-confirmados', style={'fontSize': '12px', 'marginTop': '4px'}),
                    ]),
                    html.I(className='fas fa-virus', style={'color': ORANGE, 'fontSize': '24px', 'opacity': '0.7'}),
                ]),
            ]),
            # Notificados
            html.Div(style={**card_style, 'borderLeft': f'4px solid {ACCENT}'}, children=[
                html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start'}, children=[
                    html.Div([
                        html.Div('Notificados', style={'color': TXT_MUTED, 'fontSize': '12px', 'fontWeight': 500, 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.H2(id='kpi-notificados', style={'margin': '6px 0 0', 'fontSize': '28px', 'fontWeight': 700, 'color': ACCENT}),
                        html.Div(id='trend-notificados', style={'fontSize': '12px', 'marginTop': '4px'}),
                    ]),
                    html.I(className='fas fa-bell', style={'color': ACCENT, 'fontSize': '24px', 'opacity': '0.7'}),
                ]),
            ]),
            # Taxa Confirmação
            html.Div(style={**card_style, 'borderLeft': f'4px solid {PURPLE}'}, children=[
                html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start'}, children=[
                    html.Div([
                        html.Div('Taxa Confirmação', style={'color': TXT_MUTED, 'fontSize': '12px', 'fontWeight': 500, 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.H2(id='kpi-taxa', style={'margin': '6px 0 0', 'fontSize': '28px', 'fontWeight': 700, 'color': PURPLE}),
                        html.Div('confirmados / suspeitos', style={'color': TXT_MUTED, 'fontSize': '11px', 'marginTop': '4px'}),
                    ]),
                    html.I(className='fas fa-percent', style={'color': PURPLE, 'fontSize': '24px', 'opacity': '0.7'}),
                ]),
            ]),
            # Municípios em Alerta
            html.Div(style={**card_style, 'borderLeft': f'4px solid {RED}'}, children=[
                html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start'}, children=[
                    html.Div([
                        html.Div('Municípios em Alerta', style={'color': TXT_MUTED, 'fontSize': '12px', 'fontWeight': 500, 'textTransform': 'uppercase', 'letterSpacing': '0.5px'}),
                        html.H2(
                            str(sum(1 for d in municipios_sp.values() if d['nivel'] in ('Epidemia', 'Alerta'))),
                            style={'margin': '6px 0 0', 'fontSize': '28px', 'fontWeight': 700, 'color': RED}
                        ),
                        html.Div('epidemia ou alerta ativo', style={'color': TXT_MUTED, 'fontSize': '11px', 'marginTop': '4px'}),
                    ]),
                    html.I(className='fas fa-triangle-exclamation', style={'color': RED, 'fontSize': '24px', 'opacity': '0.7'}),
                ]),
            ]),
        ]),

        # ── ROW 1: Série Temporal + Tipos ────
        html.Div(style={
            'display': 'grid',
            'gridTemplateColumns': '2fr 1fr',
            'gap': '16px',
            'marginBottom': '16px',
        }, children=[
            html.Div(style=card_style, children=[
                html.H3('Tendência Temporal', style={'margin': '0 0 4px', 'fontSize': '15px', 'fontWeight': 600}),
                html.P('Casos suspeitos e confirmados com média móvel de 7 dias', style={'color': TXT_MUTED, 'fontSize': '12px', 'margin': '0 0 12px'}),
                dcc.Graph(id='graph-temporal', config={'displayModeBar': False}),
            ]),
            html.Div(style=card_style, children=[
                html.H3('Por Arbovirose', style={'margin': '0 0 4px', 'fontSize': '15px', 'fontWeight': 600}),
                html.P('Distribuição por tipo no período', style={'color': TXT_MUTED, 'fontSize': '12px', 'margin': '0 0 12px'}),
                dcc.Graph(id='graph-tipos', config={'displayModeBar': False}),
            ]),
        ]),

        # ── ROW 2: Mapa + Incidência ─────────
        html.Div(style={
            'display': 'grid',
            'gridTemplateColumns': '3fr 2fr',
            'gap': '16px',
            'marginBottom': '16px',
        }, children=[
            html.Div(style=card_style, children=[
                html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '12px'}, children=[
                    html.Div([
                        html.H3('Mapa de Risco — São Paulo', style={'margin': 0, 'fontSize': '15px', 'fontWeight': 600}),
                        html.P('Incidência por 100 mil habitantes', style={'color': TXT_MUTED, 'fontSize': '12px', 'margin': 0}),
                    ]),
                    html.Div(style={'display': 'flex', 'gap': '10px', 'flexWrap': 'wrap'}, children=[
                        html.Span(f'● {k}', style={'color': v, 'fontSize': '11px', 'fontWeight': 500})
                        for k, v in nivel_color.items()
                    ]),
                ]),
                dcc.Graph(id='graph-mapa', config={'displayModeBar': False}),
            ]),
            html.Div(style=card_style, children=[
                html.H3('Top 10 Municípios', style={'margin': '0 0 4px', 'fontSize': '15px', 'fontWeight': 600}),
                html.P('Maior incidência por 100 mil hab.', style={'color': TXT_MUTED, 'fontSize': '12px', 'margin': '0 0 12px'}),
                dcc.Graph(id='graph-ranking', config={'displayModeBar': False}),
            ]),
        ]),

        # ── ROW 3: Faixa Etária + Gênero ────
        html.Div(style={
            'display': 'grid',
            'gridTemplateColumns': '2fr 1fr',
            'gap': '16px',
            'marginBottom': '16px',
        }, children=[
            html.Div(style=card_style, children=[
                html.H3('Pirâmide Etária', style={'margin': '0 0 4px', 'fontSize': '15px', 'fontWeight': 600}),
                html.P('Distribuição de casos por faixa etária e gênero', style={'color': TXT_MUTED, 'fontSize': '12px', 'margin': '0 0 12px'}),
                dcc.Graph(id='graph-idade', config={'displayModeBar': False}),
            ]),
            html.Div(style=card_style, children=[
                html.H3('Distribuição por Gênero', style={'margin': '0 0 4px', 'fontSize': '15px', 'fontWeight': 600}),
                html.P('Proporção total do período', style={'color': TXT_MUTED, 'fontSize': '12px', 'margin': '0 0 12px'}),
                dcc.Graph(id='graph-genero', config={'displayModeBar': False}),
            ]),
        ]),

        # ── ROW 4: Tabela de Alertas ─────────
        html.Div(style=card_style, children=[
            html.H3('Municípios em Situação de Alerta ou Epidemia', style={'margin': '0 0 4px', 'fontSize': '15px', 'fontWeight': 600}),
            html.P('Municípios com incidência acima de 150 casos por 100 mil habitantes', style={'color': TXT_MUTED, 'fontSize': '12px', 'margin': '0 0 12px'}),
            html.Div(id='alerta-table'),
        ]),

    ]),

    # ── FOOTER ───────────────────────────────
    html.Div(style={
        'backgroundColor': BG_CARD,
        'borderTop': f'1px solid {BORDER}',
        'padding': '16px 32px',
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'marginTop': '8px',
    }, children=[
        html.Span('Desenvolvido por Levi Lucena · Dados ilustrativos (mock)',
                  style={'color': TXT_MUTED, 'fontSize': '12px'}),
        html.Div(style={'display': 'flex', 'gap': '16px'}, children=[
            html.A(html.I(className='fab fa-github', style={'fontSize': '18px'}),
                   href='https://github.com/LeviLucena', target='_blank', style={'color': TXT_MUTED}),
            html.A(html.I(className='fab fa-linkedin', style={'fontSize': '18px'}),
                   href='https://linkedin.com/in/levilucena', target='_blank', style={'color': TXT_MUTED}),
        ]),
    ]),

])

# ─────────────────────────────────────────────
# CALLBACKS
# ─────────────────────────────────────────────

def filter_df(start_date, end_date):
    mask = (df['date'] >= pd.Timestamp(start_date)) & (df['date'] <= pd.Timestamp(end_date))
    return df[mask].copy()

def aggregate(dff, col, freq):
    return dff.groupby(pd.Grouper(key='date', freq=freq))[col].sum().reset_index()

@app.callback(
    [Output('kpi-suspeitos',    'children'),
     Output('kpi-confirmados',  'children'),
     Output('kpi-notificados',  'children'),
     Output('kpi-taxa',         'children'),
     Output('trend-suspeitos',  'children'),
     Output('trend-confirmados','children'),
     Output('trend-notificados','children'),
     Output('graph-temporal',   'figure'),
     Output('graph-tipos',      'figure'),
     Output('graph-mapa',       'figure'),
     Output('graph-ranking',    'figure'),
     Output('graph-idade',      'figure'),
     Output('graph-genero',     'figure'),
     Output('alerta-table',     'children')],
    [Input('date-range',    'start_date'),
     Input('date-range',    'end_date'),
     Input('disease-filter','value'),
     Input('aggregation',   'value')],
)
def update_all(start_date, end_date, disease, freq):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate

    dff = filter_df(start_date, end_date)

    # ─ KPIs ─────────────────────────────────
    total_sus  = int(dff['suspeitos'].sum())
    total_conf = int(dff['confirmados'].sum())
    total_noti = int(dff['notificados'].sum())
    taxa       = round(total_conf / total_sus * 100, 1) if total_sus else 0

    # Período anterior de mesmo tamanho para calcular tendência
    n_days = (pd.Timestamp(end_date) - pd.Timestamp(start_date)).days
    prev_end   = pd.Timestamp(start_date) - pd.Timedelta(days=1)
    prev_start = prev_end - pd.Timedelta(days=n_days)
    dfp = filter_df(prev_start.date(), prev_end.date())
    prev_sus  = int(dfp['suspeitos'].sum())  if len(dfp) else total_sus
    prev_conf = int(dfp['confirmados'].sum()) if len(dfp) else total_conf
    prev_noti = int(dfp['notificados'].sum()) if len(dfp) else total_noti

    def trend_badge(current, previous):
        pct = trend_pct(current, previous)
        if pct > 0:
            return html.Span([html.I(className='fas fa-arrow-up'), f' {pct}% vs período anterior'],
                             style={'color': RED})
        elif pct < 0:
            return html.Span([html.I(className='fas fa-arrow-down'), f' {abs(pct)}% vs período anterior'],
                             style={'color': GREEN})
        else:
            return html.Span('— sem variação', style={'color': TXT_MUTED})

    # ─ Gráfico Temporal ─────────────────────
    disease_col = 'suspeitos' if disease == 'all' else disease
    agg_sus  = aggregate(dff, 'suspeitos',   freq)
    agg_conf = aggregate(dff, 'confirmados', freq)

    ma_sus  = moving_average(agg_sus['suspeitos'])
    ma_conf = moving_average(agg_conf['confirmados'])

    fig_temporal = go.Figure()
    fig_temporal.add_trace(go.Bar(
        x=agg_sus['date'], y=agg_sus['suspeitos'],
        name='Suspeitos', marker_color=YELLOW, opacity=0.5,
    ))
    fig_temporal.add_trace(go.Bar(
        x=agg_conf['date'], y=agg_conf['confirmados'],
        name='Confirmados', marker_color=ORANGE, opacity=0.7,
    ))
    fig_temporal.add_trace(go.Scatter(
        x=agg_sus['date'], y=ma_sus,
        name='Média Móvel (Sus.)', line=dict(color=YELLOW, width=2, dash='dot'),
        mode='lines',
    ))
    fig_temporal.add_trace(go.Scatter(
        x=agg_conf['date'], y=ma_conf,
        name='Média Móvel (Conf.)', line=dict(color=ORANGE, width=2, dash='dot'),
        mode='lines',
    ))
    fig_temporal.update_layout(**layout(
        barmode='overlay',
        height=320,
        legend=dict(orientation='h', y=-0.15),
        xaxis_title=None, yaxis_title='Casos',
    ))

    # ─ Gráfico Tipos ────────────────────────
    cols = ['dengue', 'chikungunya', 'zika'] if disease == 'all' else [disease]
    colors_tipo = {'dengue': '#ef476f', 'chikungunya': '#ffd166', 'zika': '#06d6a0'}
    totais = {c: int(dff[c].sum()) for c in cols}
    fig_tipos = go.Figure(go.Pie(
        labels=[c.capitalize() for c in cols],
        values=[totais[c] for c in cols],
        hole=0.6,
        marker=dict(colors=[colors_tipo[c] for c in cols]),
        textinfo='percent+label',
        textfont=dict(size=13, color=TXT_MAIN),
    ))
    fig_tipos.update_layout(**layout(
        height=320,
        showlegend=False,
        annotations=[dict(
            text=f"{fmt_num(sum(totais.values()))}<br><span style='font-size:11px'>casos</span>",
            x=0.5, y=0.5, font_size=20, showarrow=False, font_color=TXT_MAIN,
        )],
    ))

    # ─ Mapa ─────────────────────────────────
    lats   = [d['lat']        for d in municipios_sp.values()]
    lons   = [d['lon']        for d in municipios_sp.values()]
    sizes  = [max(8, d['casos'] / 500) for d in municipios_sp.values()]
    colors_map = [nivel_color[d['nivel']] for d in municipios_sp.values()]
    texts  = [
        f"<b>{m}</b><br>Incidência: {d['incidencia']}/100k<br>Casos: {fmt_num(d['casos'])}<br>Nível: {d['nivel']}"
        for m, d in municipios_sp.items()
    ]

    fig_mapa = go.Figure(go.Scattermap(
        lat=lats, lon=lons,
        mode='markers',
        marker=dict(size=sizes, color=colors_map, opacity=0.85),
        text=texts,
        hovertemplate='%{text}<extra></extra>',
    ))
    fig_mapa.update_layout(**layout(
        height=360,
        map=dict(
            style='carto-darkmatter',
            center=dict(lat=-22.5, lon=-47.5),
            zoom=5.5,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    ))

    # ─ Ranking municípios ───────────────────
    top10 = sorted(municipios_sp.items(), key=lambda x: x[1]['incidencia'], reverse=True)[:10]
    nomes   = [m for m, _ in top10]
    incids  = [d['incidencia'] for _, d in top10]
    bar_colors = [nivel_color[d['nivel']] for _, d in top10]

    fig_rank = go.Figure(go.Bar(
        x=incids, y=nomes,
        orientation='h',
        marker_color=bar_colors,
        text=[f"{v}" for v in incids],
        textposition='outside',
        textfont=dict(color=TXT_MAIN, size=11),
    ))
    fig_rank.update_layout(**layout(
        height=360,
        xaxis_title='Incidência / 100k hab.',
        yaxis=dict(autorange='reversed', tickfont=dict(size=11)),
    ))

    # ─ Pirâmide etária ──────────────────────
    bins = list(range(0, 91, 5))
    labels_age = [f'{b}-{b+4}' for b in bins[:-1]] + ['85+']

    def age_hist(ages):
        counts = [sum(1 for a in ages if b <= a < b+5) for b in bins[:-1]]
        counts.append(sum(1 for a in ages if a >= 85))
        return counts

    m_counts = age_hist(age_male)
    f_counts = age_hist(age_female)

    fig_idade = go.Figure()
    fig_idade.add_trace(go.Bar(
        y=labels_age, x=[-v for v in m_counts],
        orientation='h', name='Masculino',
        marker_color=ACCENT, hovertemplate='Masculino: %{customdata}<extra></extra>',
        customdata=m_counts,
    ))
    fig_idade.add_trace(go.Bar(
        y=labels_age, x=f_counts,
        orientation='h', name='Feminino',
        marker_color='#f783ac', hovertemplate='Feminino: %{x}<extra></extra>',
    ))
    fig_idade.update_layout(**layout(
        height=340,
        barmode='overlay',
        xaxis=dict(
            tickvals=[-60, -40, -20, 0, 20, 40, 60],
            ticktext=['60','40','20','0','20','40','60'],
            title='Número de casos',
        ),
        yaxis_title='Faixa etária',
        legend=dict(orientation='h', y=-0.15),
    ))

    # ─ Gênero ───────────────────────────────
    fig_genero = go.Figure(go.Pie(
        labels=['Masculino', 'Feminino'],
        values=[len(age_male), len(age_female)],
        hole=0.55,
        marker=dict(colors=[ACCENT, '#f783ac']),
        textinfo='percent',
        textfont=dict(size=15, color=TXT_MAIN),
    ))
    fig_genero.update_layout(**layout(
        height=340,
        legend=dict(orientation='h', y=-0.05),
    ))

    # ─ Tabela de Alertas ────────────────────
    alertas = [
        (m, d) for m, d in municipios_sp.items()
        if d['nivel'] in ('Epidemia', 'Alerta')
    ]
    alertas.sort(key=lambda x: x[1]['incidencia'], reverse=True)

    header_style = {
        'backgroundColor': BG_DARK,
        'padding': '10px 16px',
        'fontSize': '11px',
        'fontWeight': 600,
        'textTransform': 'uppercase',
        'letterSpacing': '0.5px',
        'color': TXT_MUTED,
        'borderBottom': f'1px solid {BORDER}',
    }
    row_style = {
        'padding': '10px 16px',
        'borderBottom': f'1px solid {BORDER}',
        'fontSize': '13px',
    }

    table = html.Table(style={
        'width': '100%',
        'borderCollapse': 'collapse',
    }, children=[
        html.Thead(html.Tr([
            html.Th('Município',     style=header_style),
            html.Th('Nível',         style=header_style),
            html.Th('Incidência',    style=header_style),
            html.Th('Casos Estimados', style=header_style),
            html.Th('População',     style=header_style),
        ])),
        html.Tbody([
            html.Tr([
                html.Td(m, style=row_style),
                html.Td(
                    html.Span(d['nivel'], style={
                        'backgroundColor': nivel_color[d['nivel']] + '33',
                        'color': nivel_color[d['nivel']],
                        'padding': '2px 10px',
                        'borderRadius': '20px',
                        'fontWeight': 600,
                        'fontSize': '12px',
                    }),
                    style=row_style
                ),
                html.Td(f"{d['incidencia']}/100k", style={**row_style, 'color': nivel_color[d['nivel']], 'fontWeight': 600}),
                html.Td(fmt_num(d['casos']),  style=row_style),
                html.Td(fmt_num(d['pop']),    style=row_style),
            ]) for m, d in alertas
        ]),
    ])

    return (
        fmt_num(total_sus),
        fmt_num(total_conf),
        fmt_num(total_noti),
        f'{taxa}%',
        trend_badge(total_sus,  prev_sus),
        trend_badge(total_conf, prev_conf),
        trend_badge(total_noti, prev_noti),
        fig_temporal,
        fig_tipos,
        fig_mapa,
        fig_rank,
        fig_idade,
        fig_genero,
        table,
    )


if __name__ == '__main__':
    app.run(debug=True)
