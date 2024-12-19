from enum import Enum, auto

from plugins.model.data_loader import DataLoader
from plugins.model.heatmap_exception import HeatmapException
from plugins.model.heatmap_data_formatter import HeatmapDataFormatter
from plugins.model.heatmap_builder import HeatmapBuilder
from plugins.model.filter_builder import FilterBuilder
from plugins.model.filter_handler import FilterHandler
from dash import html

class DataControllerState(Enum):
    """
    Enum representing the current state of the DataController.
    """
    NULL = auto()                # Initial state (no data loaded)
    LOADING = auto()             # Transition between heatmaps
    WELLS_MODELS = auto()        # Heatmap: Wells vs Models
    ATTRIBUTES_MODELS = auto()   # Heatmap: Attributes vs Models
    WELLS_ATTRIBUTES = auto()    # Heatmap: Wells vs Attributes
    READY = auto()           # Loaded state (data loaded)

class DataController:
    """
    Controller class, responsible for interacting with the application on main.py and other classes
    """
    initialized = False  # Initialization flag

    def __init__(self):
        self.data_loader = DataLoader()
        self.__current_state = DataControllerState.NULL
        self.initialize()

    def initialize(self, load_sample = False):
        """
        Static block that executes default get data from file
        """
        if not DataController.initialized:
            print(f"[{self.__class__.__name__}] [INITIALIZE]: Static block executed: DataController is being initialized.")
            if load_sample:
                self.data_loader.get_data_from_file('C:\\Code\\Studies\\IC\\webviz_nqdsheatmap\\plugins\\fullsample.txt')
                print(f"[{self.__class__.__name__}] [INITIALIZE]: Sample data loaded successfully.")
                self.set_state(DataControllerState.READY)
            else:
                print(f"[{self.__class__.__name__}] [INITIALIZE]: Controller initialized without sample data.")
                self.set_state(DataControllerState.NULL)
            DataController.initialized = True

    def get_state(self):
        """
        Getter for the current state.
        """
        return self.__current_state

    def set_state(self, new_state):
        """
        Setter to validate and set the state using DataControllerState Enum.
        """
        if not isinstance(new_state, DataControllerState):
            raise ValueError(f"[CONTROLLER] [SET_STATE]: Invalid state: {new_state}. Must be a DataControllerState Enum value.")
        self.__current_state = new_state
        print(f"[{self.__class__.__name__}] [SET_STATE]: State updated to: {self.__current_state.name}")  # Update notification


    def load_uploaded_data(self, filepath):
        """
        Receives a filepath to a data file and processes it in DataLoader
        """
        print(f"[{self.__class__.__name__}] [LOAD_UPLOADED_DATA]: Received uploaded data. Processing...")
        self.set_state(DataControllerState.LOADING)
        self.data_loader.clear_data()
        self.data_loader.get_data_from_file(filepath)
        print(f"[{self.__class__.__name__}] [LOAD_UPLOADED_DATA]: Data successfully processed")
        self.set_state(DataControllerState.READY)


    def build_filters(self):
        """
        Builds Filters' HTML component.
        Ensures that data is loaded before attempting to build filters.
        Returns:
            Filters HTML component or a placeholder message.
        """
        if self.__current_state != DataControllerState.READY:
            print(f"[{self.__class__.__name__}] [BUILD_FILTERS]: Data is not ready. Cannot build filters.")
            return html.Div("Please, upload data first.", style={'color': 'red', 'fontSize': '18px'})

        try:
            wells, models, attributes = self.data_loader.get_indexes()
            return FilterBuilder.build_filters_based_on_index(wells, models, attributes)
        except ValueError as e:
            print(f"[{self.__class__.__name__}] [BUILD_FILTERS]: Error while building filters: " + str(e))
            return html.Div("Error while building filter", style={'color': 'red', 'fontSize': '18px'})
    

    def build_iteration_selector(self):
        """
        Builds Iteration Selector HTML component.
        Ensures that data is loaded before attempting to build the selector.
        Returns:
            Iteration Selector HTML component or a placeholder message.
        """
        if self.__current_state != DataControllerState.READY:
            print(f"[{self.__class__.__name__}] [BUILD_ITERATION_SELECTOR]: Data is not ready. Cannot build iteration selector.")
            return html.Div("Please, upload data first.", style={'color': 'red', 'fontSize': '18px'})

        try:
            iteration_count = self.data_loader.get_iteration_count()
            return FilterBuilder.build_iteration_selector(iteration_count)
        except ValueError as e:
            print(f"[{self.__class__.__name__}] [BUILD_ITERATION_SELECTOR]: Error while building iteration selector: " + str(e))
            return html.Div("Error while building iteration selector", style={'color': 'red', 'fontSize': '18px'})


    def gather_heatmap_data(self, heatmap_type, iteration, heatmap_mode, transposed = False):
        """
        Gathers data according to desired Heatmap type
        \nArgs:
        heatmap_type (DataControllerState): type of desired heatmap (Wells x Models, Models x Attributes, Wells x Atributes)
        iteration (int): desired iteration
        \nReturn:
        DataFrame formatted to according heatmap type
        """
        if self.get_state() is DataControllerState.NULL:
            raise HeatmapException("Gathering data while DataControllerState is NULL")
        
        # Sets LOADING state
        self.set_state(DataControllerState.LOADING)
        data = None

        # Gathers data based on heatmap type selected
        if heatmap_type is DataControllerState.WELLS_MODELS:
            print(f"[{self.__class__.__name__}] [GATHER_HEATMAP_DATA]: Processing Wells X Models")
            data = HeatmapDataFormatter.wells_models(self.data_loader.get_iteration(iteration), heatmap_mode)
            self.set_state(DataControllerState.WELLS_MODELS)

        elif heatmap_type is DataControllerState.ATTRIBUTES_MODELS:
            print(f"[{self.__class__.__name__}] [GATHER_HEATMAP_DATA]: Processing Attributes X Models")
            data = HeatmapDataFormatter.attributes_models(self.data_loader.get_iteration(iteration), heatmap_mode)
            self.set_state(DataControllerState.ATTRIBUTES_MODELS)

        elif heatmap_type is DataControllerState.WELLS_ATTRIBUTES:
            print(f"[{self.__class__.__name__}] [GATHER_HEATMAP_DATA]: Processing Wells X Attributes")
            data = HeatmapDataFormatter.wells_attributes(self.data_loader.get_iteration(iteration), heatmap_mode)
            self.set_state(DataControllerState.WELLS_ATTRIBUTES)
        
        if transposed:
            data = data.transpose()
            print(f"[{self.__class__.__name__}] [GATHER_HEATMAP_DATA]: Transposed")
        return data


    def build_heatmap(self, heatmap_type, iteration, heatmap_mode, filters, colorscale, order, transposed = False):
        """
        Method responsible for Gathering Data, applying filters and retrieving the heatmap HTML component
        \nArgs:
        heatmap_type (DataControllerState): heatmap type based on DataControllerState Enum
        iteration (int): desired iteration
        heatmap_mode (HeatmapDataMode): display mode of the heatmap
        filters (map/dict): dictionary containing current filter state (KEYS: wells, models, attributes)
        \nReturns:
        Heatmap Dash HTML component
        """
        unfiltered_df = self.gather_heatmap_data(heatmap_type, iteration, heatmap_mode, transposed)
        #print(unfiltered_df)
        
        # apply filter
        filtered_df = FilterHandler.apply_filter_to_dataframe(unfiltered_df, filters)

        ordered_df = FilterHandler.apply_ordering_to_dataframe(filtered_df, order)

        # build heatmap html component
        heatmap_builder = HeatmapBuilder(ordered_df, colorscale)
        heatmap_component = heatmap_builder.buildHeatmap(f'heatmap-{iteration}')
        print(f"[{self.__class__.__name__}] [BUILD_HEATMAP]: Heatmap built")
        return heatmap_component