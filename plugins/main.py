import base64
import os

from webviz_config import WebvizPluginABC
from dash import html, dcc, Input, Output, State
import plotly.express as px

from plugins.model.heatmap_data_formatter import HeatmapDataMode
from plugins.model.utilitary import Utilitary

from plugins.controller.data_controller import DataController, DataControllerState


class Heatmap(WebvizPluginABC):
    """
    Heatmap plugin built by webviz project.yaml
    """
    def __init__(self, app):
        self.controller = DataController() # Controller instance
        self.color_scales = px.colors.named_colorscales() # Default colorscales already present in plotly
        super().__init__()
        self.set_callbacks(app)


    @property
    def layout(self):
        """
        Default class responsible for generating HTML layout
        """
        return html.Div([
                dcc.Store(id='uploaded-data', storage_type='memory'),
                html.Div([
                    html.Div([
                        html.H5("Upload file"),
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div(['Drag or ', html.A('select a file')]),
                            style={
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px auto'
                            },
                            multiple=False  # Permite apenas um arquivo
                        ),
                        html.Div(id='file-upload-status', style={'marginTop': '10px', 'color': 'green'})
                    ],
                    style={'display': 'flex', 'justify-content': 'center', 'flex-direction': 'column', 
                    'align-items': 'center'}),
                html.H1("DAVis"),
                
                html.Div([
                    dcc.Tabs(id='data-selection', value="WELLS_MODELS", # Initial value: WELLS_MODELS
                            children=[
                            dcc.Tab(label='Models by Wells', value="WELLS_MODELS"),
                            dcc.Tab(label='Attributes by Models', value="ATTRIBUTES_MODELS"),
                            dcc.Tab(label='Wells by Attributes', value="WELLS_ATTRIBUTES")
                        ],)
                ],
                style={'display': 'flex', 'justify-content': 'center'}),
                html.P('Color Selection'),
                dcc.Dropdown(
                id='color-scale-dropdown',
                options=[{'label': scale, 'value': scale} for scale in self.color_scales],
                value="bluered",
                style={'width': '200px'}
                ),

                html.Div([
                    self.controller.build_filters()
                    ],
                    id='filters-container',
                    style={'width': '100%', 'display': 'flex',
                    'justify-content': 'center', 'flex-direction': 'column', 
                    'align-items': 'center'}),

                html.Div([
                    self.controller.build_iteration_selector()
                    ],
                    id='iterations-container',
                    style={'display': 'flex', 'margin-top': '16px'}),
                html.Div([
                    dcc.RadioItems(
                        id='mode-selector',
                        options=[
                            {'label': 'MAX', 'value': "MAX"},
                            {'label': 'AVERAGE', 'value': "AVG"},
                            {'label': 'MIN', 'value': "MIN"}                       
                        ],
                        value="MAX"  # Initial value: MAX
                    ),
                    dcc.RadioItems(
                        id='ordering-selector',
                        options=[
                            {'label': 'DEFAULT', 'value': 'default'},
                            {'label': 'ASCENDING', 'value': 'ascend'},
                            {'label': 'DESCENDING', 'value': 'descend'}                          
                        ],
                        value='default'  # Initial value: DEFAULT
                    )
                ], style={'display': 'flex', 'flex-direction': 'row', 'margin-top': '16px'}),
                html.Div(
                    id='graph-container',
                    style={'display': 'flex'}
                ),
                html.Div([
                    html.Button("Invert Axis", id='axis-inversion', n_clicks=0)],
                    style={'margin-bottom': '20px'}
                ),
            ], style={'display': 'flex', 'justify-content': 'center', 'flex-direction': 'column', 'align-items': 'center'}),
        ], style={'height': '100vh'})
     
    def set_callbacks(self, app):
        @app.callback(
        [Output('file-upload-status', 'children'),
        Output('uploaded-data', 'data')],  # Saída de status do upload
        Input('upload-data', 'contents'),          # Input: conteúdo do arquivo
        State('upload-data', 'filename')           # Estado: nome do arquivo
        )
        def upload_file(contents, filename):
            if contents is None:
                return "No file uploaded.", None
            print(f"[{self.__class__.__name__}] [UPLOAD_FILE]: Callback received")
            try:
                temp_dir = "/tmp"
                os.makedirs(temp_dir, exist_ok=True)

                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)

                # Caminho temporário para salvar o arquivo
                temp_path = f"/tmp/{filename}"
                with open(temp_path, 'wb') as temp_file:
                    temp_file.write(decoded)

                # Atualiza o DataLoader chamando `get_data_from_file`
                self.controller.load_uploaded_data(temp_path)

                print(f"[{self.__class__.__name__}] [UPLOAD_FILE]: File '{filename}' loaded into DataLoader")
                return f"File '{filename}' successfully uploaded!", True

            except Exception as e:
                print(f"[{self.__class__.__name__}] [UPLOAD_FILE]: Error while uploading file '{filename}: {str(e)}'")
                return f"Error while uploading file: {str(e)}", False


        @app.callback(
        Output('graph-container', 'children'),
        [Input('uploaded-data', 'data'),  # Adiciona o estado dos dados como dependência
        Input('iterations-checklist', 'value'),
        Input('color-scale-dropdown', 'value'),
        Input('axis-inversion', 'n_clicks'),
        Input('data-selection', 'value'),
        Input('wells-filter', 'value'),
        Input('models-filter', 'value'),
        Input('attributes-filter', 'value'),
        Input('mode-selector', 'value'),
        Input('ordering-selector', 'value')]
        )
        def update_figure(data_loaded, iterations, colorscale, axisinvertclicks, heatmap_selection, wells_filter, models_filter, attributes_filter, graphmode, order):
            """
            Callback responsible for generating heatmap(s) and updating the figure based on filter update accordingly
            """
            if not data_loaded or self.controller.get_state() in [DataControllerState.LOADING, DataControllerState.NULL]:
                return html.Div("No data loaded. Please upload a file.", style={'color': 'red'})
            
            print(f"[{self.__class__.__name__}] [UPDATE_FIGURE]: Callback received")
            print(f"[{self.__class__.__name__}] [UPDATE_FIGURE]: Iterations list: {iterations}")

            # Converts selection to enum type
            heatmap_selection_enum = DataControllerState[heatmap_selection]
            heatmap_mode_enum = HeatmapDataMode[graphmode]

            transposed = False
            if axisinvertclicks % 2 != 0:
                transposed = True

            # Builds filter map
            filters = {
                "Wells": sorted(wells_filter, key=Utilitary.natural_sort_key), # Special key for sorting strings like PROD10 and PROD2 correctly
                "Models": sorted(models_filter),
                "Attributes": sorted(attributes_filter)
            }

            # Debug: print the filters dictionary
            print(f"[{self.__class__.__name__}] [UPDATE_FIGURE]: Filters dictionary: {filters}")

            graphs = []
         
            # Builds a heatmap for each iteration selected
            for i in iterations:
                print(f'[{self.__class__.__name__}] [UPDATE_FIGURE]: Building iteration: {i}')
                new_heatmap = self.controller.build_heatmap(heatmap_selection_enum, i, heatmap_mode_enum, filters, colorscale, order, transposed)
                graphs.append(new_heatmap)

            return graphs
            
        @app.callback(
            Output('models-output', 'children'),
            Input('models-filter', 'value')
        )
        def update_slider_output(value):
            """
            Updates label containing current Model selection
            """
            print(f"[{self.__class__.__name__}] [UPDATE_SLIDER_OUTPUT]: Callback received")
            return f"Models: {value[0]} to {value[1]}"
        

        @app.callback(
            [Output('filters-container', 'children'),
            Output('iterations-container', 'children')],
            [Input('uploaded-data', 'data')]
        )
        def update_filters_and_iterations(data_loaded):
            """
            Callback responsible for updating the dynamically generated filters and iteration selector
            """
            print(f"[{self.__class__.__name__}] [UPDATE_FILTERS_AND_ITERATIONS]: Callback received")
            # If controller is not ready or there is no data loaded, stops
            if not data_loaded or self.controller.get_state() != DataControllerState.READY:
                return html.Div("Please upload data first.", style={'color': 'red'}), None

            # Builds filters dynamically
            filters = self.controller.build_filters()
            iterations = self.controller.build_iteration_selector()
            print(f"[{self.__class__.__name__}] [UPDATE_FILTERS_AND_ITERATIONS]: Filters and iterations built successfully")
            return filters, iterations
