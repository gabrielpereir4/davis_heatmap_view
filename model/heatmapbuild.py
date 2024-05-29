import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, html, dcc, Input, Output


class HeatmapBuild:
    def __init__(self, data, title='Poços x Modelos', initial_colorscale='turbo', xaxis='Poços', yaxis='Modelos'):
        self.__data = data
        self.__title = title
        self.__initial_colorsscale = initial_colorscale
        self.__xaxis = xaxis
        self.__yaxis = yaxis
        self.__layout = go.Layout(
                title= self.__title,
                xaxis=dict(title= self.__xaxis),
                yaxis=dict(title= self.__yaxis)
            )
        self.__heatmap = go.Heatmap()


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
        return dcc.Graph(
                id= id,
                figure={'data': [self.heatmap], 'layout': self.layout}
            )