# Arbovirose SP — Dashboard Epidemiológico

![logo artigo](https://github.com/LeviLucena/Arbovirose/assets/34045910/74a25acd-b4de-4c01-b849-284bbc16bbc4)

Dashboard interativo para monitoramento de casos de arboviroses (Dengue, Chikungunya e Zika) no estado de São Paulo, com dados mock sazonais, filtros dinâmicos e visualizações epidemiológicas avançadas.

---

## Funcionalidades

- **KPIs com tendência** — Suspeitos, Confirmados, Notificados e Taxa de Confirmação com seta de variação em relação ao período anterior
- **Filtros interativos** — Seletor de período, tipo de arbovirose (Dengue / Chikungunya / Zika) e agregação temporal (Diário / Semanal / Mensal)
- **Tendência temporal** — Gráfico de barras sobrepostas com média móvel de 7 dias
- **Distribuição por arbovirose** — Donut chart com total de casos no centro
- **Mapa de risco** — Mapa dark (carto-darkmatter) com bolhas proporcionais à incidência por município
- **Ranking de municípios** — Top 10 por incidência por 100 mil habitantes
- **Pirâmide etária** — Distribuição bimodal masculino/feminino por faixa etária
- **Tabela de alertas** — Municípios em situação de Epidemia ou Alerta com nível de risco, incidência e população

## Galeria

![tela2](https://github.com/LeviLucena/Arbovirose/assets/34045910/e7cf2876-50d7-46fe-88ee-439850a3e734)
![tela3](https://github.com/LeviLucena/Arbovirose/assets/34045910/e5b25050-13e0-4c9b-9b03-da4eb8222ce3)
![tela4](https://github.com/LeviLucena/Arbovirose/assets/34045910/9a763304-2d70-4087-b0b3-248e6cc370e0)

---

## Tecnologias

| Biblioteca | Versão mínima | Uso |
|---|---|---|
| [Dash](https://dash.plotly.com/) | 4.0 | Framework web interativo |
| [Plotly](https://plotly.com/python/) | 6.0 | Visualizações e mapas |
| [Pandas](https://pandas.pydata.org/) | 3.0 | Manipulação de dados |
| [NumPy](https://numpy.org/) | 2.0 | Geração de dados sazonais |
| Font Awesome 6 | CDN | Ícones |
| Google Fonts (Inter) | CDN | Tipografia |

---

## Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/LeviLucena/Arbovirose.git
cd Arbovirose
```

### 2. Instale as dependências

**Com pip:**
```bash
pip install dash plotly pandas numpy
```

**Com conda (ambiente existente):**
```bash
conda activate <seu-ambiente>
pip install dash plotly pandas numpy
```

### 3. Execute
```bash
python app.py
```

Acesse em: **http://127.0.0.1:8050**

---

## Estrutura do projeto

```
Arbovirose/
└── app.py       # Aplicação Dash — dados, layout e callbacks
```

---

## Sobre os dados

Os dados são **100% simulados (mock)** com sazonalidade realista:

- **Pico no verão austral** (jan–mar): reflete o comportamento epidemiológico real da dengue em SP
- **Distribuição bimodal de idade**: adultos jovens (~25 anos) e idosos (~60 anos)
- **Incidência por município**: proporcional à população real de cada cidade
- **46 municípios** do estado de São Paulo com coordenadas e populações reais

O projeto está preparado para ser conectado a uma API ou banco de dados real substituindo a geração de dados no início do `app.py`.

---

## Contato

- **LinkedIn:** [![Linkedin Badge](https://img.shields.io/badge/-LinkedIn-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/levilucena/)](https://www.linkedin.com/in/levilucena/)
- **GitHub:** [LeviLucena](https://github.com/LeviLucena)
