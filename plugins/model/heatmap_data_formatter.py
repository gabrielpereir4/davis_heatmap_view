from enum import Enum, auto


class HeatmapDataMode(Enum):
    """
    Enum representing the display mode of the heatmap.
    """
    AVG = auto() # AVERAGE
    MIN = auto() # MINIMUM
    MAX = auto() # MAXIMUM


class HeatmapDataFormatter():
    """
    Class responsible for formatting heatmap data based on heatmap type and mode.
    """
    def __init__(self):
        pass

    @staticmethod
    def wells_models(data, mode):
        """
        Returns Wells by Models dataframe based on provided data
        \nArgs:
        data (DataFrame): provided data to be formatted
        """
        print('[HEATMAP_FORMATTER] Wells x Models')
        HeatmapDataFormatter.check_mode(mode)
        print(f'[HEATMAP_FORMATTER] Heatmap Mode: {mode}')
        
        data['NQDS_Value'] = data['NQDS_Value'].abs()
        final_df = None

        if mode is HeatmapDataMode.AVG:
            final_df = data.groupby(['Wells', 'Models'])['NQDS_Value'].mean().reset_index()

        # MIN view
        elif mode is HeatmapDataMode.MIN:
            final_df = data.groupby(['Wells', 'Models'])['NQDS_Value'].min().reset_index()

        # MAX view
        elif mode is HeatmapDataMode.MAX:
            final_df = data.groupby(['Wells', 'Models'])['NQDS_Value'].max().reset_index()

        pivot_df = final_df.pivot(index='Wells', columns='Models', values='NQDS_Value')
        return pivot_df
    
    @staticmethod
    def wells_attributes(data, mode):
        """
        Returns Wells by Attributes dataframe based on provided data
        \nArgs:
        data (DataFrame): provided data to be formatted
        """
        print('[HEATMAP_FORMATTER] Wells x Attributes')
        print(f'[HEATMAP_FORMATTER] Heatmap Mode: {mode}')

        HeatmapDataFormatter.check_mode(mode)
        
        data['NQDS_Value'] = data['NQDS_Value'].abs()
        final_df = None

        if mode is HeatmapDataMode.AVG:
            final_df = data.groupby(['Wells', 'Attributes'])['NQDS_Value'].mean().reset_index()

        # MIN view
        elif mode is HeatmapDataMode.MIN:
            final_df = data.groupby(['Wells', 'Attributes'])['NQDS_Value'].min().reset_index()

        # MAX view
        elif mode is HeatmapDataMode.MAX:
            final_df = data.groupby(['Wells', 'Attributes'])['NQDS_Value'].max().reset_index()

        pivot_df = final_df.pivot(index='Wells', columns='Attributes', values='NQDS_Value')
        return pivot_df
    

    @staticmethod
    def attributes_models(data, mode):
        """
        Returns Attributes by Models dataframe based on provided data
        \nArgs:
        data (DataFrame): provided data to be formatted
        """
        print('[HEATMAP_FORMATTER] Attributes x Models')
        print(f'[HEATMAP_FORMATTER] Heatmap Mode: {mode}')

        HeatmapDataFormatter.check_mode(mode)
        
        data['NQDS_Value'] = data['NQDS_Value'].abs()
        final_df = None

        if mode is HeatmapDataMode.AVG:
            final_df = data.groupby(['Attributes', 'Models'])['NQDS_Value'].mean().reset_index()

        # MIN view
        elif mode is HeatmapDataMode.MIN:
            final_df = data.groupby(['Attributes', 'Models'])['NQDS_Value'].min().reset_index()

        # MAX view
        elif mode is HeatmapDataMode.MAX:
            final_df = data.groupby(['Attributes', 'Models'])['NQDS_Value'].max().reset_index()

        pivot_df = final_df.pivot(index='Attributes', columns='Models', values='NQDS_Value')
        return pivot_df


    @staticmethod
    def check_mode(mode):
        """
        Validates if mode is an instance of HeatmapDataMode
        """
        if not isinstance(mode, HeatmapDataMode):
            raise ValueError(f"[HeatmapDataFormatter] Invalid state: {mode}. Must be a HeatmapDataMode Enum value.")