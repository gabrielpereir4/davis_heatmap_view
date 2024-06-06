from webviz_config import WebvizPluginABC
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

from model.heatmapbuild import HeatmapBuild


rows = 20
cols = 15 # Qntd de valores
# Gerando os valores aleatórios
data = np.random.rand(rows, cols)

# Criando o DataFrame
df = pd.DataFrame(data, columns=[x for x in range(0, 15)], index=[x for x in range(0, 20)])
# Criar o texto de hover para cada célula do heatmap
color_scales = px.colors.named_colorscales()
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

    @property
    def layout(self):
        return html.Div([
            html.Div([
                html.H1("Gráfico Heatmap"),
                html.P('Seleção de Cores:'),
                dcc.Dropdown(
                id='color-scale-dropdown',
                options=[{'label': scale, 'value': scale} for scale in color_scales],
                value="turbo",
                style={'width': '200px'}
                ),
                html.Div([
                    html.Div([
                        html.P("Seleção de Poços", style={'margin-bottom': '0px'}),
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
                        html.P("Seleção de Modelos", style={'text-align': 'center', 'margin-bottom': '0px'}),
                        dcc.RangeSlider(0, 19, 1, count=1, value=[0, 19], tooltip={"placement": "bottom", "always_visible": False}, id='model_selection'),
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
                            {'label': 'Iteração X', 'value': 'X'},
                            {'label': 'Iteração Y', 'value': 'Y'}
                        ],
                        value=['X']  # Iteração X selecionada por padrão
                    ),
                ], style={'display': 'flex', 'margin-top': '16px'}),
                html.Div(
                    id='graph-container',
                    style={'display': 'flex'}
                )
            ], style={'display': 'flex', 'justify-content': 'center', 'flex-direction': 'column', 'align-items': 'center'}),
        ], style={'height': '100vh'})
     
    def set_callbacks(self, app):
        @app.callback(
        Output('graph-container', 'children'),
        [Input('iterations-checklist', 'value'),
        Input('color-scale-dropdown', 'value'),
        Input('filtro', 'value'),
        Input('model_selection', 'value')]
        )
        def update_figure(iterations, colorscale, selecao, modelos):
            #print(selecao)
            selecao = sorted(selecao)
            #print(selecao)
            df_filter =  df.iloc[modelos[0]:modelos[1]+1, selecao]
            print(modelos)

            hovertext = [[f'Modelo: {df_filter.index[row]}, Poço: {col}, NQDS: {df_filter.iloc[row][col]:.2f}' for col in (df_filter.columns)] for row in range(df_filter.shape[0])]


            graphs = []
            for iteration in iterations:
                heatmap = HeatmapBuild(df_filter, colorscale=colorscale, hovertext=hovertext)
                graph = heatmap.buildHeatmap(id=f'heatmap-{iteration}')
                graphs.append(graph)
            return graphs
        
        @app.callback(
        Output('novoheatmap', 'children'),
        [Input('color-scale-dropdown', 'value'),
        Input('toggleheatmap', 'value'),
        Input('filtro', 'value')]
        )
        def toggle_extraheatmap(colorscale, value, selecao):
            if 'show' in value:
                df_filter = df[selecao]
                hovertext = [[f'Modelo: {df_filter.index[row]}, Poço: {df_filter.columns[col]}, NQDS: {df_filter[row][col]:.2f}' for col in range(cols)] for row in range(rows)]

                heatmap = go.Heatmap(
                    z=df_filter,
                    colorscale=colorscale,
                    colorbar=dict(title='Precisão'),
                    hovertext=hovertext

                )
                layout = heatmap_layout
                return dcc.Graph(
                    id='extra-heatmap-graph',
                    figure={'data': [heatmap], 'layout': layout}
                )
            else:
                return None