import re

class Utilitary:
    def __init__(self):
        pass
    
    @staticmethod
    def natural_sort_key(value):
        """
        Extracts numeric parts of a string for natural sorting.
        Example: 'PROD10' -> ['PROD', 10]
        """
        return [int(part) if part.isdigit() else part for part in re.split(r'(\d+)', value)]