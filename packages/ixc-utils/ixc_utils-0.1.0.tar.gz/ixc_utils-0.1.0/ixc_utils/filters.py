"""
Módulo para filtros e manipulação de dados
"""

import json
import re


def grid_param(*filtros):
    """
    Cria parâmetros de filtro para API IXC no formato grid_param.
    
    Args:
        *filtros: Tuplas no formato (tb, op, valor, conector) onde:
            - tb (str): Nome da tabela/campo
            - op (str): Operador (ex: '=', 'LIKE', 'IN', etc)
            - valor (str): Valor para filtrar
            - conector (str): Conector lógico ('AND' ou 'OR')
    
    Returns:
        str: String JSON formatada para uso no grid_param
        
    Example:
        >>> grid_param(
        ...     ('id_cliente', '=', '123', 'AND'),
        ...     ('status', '=', 'ativo', 'AND')
        ... )
    """
    filtros_strings = []
    
    for filtro in filtros:
        tb, op, valor, conector = filtro
        filtro_json = {
            "TB": tb,
            "OP": op,
            "P": valor,
            "C": conector,
            "G": tb
        }
        filtros_strings.append(json.dumps(filtro_json))
    
    resultado = "[" + ", ".join(filtros_strings) + "]"
    return resultado.replace('"', '\\"')


def filtrar_dataframe(dataframe, coluna, padroes_regex, negar=False, flags=re.IGNORECASE):
    """
    Filtra um DataFrame usando expressões regulares.
    
    Args:
        dataframe (pd.DataFrame): DataFrame a ser filtrado
        coluna (str): Nome da coluna para aplicar o filtro
        padroes_regex (str or list): Padrão regex ou lista de padrões
        negar (bool, optional): Se True, inverte o filtro. Padrão: False
        flags (int, optional): Flags do regex. Padrão: re.IGNORECASE
        
    Returns:
        pd.DataFrame: DataFrame filtrado
        
    Example:
        >>> df_filtrado = filtrar_dataframe(df, 'nome', ['João', 'Maria'])
        >>> df_sem_teste = filtrar_dataframe(df, 'status', 'teste', negar=True)
    """
    if isinstance(padroes_regex, list):
        padroes_regex = '|'.join(padroes_regex)
    
    mascara = dataframe[coluna].astype(str).str.contains(
        padroes_regex, 
        flags=flags, 
        regex=True,
        na=False
    )
    
    if negar:
        mascara = ~mascara
    
    return dataframe.loc[mascara]