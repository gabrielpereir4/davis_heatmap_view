import pandas as pd

class DataLoader:
    """
    Handles loading and parsing data from input files.
    \nAttributes:
    data: full DataFrame captured from loading data file
    iterations: (dictionary) DataFrames formatted by iterations
    """
    def __init__(self):
        self.__data = None
        self.__iterations = {}


    def get_data_from_file(self, path, maxmodels = None):
        """
        Method for gathering data from specified path
        \nArgs:
        path (str): Full path to the file.
        maxmodels (int, optional): Maximum number of models to load. Default is None (unlimited).
        """
        with open(path, 'r', encoding='utf-8') as file:
            file_lines = file.readlines()

        # Ignores first 3 lines
        file_lines = file_lines[3:]

        # Formatting
        rows = []
        for line in file_lines:
            new_line = self.format_file_line(line)

            if maxmodels and new_line['Models'] > maxmodels:
                break
            
            rows.append(new_line)

            # Update iterations dictionary
            iteration = new_line['Iteration']
            if iteration in self.__iterations:
                self.__iterations[iteration] = pd.concat(
                    [self.__iterations[iteration], pd.DataFrame([new_line])], 
                    ignore_index=True
                )
            else:
                self.__iterations[iteration] = pd.DataFrame([new_line])

        self.__data = pd.DataFrame(rows)


    def clear_data(self):
        """
        Clears the currently loaded data.
        """
        self.__data = None
        self.__iterations = {}


    @staticmethod
    def format_file_line(line):
        """
        Formats a single line from the data file into a dictionary.
        \nArgs:
            line (str): A single line from the file.
        \nReturns:
            dict: Formatted line as a dictionary.
        """
        separated_line = line.split(';')
        iteration = int(separated_line[0])
        model = int(separated_line[1][4:])

        separated_nqds_field = separated_line[2].split()
        attribute = separated_nqds_field[1]
        well = separated_nqds_field[3]

        nqds_value = float(separated_line[3])

        # Creating new line with gathered data
        return {
        'Iteration': iteration,
        'Models': model,
        'Attributes': attribute,
        'Wells': well,
        'NQDS_Value': nqds_value
        }

    

    def get_iteration(self, iteration = 1):
        """
        Gets DataFrame from respective iteration
        \nArgs:
        iteration (int, default = 1): the number of the desired iteration
        \nReturns:
        DataFrame from respective iteration
        """

        return self.__iterations[iteration]
    
    def get_iteration_count(self):
        """
        Retrieves the total number of iterations loaded in the iterations dictionary.
        \nReturns:
            int: The number of iterations.
        """
        return list(self.__iterations.keys())
    
    
    def get_indexes(self):
        """
        Retrieves all unique attributes, models, and wells from the current data.
        \nReturns:
            wells, models, attributes list
        """
        if self.__data is None:
            raise ValueError("Data has not been loaded yet. Call get_data_from_file() first.")
        
        attributes = self.__data['Attributes'].unique().tolist()
        min_models = self.__data['Models'].min()
        max_models = self.__data['Models'].max()
        models = [min_models, max_models]
        wells = self.__data['Wells'].unique().tolist()
        
        return wells, models, attributes