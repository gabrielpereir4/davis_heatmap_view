
EM DEV:
    - Escolha do gráfico (FEITO!)
    - Ajustar filtros para WxA e AxM (FEITO!)
    - Adicionar funcionalidade dos filtros (FEITO!)
    - QUESTÃO: Transposição dos gráficos está do melhor jeito...?

    Nome dele agora é DAVis!

NOTAS:
    - Filtros
        Usar data handler
        Como controlar para onde os dados do filtro vão (para o caso do gráfico estar transposto?)
            - Quando os gráficos são transpostos, o índice se atualiza de acordo. Logo, na transposição, basta aplicar o filtro X em Y e vice versa.

    16/12
    Refazendo e organizando código. criando uma classe DataController como ponto central de controle da aplicação, que se comunica com todas as classes e com o main.py (aplicação)
    - FilterBuilder completo
    - PROXIMOS PASSOS: Adaptar criação do Heatmap. Desvincilhar a classe data handler.
    - REIMPLEMENTAÇÃO FEITA!


    18/12
    - Implementar ordem ascendente, descendente
    - Ranking melhores modelos?
    - Limitador de modelos?
    
            


,
                    '''
                    html.Label('Attributes (Z)'),
                    dcc.Checklist(
                        id='Z-filter',
                        options=[{'label': attribute, 'value': attribute} for attribute in attributes],
                        value=attributes,
                        inline=True,
                    ),
                    '''