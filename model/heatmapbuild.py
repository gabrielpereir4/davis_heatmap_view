import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, html, dcc, Input, Output

# Classe para construir o Heatmap. Como estamos trabalhando com Heatmaps iguais, a classe encapsula a configuração dos gráficos.

class HeatmapBuild:
    def __init__(self, data, title='Models by Wells', colorscale='turbo', xaxis='Wells', yaxis='Models', hovertext=None):
        self.__data = data
        self.__title = title
        self.__colorscale = colorscale
        self.__xaxis = xaxis
        self.__yaxis = yaxis
        self.__layout = go.Layout(
                title= self.__title,
                # Building the x and y axis "captions"
                xaxis=dict(title= self.__xaxis, tickvals=list(range(len(self.data.columns))), ticktext=self.data.columns.tolist()),
                yaxis=dict(title= self.__yaxis, tickvals=list(range(len(self.data.index))), ticktext=self.data.index.tolist())
            )
        self.__heatmap = go.Heatmap(
                z=data,
                colorscale=colorscale,
                colorbar=dict(title='Precision'),
                hoverinfo='text',
                hovertext=hovertext,
                showlegend=False
                )


    @property
    def data(self):
        return self.__data
    
    @property
    def layout(self):
        return self.__layout
    
    @property
    def heatmap(self):
        return self.__heatmap
            
    def buildHeatmap(self, id):
        """
        Builds a Heatmap in plotly.go and returns a dash component (dcc.Graph)\n
        All Heatmap data and details are given in the class HeatmapBuild's initialization

        :param id: id of the to-be built graph
        :type id: str
        :return: A Dash Graph component containing the heatmap.
        """
        print(self.data.columns.tolist())
        figure = go.Figure(
                data=[self.heatmap], layout=self.layout
            )
        return dcc.Graph(id=id, figure=figure)