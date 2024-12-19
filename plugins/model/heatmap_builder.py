import plotly.graph_objs as go
from dash import dcc
import numpy as np


class HeatmapBuilder:
    """
    Class for encapsulating Heatmap building
    """
    def __init__(self, data, colorscale='bluered'):
        self.__data = data

        self.__colorscale = colorscale

        self.__title = self._generate_title()
        self.__xaxis = self.__data.index.name
        self.__yaxis = self.__data.columns.name

        x_tickvals, x_ticktext = self._adjust_ticks(self.__data.columns, self.__yaxis)
        y_tickvals, y_ticktext = self._adjust_ticks(self.__data.index, self.__xaxis)

        self.__layout = go.Layout(
                title= self.__title,
                # Building the x and y axis "captions"
                xaxis=dict(title=self.__yaxis, tickvals=x_tickvals, ticktext=x_ticktext),
                yaxis=dict(title=self.__xaxis, tickvals=y_tickvals, ticktext=y_ticktext),
                width=1200,
                height=800,
                margin=dict(l=100, r=100, t=100, b=100),
            )
        self.__heatmap = go.Heatmap(
                z=data,
                colorscale=self.__colorscale,
                colorbar=dict(title='Misfit Value',
                                tickvals=[0, 2, 5, 10, 20],
                                ticktext=['1', '2', '5', '10', '20']),
                zmin=0,  # minimum colorscale value
                zmax=20,  # maximum colorscale value
                hoverinfo='text',
                hovertext=self._build_hovertext()
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


    def _generate_title(self):
        """
        Generates Heatmap Title based on DataFrame's colums and index titles.
        """
        x_axis = self.__data.columns.name
        y_axis = self.__data.index.name
        return f"{y_axis} x {x_axis}"
    
    def _adjust_ticks(self, axis_values, axis_name):
        """
        Adjusts tickvals and ticktext for axes.
        If the axis is named 'Models', it displays a tick every 25 elements.

        Args:
            axis_values (pd.Index or list): The axis values.
            axis_name (str): The name of the axis.

        Returns:
            tuple: Adjusted tickvals and ticktext.
        """
        if axis_name == "Models":
            # Shows multiple of 25 values
            tickvals = [i for i in range(24, len(axis_values), 25)]  # 0-based index
            ticktext = [str(i + 1) for i in tickvals] # Adapts to 1-based index
        else:
            # Shows full values
            tickvals = list(range(len(axis_values)))
            ticktext = axis_values.tolist()

        return tickvals, ticktext


    def _build_hovertext(self):
        """
        Creates a hovertext matrix with cell information.
        """
        index_name = self.__data.index.name[:-1]
        column_name = self.__data.columns.name[:-1]
        hovertext = []
        for i, row in enumerate(self.__data.index):
            hovertext_row = []
            for j, col in enumerate(self.__data.columns):
                value = self.__data.iloc[i, j]
                hovertext_row.append(f"{index_name}: {row}<br>{column_name}: {col}<br>Value: {value:.2f}")
            hovertext.append(hovertext_row)
        return np.array(hovertext)

    def buildHeatmap(self, target_id):
        """
        Builds a Heatmap in plotly.go and returns a dash component (dcc.Graph)\n
        All Heatmap data and details are given in the class HeatmapBuild's initialization

        \nArgs:
        id (str): id of the to-be built graph
        \nReturns:
        A Dash Graph component containing the heatmap.
        """
        figure = go.Figure(
                data=[self.heatmap], layout=self.layout
            )
        return dcc.Graph(id=target_id, figure=figure)
