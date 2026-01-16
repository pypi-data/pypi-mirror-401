# Sage X3 Requests Wrapper (ALPHA)

> ⚠️ **AVISO: BIBLIOTECA EM DESENVOLVIMENTO (ALPHA)** ⚠️
>
> Esta biblioteca foi publicada para uso pessoal e testes. **Não é recomendada para produção.**
> A API pode mudar drasticamente a qualquer momento sem aviso prévio. Use por sua conta e risco.

## Instalação

```bash
pip install internal-lib-48e662a6
```

## Exemplos de Uso

### Configuração
```python
from sage_x3_requests import SageX3Config, SageX3Requester

config = SageX3Config(
    base_url="https://seu-erp.com",
    username="admin",
    password="password",
    folder="SEED"
)
```

### Pedir 5 Registos (Limit)
Use `.count(5)` ou `.top(5)` para limitar o número de resultados retornados.

```python
with SageX3Requester(config) as client:
    # Opção 1: Usando count (recomendado se a sua API usa count para limite)
    registos = client.request("CLIENTES", "BPC") \
                     .count(5) \
                     .execute()
    
    # Opção 2: Usando top (padrão OData/Syracuse)
    registos = client.request("CLIENTES", "BPC") \
                     .top(5) \
                     .execute()
```

### Pedir TODOS os Registos (Paginação Automática)
Use `.get_all_resources()` para buscar todos os dados, percorrendo todas as páginas automaticamente.

```python
with SageX3Requester(config) as client:
    # Busca todos os clientes (cuidado com grandes volumes de dados!)
    todos_clientes = client.request("CLIENTES", "BPC") \
                           .get_all_resources()
                           
    print(f"Total encontrado: {len(todos_clientes)}")
```

### Contagem Total
Para saber quantos registos existem sem trazer os dados:

```python
with SageX3Requester(config) as client:
    query = client.request("CLIENTES", "BPC").count(True).execute()
    total = query.get("count") # ou verificar estrutura de retorno
```
