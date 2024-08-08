from webviz_config import WebvizPluginABC
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

from model.heatmapbuild import HeatmapBuild
from model.data_handler import DataHandler


rows = 20
cols = 15 # Qntd de valores
# Gerando os valores aleatórios
data = np.random.rand(rows, cols)

# Criando o DataFrame
df = pd.DataFrame(data, columns=[x for x in range(0, 15)], index=[x for x in range(0, 20)])
# Criar o texto de hover para cada célula do heatmap
color_scales = px.colors.named_colorscales()

dthandler = DataHandler()
dthandler.SampleData()

checklist_options = [{'label': column, 'value': int(column)} for column in df.columns]

# go.Layout se refere a configurações de eixos, legendas, títulos do gráfico

heatmap_layout = go.Layout(
                title='Gráfico Poços X Modelos',
                xaxis=dict(title='Poços'),
                yaxis=dict(title='Modelos')
            )

# go.Heatmap diz respeito a configurações do heatmap, como seus dados, eixo de cores, etc

heatmap_heatmap = go.Heatmap()
    

class Heatmap(WebvizPluginABC):

    def __init__(self, app):

        super().__init__()

        self.set_callbacks(app)

    # Layout HTML da página
    @property
    def layout(self):
        return html.Div([
            html.Div([
                html.H1("NQDS HEATMAP"),
                html.Div([
                    dcc.Tabs(id='data-selection', value='modelswells', 
                            children=[
                            dcc.Tab(label='Models by Wells', value='modelswells'),
                            dcc.Tab(label='Attributes by Models', value='attributesmodels'),
                            dcc.Tab(label='Wells by Attributes', value='wellsattributes')
                        ],)
                ],
                style={'display': 'flex', 'justify-content': 'center'}),
                html.P('Color Selection'),
                dcc.Dropdown(
                id='color-scale-dropdown',
                options=[{'label': scale, 'value': scale} for scale in color_scales],
                value="turbo",
                style={'width': '200px'}
                ),
                html.Div([
                    html.Div([
                        html.P("Well Selection", style={'margin-bottom': '0px'}),
                        dcc.Checklist(
                            id='filtro',
                            options=checklist_options,
                            value=[column['value'] for column in checklist_options],
                            inline=True,
                            style={'margin-top': '16px'}
                        ),
                    ],
                    style={'display': 'flex', 'flex-direction': 'column', 'width': '200px'}
                    ),
                    html.Div([
                        html.P("Model Selection", style={'text-align': 'center', 'margin-bottom': '0px'}),
                        dcc.RangeSlider(1, 2, 1, count=1, value=[1, 2], tooltip={"placement": "bottom", "always_visible": False}, id='model_selection'),
                    ],
                    style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-itens': 'center', 'width': '100vh'}
                    )
                ],
                style={'display': 'flex', 'width': '100vh'}
                ),
                html.Div([
                    dcc.Checklist(
                        id='iterations-checklist',
                        options=[
                            {'label': 'Iteration X', 'value': 'X'},
                            {'label': 'Iteration Y', 'value': 'Y'}
                        ],
                        value=['X']  # Iteração X selecionada por padrão
                    ),
                ], style={'display': 'flex', 'margin-top': '16px'}),
                html.Div(
                    id='graph-container',
                    style={'display': 'flex'}
                ),
                html.Button("Invert Axis", id='axis-inversion', n_clicks=0)
            ], style={'display': 'flex', 'justify-content': 'center', 'flex-direction': 'column', 'align-items': 'center'}),
        ], style={'height': '100vh'})
     
    def set_callbacks(self, app):
        @app.callback(
        Output('graph-container', 'children'),
        [Input('iterations-checklist', 'value'),
        Input('color-scale-dropdown', 'value'),
        Input('filtro', 'value'),
        Input('model_selection', 'value'),
        Input('axis-inversion', 'n_clicks'),
        Input('data-selection', 'value')]
        )
        def update_figure(iterations, colorscale, selecao, modelos, axisinvertclicks, heatmap_selection):
            selecao = sorted(selecao)
            print(modelos)

            if heatmap_selection == 'modelswells':
                if axisinvertclicks % 2 == 1:
                    df_filter = dthandler.TransposeData()
                    graphtitle = 'Models by Wells'
                    xaxis = 'Wells'
                    yaxis = 'Models'
                else:
                    df_filter = dthandler.WellsModels()
                    graphtitle = 'Wells by Models'
                    yaxis = 'Wells'
                    xaxis = 'Models'

            elif heatmap_selection == 'attributesmodels':
                if axisinvertclicks % 2 == 1:
                    df_filter = dthandler.TransposeData()
                    graphtitle = 'Models by Attributes'
                    yaxis = 'Models'
                    xaxis = 'Attributes'
                else:
                    df_filter = dthandler.AttributesModels()
                    graphtitle = 'Attributes by Models'
                    yaxis = 'Attributes'
                    xaxis = 'Models'
            elif heatmap_selection == 'wellsattributes':
                    if axisinvertclicks % 2 == 1:
                        df_filter = dthandler.TransposeData()
                        graphtitle = 'Attributes by Wells'
                        yaxis = 'Attributes'
                        xaxis = 'Wells'
                    else:
                        df_filter = dthandler.WellsAttributes()
                        graphtitle = 'Wells by Attributes'
                        yaxis = 'Wells'
                        xaxis = 'Attributes'                

            graphs = []
            for iteration in iterations:
                heatmap = HeatmapBuild(df_filter, title=graphtitle, colorscale=colorscale, xaxis=xaxis, yaxis=yaxis, hovertext=dthandler.HoverText())
                graph = heatmap.buildHeatmap(id=f'heatmap-{iteration}')
                graphs.append(graph)
            return graphs
