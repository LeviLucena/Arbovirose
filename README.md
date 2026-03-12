![Python](https://img.shields.io/badge/Python-3.x-3776ab?style=flat-square&logo=python&logoColor=white) ![Dash](https://img.shields.io/badge/Dash-4.0-6366f1?style=flat-square&logo=dash&logoColor=white) ![Plotly](https://img.shields.io/badge/Plotly-6.0-1f8ecd?style=flat-square&logo=plotly&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-3.0-13004b?style=flat-square&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-2.0-bf40bf?style=flat-square&logo=numpy&logoColor=white) ![Font Awesome 6](https://img.shields.io/badge/Font_Awesome-6-1e2a6c?style=flat-square&logo=font-awesome&logoColor=white) ![Google Fonts Inter](https://img.shields.io/badge/Google_Fonts-Inter-4285F4?style=flat-square&logo=google-fonts&logoColor=white)
# Arbovirose SP — Dashboard Epidemiológico

Dashboard interativo para monitoramento de casos de arboviroses (Dengue, Chikungunya e Zika) no estado de São Paulo, com dados mock sazonais, filtros dinâmicos e visualizações epidemiológicas avançadas.
<img width="2752" height="1536" alt="Gemini_Generated_Image_bamfsmbamfsmbamf" src="https://github.com/user-attachments/assets/6030909f-f027-4d9b-b069-89a506bd6a7d" />

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

![tela2](https://github.com/user-attachments/assets/dadbd388-cbff-46da-a73f-486b71936536)
![tela3](https://github.com/user-attachments/assets/406aa8a9-4263-4b44-8540-3b4c1d71c894)

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
