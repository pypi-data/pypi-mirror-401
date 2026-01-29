"""
Módulo para processamento de dados específicos
"""

import numpy as np


def get_firstpay(group):
    """
    Obtém o valor do primeiro pagamento de um grupo de parcelas recorrentes.
    
    Busca primeiro por parcela número 1, depois por parcelas sem número,
    e retorna NaN se não encontrar nenhuma.
    
    Args:
        group (pd.DataFrame): Grupo de registros com colunas 
                             'numero_parcela_recorrente' e 'valor_recebido'
        
    Returns:
        float: Valor recebido do primeiro pagamento ou NaN
        
    Example:
        >>> df.groupby('id_cliente').apply(get_firstpay)
    """
    # Primeiro tenta pegar parcela = 1
    parcela_1 = group[group['numero_parcela_recorrente'] == "1"]
    if not parcela_1.empty:
        return parcela_1['valor_recebido'].iloc[0]
    
    # Se não tem parcela = 1, pega registros com parcela vazia/nula
    parcela_vazia = group[group['numero_parcela_recorrente'].isna()]
    if not parcela_vazia.empty:
        return parcela_vazia['valor_recebido'].iloc[0]
    
    # Se não tem nem parcela = 1 nem vazia, retorna NaN
    return np.nan