# IXC Utils

Biblioteca Python com funções utilitárias para trabalhar com a API IXC Soft e manipulação de dados relacionados.

## Instalação

```bash
pip install ixc-utils
```

## Funcionalidades

### Requisições à API IXC

- `requisicao_ixc()` - Requisição genérica à API
- `requisicao_ixc_especifica()` - Requisição otimizada para IDs específicos
- `mapeamento()` - Cria dicionários de mapeamento a partir da API

### Filtros e Manipulação de Dados

- `grid_param()` - Cria filtros no formato da API IXC
- `filtrar_dataframe()` - Filtra DataFrames usando regex

### Processamento de Texto

- `limpar_prefixo_filial()` - Remove prefixos de filial
- `limpar_endereco()` - Limpa e formata endereços
- `substituir_nulos()` - Substitui valores vazios

### Processamento de Dados

- `get_firstpay()` - Obtém primeiro pagamento de parcelas recorrentes

## Uso Básico

### Requisições à API

```python
from ixc_utils import configure, requisicao_ixc, mapeamento

# Configurar credenciais
configure(
    api_url="https://SEU_DOMINIO/webservice/v1",
    api_key="sua-chave-api"
)

# Fazer uma requisição simples
df = requisicao_ixc(
    rota="cliente"
)

# Criar mapeamento
clientes_map = mapeamento(
    rota="cliente",
    id="id",
    traducao="nome"
)
```

### Requisições Otimizadas

```python
from ixc_utils import requisicao_ixc_especifica

# Buscar contratos específicos por IDs
ids = [1, 2, 3, 4, 5]
df = requisicao_ixc_especifica(
    rota="cliente_contrato",
    ids=ids,
    tabela="id"
)
```

### Criando Filtros

```python
from ixc_utils import grid_param

# Criar filtro complexo
filtro = grid_param(
    ('id_cliente', '=', '123', 'AND'),
    ('status', '=', 'A', 'AND')
)

# Usar o filtro na requisição
df = requisicao_ixc(
    rota="cliente_contrato",
    query=filtro
)
```

### Filtrar DataFrame

```python
from ixc_utils import filtrar_dataframe

# Filtrar por padrão
df_filtrado = filtrar_dataframe(
    df, 
    coluna='nome', 
    padroes_regex=['João', 'Maria']
)

# Filtrar excluindo padrão
df_sem_teste = filtrar_dataframe(
    df, 
    coluna='status', 
    padroes_regex='teste', 
    negar=True
)
```

### Manipulação de Texto

```python
from ixc_utils import limpar_prefixo_filial, limpar_endereco, substituir_nulos

# Limpar prefixo de filial
plano = limpar_prefixo_filial("01 Plano Fibra 500MB")
# Resultado: "PLANO FIBRA 500MB"

# Limpar endereço
endereco = limpar_endereco("Rua ABC, 123 - Apto. 45")
# Resultado: "Rua Abc Apto"

# Substituir valores vazios
valor = substituir_nulos("", "N/A")
# Resultado: "N/A"
```

### Processamento de Pagamentos

```python
from ixc_utils import get_firstpay

# Obter primeiro pagamento por cliente
primeiro_pag = df.groupby('id_cliente').apply(get_firstpay)
```

## Requisitos

- Python >= 3.8
- pandas >= 1.5.0
- requests >= 2.28.0
- numpy >= 1.23.0

## Licença

MIT License

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Autor

César Bragança - cesarbgf.contato@gmail.com

## Links

- [Repositório GitHub](https://github.com/cesarbgf/ixc-utils)
- [PyPI](https://pypi.org/cesarbgf/ixc-utils/)