"""
Módulo para requisições à API IXC
"""

import json
import time
import requests
import pandas as pd
from pandas import json_normalize
from concurrent.futures import ThreadPoolExecutor, as_completed


_API_URL = None
_API_KEY = None


def configure(api_url, api_key):
    """
    Configura as credenciais da API IXC globalmente.
    
    Após chamar esta função, você não precisa passar api_url e api_key
    em cada requisição.
    
    Args:
        api_url (str): URL base da API IXC
        api_key (str): Chave de autorização da API
        
    Example:
        >>> from ixc_utils import configure
        >>> configure(
        ...     api_url="https://sua-api.ixcsoft.com.br/webservice/v1",
        ...     api_key="sua-chave-api"
        ... )
        >>> # Agora pode usar as funções sem passar api_url e api_key
        >>> df = requisicao_ixc("cliente")
    """
    global _API_URL, _API_KEY
    _API_URL = api_url
    _API_KEY = api_key


def mapeamento(rota, id, traducao, api_url=None, api_key=None):
    """
    Cria um dicionário de mapeamento a partir de uma rota da API IXC.
    
    Args:
        rota (str): Rota da API IXC
        id (str): Campo que será usado como chave do dicionário
        traducao (str): Campo que será usado como valor do dicionário
        api_url (str, optional): URL base da API IXC. Se None, usa o valor configurado.
        api_key (str, optional): Chave de autorização da API. Se None, usa o valor configurado.
        
    Returns:
        dict: Dicionário com o mapeamento id -> traducao
    """
    api_url = api_url or _API_URL
    api_key = api_key or _API_KEY
    
    if api_url is None or api_key is None:
        raise ValueError(
            "api_url e api_key são obrigatórios. "
            "Use configure(api_url, api_key) ou passe como parâmetros."
        )
    
    url = f'{api_url}/{rota}'
    
    payload = json.dumps({
        'qtype': '',
        'query': '',
        'oper': '',
        'page': '1',
        'rp': '999999'
    })
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': api_key,
        'ixcsoft': 'listar'
    }
    
    response = requests.request('POST', url, headers=headers, data=payload)
    
    df_mapping = pd.json_normalize(response.json()['registros'])
    df_mapping[f'{traducao}'] = df_mapping[f'{traducao}'].str.upper()
    df_mapping = df_mapping.set_index(f'{id}')[f'{traducao}'].to_dict()
    
    return df_mapping


def requisicao_ixc(rota, query='[]', api_url=None, api_key=None):
    """
    Faz uma requisição genérica à API IXC.
    
    Args:
        rota (str): Rota da API IXC
        query (str, optional): Parâmetros de filtro em formato JSON. Padrão: '[]'
        api_url (str, optional): URL base da API IXC. Se None, usa o valor configurado.
        api_key (str, optional): Chave de autorização da API. Se None, usa o valor configurado.
        
    Returns:
        pd.DataFrame: DataFrame com os registros retornados
    """
    api_url = api_url or _API_URL
    api_key = api_key or _API_KEY
    
    if api_url is None or api_key is None:
        raise ValueError(
            "api_url e api_key são obrigatórios. "
            "Use configure(api_url, api_key) ou passe como parâmetros."
        )
    
    url = f'{api_url}/{rota}'
    
    payload = json.dumps({
        'qtype': '',
        'query': '',
        'oper': '',
        'page': '1',
        'rp': '999999',
        'grid_param': f'{query}'
    })
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': api_key,
        'ixcsoft': 'listar'
    }
    
    response = requests.request('POST', url, headers=headers, data=payload)
    
    df = pd.json_normalize(response.json()['registros'])
    
    return df


def requisicao_ixc_especifica(rota, ids, tabela, query='[]', max_workers=30, 
                               estrategia=None, api_url=None, api_key=None):
    """
    Faz requisições otimizadas à API IXC para IDs específicos.
    
    Esta função automaticamente escolhe entre estratégia 'bulk' ou 'lotes'
    baseado na quantidade de IDs solicitados vs total de registros.
    
    Args:
        rota (str): Rota da API IXC
        ids (list, str, int): ID(s) para buscar
        tabela (str): Nome da tabela/campo para filtro
        query (str, optional): Parâmetros adicionais de filtro. Padrão: '[]'
        max_workers (int, optional): Número de threads para requisições paralelas. Padrão: 30
        estrategia (str, optional): Forçar estratégia 'bulk' ou 'lotes'. Padrão: None (automático)
        api_url (str, optional): URL base da API IXC. Se None, usa o valor configurado.
        api_key (str, optional): Chave de autorização da API. Se None, usa o valor configurado.
        
    Returns:
        pd.DataFrame: DataFrame com os registros encontrados
    """
    api_url = api_url or _API_URL
    api_key = api_key or _API_KEY
    
    if api_url is None or api_key is None:
        raise ValueError(
            "api_url e api_key são obrigatórios. "
            "Use configure(api_url, api_key) ou passe como parâmetros."
        )
    
    inicio = time.time()
    if isinstance(ids, str):
        ids = [ids]
    elif isinstance(ids, int):
        ids = [str(ids)]
    else:
        ids = list(map(str, ids))
    
    ids_unicos = list(set(ids))
    
    def analisar_tabela():
        url = f'{api_url}/{rota}'
        payload = json.dumps({
            'qtype': tabela,
            'query': '',
            'oper': 'LIKE',
            'page': '1',
            'rp': '1',
            'grid_param': f'{query}'
        })
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': api_key,
            'ixcsoft': 'listar'
        }
        
        try:
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return int(data.get('total', 0))
        except:
            pass
        return None

    def executar_bulk():
        url = f'{api_url}/{rota}'
        payload = json.dumps({
            'qtype': tabela,
            'query': '',
            'oper': 'LIKE',
            'page': '1',
            'rp': '999999',
            'grid_param': f'{query}'
        })
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': api_key,
            'ixcsoft': 'listar'
        }
        
        try:
            response = requests.post(url, headers=headers, data=payload, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                registros = data.get("registros", [])
                
                ids_set = set(map(str, ids_unicos))
                registros_filtrados = [
                    reg for reg in registros 
                    if str(reg.get('id', '')) in ids_set
                ]
                
                tempo_total = time.time() - inicio
                print(f"Bulk: {len(registros_filtrados)} registros em {tempo_total:.1f}s na Rota: {rota}")
                
                return json_normalize(registros_filtrados)
        except Exception as e:
            print(f"Erro bulk: {e}")
        
        return json_normalize([])

    def executar_lotes():
        batch_size = 200
        lotes = [ids_unicos[i:i + batch_size] for i in range(0, len(ids_unicos), batch_size)]
        
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': api_key,
            'ixcsoft': 'listar',
            'Connection': 'keep-alive'
        })
        session.mount('https://', requests.adapters.HTTPAdapter(
            pool_connections=20,
            pool_maxsize=40
        ))
        
        def processar_lote(batch_info):
            lote_num, ids_lote = batch_info
            ids_str = ','.join(map(str, ids_lote))
            url = f'{api_url}/{rota}'
            payload = json.dumps({
                'qtype': tabela,
                'query': f'{ids_str}',
                'oper': 'IN',
                'page': '1',
                'rp': '999999',
                'grid_param': f'{query}'
            })
            
            try:
                response = session.post(url, data=payload, timeout=45)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("registros", [])
            except:
                pass
            return []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            batch_infos = [(i, lote) for i, lote in enumerate(lotes)]
            futures = [executor.submit(processar_lote, batch_info) for batch_info in batch_infos]
            all_results = []
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    all_results.extend(result)
        
        session.close()
        
        tempo_total = time.time() - inicio
        print(f"Lotes: {len(all_results)} registros em {tempo_total:.1f}s para a Rota: {rota}")
        
        return json_normalize(all_results)
    
    # Lógica de decisão
    if estrategia == 'bulk':
        return executar_bulk()
    elif estrategia == 'lotes':
        return executar_lotes()
    else:
        total_registros = analisar_tabela()
        
        if total_registros:
            razao_solicitada = len(ids_unicos) / total_registros
            
            if razao_solicitada > 0.05 and total_registros < 200000:
                return executar_bulk()
            else:
                return executar_lotes()
        else:
            return executar_lotes()