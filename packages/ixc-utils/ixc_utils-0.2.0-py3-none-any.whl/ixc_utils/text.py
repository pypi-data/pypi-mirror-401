"""
Módulo para manipulação de texto
"""

import re


def limpar_prefixo_filial(plano):
    """
    Remove prefixo numérico de filial dos nomes de planos.
    
    Args:
        plano (str): Nome do plano com possível prefixo de filial
        
    Returns:
        str: Nome do plano limpo, em maiúsculas e sem espaços extras
        
    Example:
        >>> limpar_prefixo_filial("01 Plano Básico")
        'PLANO BÁSICO'
    """
    plano_limpo = re.sub(r'^[0-9]+\s+', '', plano)
    plano_limpo = plano_limpo.upper().strip()
    return plano_limpo


def limpar_endereco(text):
    """
    Remove caracteres especiais de endereços, mantendo apenas letras e espaços.
    
    Args:
        text (str): Texto do endereço a ser limpo
        
    Returns:
        str: Endereço limpo, formatado em Title Case
        
    Example:
        >>> limpar_endereco("Rua ABC, 123 - Apto. 45")
        'Rua Abc Apto'
    """
    cleaned_text = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', text)
    formatted_text = ' '.join(cleaned_text.split()).title()
    return formatted_text


def substituir_nulos(valor, padrao):
    """
    Substitui valores vazios ou em branco por um valor padrão.
    
    Args:
        valor: Valor a ser verificado
        padrao: Valor padrão a retornar se o valor estiver vazio
        
    Returns:
        O valor original se não estiver vazio, ou o padrão se estiver
        
    Example:
        >>> substituir_nulos("", "N/A")
        'N/A'
        >>> substituir_nulos("Texto", "N/A")
        'Texto'
    """
    return padrao if isinstance(valor, str) and valor.strip() == '' else valor