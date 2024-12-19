from dash import html, dcc

class FilterBuilder:
    """
    Class responsible for Filter building, based on dash HTML and dcc components
    """
    def __init__(self):
        pass

    @staticmethod
    def build_filters_based_on_index(wells, models, attributes):
        """
        Generates filters based on the DataFrame's index provided
        \nReturns:
        filters (html component)
        """
        return html.Div([
            html.Div([
                html.Label('Attributes'),
                dcc.Checklist(
                    id='attributes-filter',
                    options=[{'label': attr, 'value': attr} for attr in attributes],
                    value=attributes,
                    inline=True,
                    style={'max-width': '50%'}
                )
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label('Models'),
                dcc.RangeSlider(
                    min=min(models),
                    max=max(models),
                    value=[min(models), max(models)],
                    step=1,
                    marks={str(model): str(model) for model in models},
                    id='models-filter'
                ),
                html.Div(id='models-output', style={'marginTop': '20px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label('Wells'),
                dcc.Checklist(
                    id='wells-filter',
                    options=[{'label': well, 'value': well} for well in wells],
                    value=wells,
                    inline=True,
                    style={'max-width': '50%'}
                )
            ])
        ])
    
    @staticmethod
    def build_iteration_selector(iteration_count):
        """
        Builds a checklist component for selecting iterations.
        
        \nArgs:
            iteration_count (list): List of available iterations.
            
        \nReturns:
            html.Div: A Dash HTML Div containing a label and checklist for iterations.
        """
        iterations = sorted(iteration_count)

        return html.Div([
            html.Label('Iterations'),
            dcc.Checklist(
                id='iterations-checklist',
                options=[{'label': str(i), 'value': i} for i in iterations],
                value=[iterations[0]] if iterations else [],  # Default: first iteration if exists
                inline=True,
                style={'max-width': '50%', 'display': 'flex'}
            ),
        ],
        )

