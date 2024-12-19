class FilterHandler():
    def __init__(self):
        pass

    @staticmethod
    def apply_filter_to_dataframe(dataframe, filter_map):
        """
        Applies filter map (accordingly) to given dataframe
        \nArgs:
        dataframe (Dataframe): Dataframe containing data
        filter_map (map/dictionary): dictionary as built in main.py containing the filter list as values
        """
        print("[FILTER_HANDLER] Applying filters to DataFrame")

        x_filter = filter_map.get(dataframe.index.name)
        y_filter = filter_map.get(dataframe.columns.name)

        # If any of the axes filters is Models, the list is adapted to include full range

        # Apply filters for index (rows)
        x_filter = FilterHandler.expand_range_if_models(dataframe.index.name, filter_map.get(dataframe.index.name, slice(None)))
        if x_filter != slice(None):  # Apply filter only if it exists
            dataframe = dataframe.loc[x_filter]

        # Apply filters for columns
        y_filter = FilterHandler.expand_range_if_models(dataframe.columns.name, filter_map.get(dataframe.columns.name, slice(None)))
        if y_filter != slice(None):  # Apply filter only if it exists
            dataframe = dataframe.loc[:, y_filter]

        print(f"[{FilterHandler.__name__}] [APPLY_FILTER]: Filters applied successfully")
        print(f"[{FilterHandler.__name__}] [APPLY_FILTER]: Filtered DataFrame shape: {dataframe.shape}")
        return dataframe
    

    @staticmethod
    def apply_ordering_to_dataframe(dataframe, order):
        """
        Applies ascendant or descendant ordering to a dataframe
        \nArgs:
        dataframe (DataFrame): DataFrame to be applied on
        order (str): Ordering mode
        \nReturns:
        a DataFrame with ordering applied, or none applied
        """
        if order == 'ascend':
            print('Ascending')
            ordered_df = dataframe.sort_values(by=dataframe.columns.tolist(), axis=0, ascending=True)
        elif order == 'descend':
            ordered_df = dataframe.sort_values(by=dataframe.columns.tolist(), axis=0, ascending=False)
        else:
            # Default ordering
            ordered_df = dataframe
        print(f"[{FilterHandler.__name__}] [APPLY_ORDERING]: Ordering applied successfully")
        return ordered_df


    @staticmethod
    def expand_range_if_models(key, value):
        """
        Expands the range if the key is 'MODELS' and the value is a two-integer list.
        """
        if key == 'Models' and isinstance(value, list) and len(value) == 2:
            start, end = value
            if isinstance(start, int) and isinstance(end, int):
                return list(range(start, end + 1))  # Generate full range
        return value  # Return value unchanged if conditions are not met