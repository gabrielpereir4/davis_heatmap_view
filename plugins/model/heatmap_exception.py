class HeatmapException(Exception):
    """Exception class for Heatmap-related issues"""
    def __init__(self, mensagem):
        super().__init__(mensagem)  # Passa a mensagem para a classe base Exception
        self.mensagem = mensagem