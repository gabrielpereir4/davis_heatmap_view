import pandas as pd
import numpy as np

class RandomData:
    def __init__(self, rows, cols):
        self.rowcount = rows
        self.colcount = cols
        self.data = np.random.rand(rows, cols)
        self.df = pd.DataFrame(self.data, columns=[x for x in range(0, cols)], index=[x for x in range(0, rows)])
