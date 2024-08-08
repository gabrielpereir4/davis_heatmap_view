import pandas as pd

# Class dedicated to manipulating and handling data from the heatmap's DF.

class DataHandler:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Iteracao', 'Numero_Modelo', 'Atributo', 'Nome_Poco', 'Valor'])
        self.currentdata = None

    def TransposeData(self):
        '''
        Transposes Pandas dataframe and applies respective filter, without altering the local stored dataframe
        '''
        transposed_df = self.currentdata.transpose()
        self.currentdata = transposed_df
        return transposed_df
    
    def SampleData(self):
        with open('C:\\Code\\Studies\\IC\\webviz_nqdsheatmap\\model\\sample.txt', 'r') as file:
            lines = file.readlines()
        lines = lines[3:]
        for line in lines:
            parts = line.split(';')
            iteracao = parts[0]
            numero_modelo = int(parts[1][4:])
            nqds_parts = parts[2].split()
            atributo = nqds_parts[1]
            nome_poco = nqds_parts[3]
            valor = float(parts[3])
            
            self.data.loc[len(self.data)] = [iteracao, numero_modelo, atributo, nome_poco, valor]
        return self.data
    
    def WellsModels(self):
        df_teste = self.data.groupby(['Nome_Poco', 'Numero_Modelo'])['Valor'].max().reset_index()
        df_mean = df_teste.pivot(index='Nome_Poco', columns='Numero_Modelo', values='Valor')
        #print(df_mean)
        self.currentdata = df_mean
        return df_mean
    
    def AttributesModels(self):
        #print(self.data)
        df_teste = self.data.groupby(['Atributo', 'Numero_Modelo'])['Valor'].max().reset_index()
        #print(df_teste)
        df_mean = df_teste.pivot(index='Atributo', columns='Numero_Modelo', values='Valor')
        #print(df_mean)
        self.currentdata = df_mean
        return df_mean
    
    def WellsAttributes(self):
        #print(self.data)
        df_teste = self.data.groupby(['Nome_Poco', 'Atributo'])['Valor'].max().reset_index()
        #print(df_teste)
        df_mean = df_teste.pivot(index='Nome_Poco', columns='Atributo', values='Valor')
        #print(df_mean)
        self.currentdata = df_mean
        return df_mean
    
    def HoverText(self):
        hovertext = []
        data = self.currentdata
        for yi, yy in enumerate(data.index):
                hovertext.append([])
                for xi, xx in enumerate(data.columns):
                    hovertext[-1].append(f"Poço: {yy}<br>Modelo: {xx}<br>Value: {data.iloc[yi, xi]}")
        return hovertext
    
    def FilterDF(self):
        '''
        Filter Dataframe by index and columns
        '''
        print(self.data)
        remodel_df = self.data.pivot(index='Nome_Poco', columns='Numero_Modelo', values='Valor')
        print(remodel_df)
