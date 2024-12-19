# DAVis (Data Assimilation Visualization) Webviz Plugin

The **DAVis Webviz Plugin** provides a Heatmap view for visualizing Data Assimilation steps in oil reserves exploration. It processes `.txt` files containing preformatted data, delivering an interactive and customizable visualization.

## How to Use

1. Build the plugin:
   ```bash
   webviz build project.yaml

2. After building, upload a data file to the Upload File section, and wait for the plugin to process and return the view. After that,
the view can be completely manipulated, according to the selectors and filters available on the screen.

## Technical Aspects

The project follows an MVC-like architecture, where main.py is a view, and DataController is a controller class for interactions between the main view and model classes (which process and manipulates data as provided). 

**NOTE**: There is a max_models parameter in DataLoader.get_data_from_file() method, which limits the amount of models loaded from the file provided by the user. The default value is set to None, which means the method loads an unlimited number of models. This parameter can be changed to limit this number and avoid performance or loading issues. A suggested improvement would be to allow the user to set this limit dynamically.