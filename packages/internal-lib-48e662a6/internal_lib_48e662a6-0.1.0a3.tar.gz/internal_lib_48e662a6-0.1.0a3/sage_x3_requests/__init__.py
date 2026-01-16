import httpx
import asyncio
from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, SecretStr
from urllib.parse import quote


class SageX3Config(BaseModel):
    base_url: str
    username: str
    password: str
    folder: str
    api_version: str = "api1"
    app: str = "x3"
    env_prefix: str = "erp"
    language: str = "PT"


class SageX3QueryBuilder:
    """Builder para construir queries ao Sage X3"""

    def __init__(self, client: 'SageX3Requester', endpoint: str, representation: str):
        self.client = client
        self.endpoint = endpoint
        self.representation = representation
        self._filter: Optional[str] = None
        self._top: Optional[int] = None
        self._skip: Optional[int] = None
        self._items_per_page: Optional[int] = None
        self._order_by: List[tuple] = []
        self._count: bool = False
        self._fields: List[str] = []

    def filter(self, condition: str) -> 'SageX3QueryBuilder':
        """Adiciona filtro WHERE"""
        self._filter = condition
        return self

    def top(self, n: int) -> 'SageX3QueryBuilder':
        """Limita número de resultados"""
        self._top = n
        return self

    def skip(self, n: int) -> 'SageX3QueryBuilder':
        """Salta N resultados (paginação)"""
        self._skip = n
        return self

    def items_per_page(self, n: int) -> 'SageX3QueryBuilder':
        """Define items por página"""
        self._items_per_page = n
        return self

    def order_by(self, field: str, direction: str = "asc") -> 'SageX3QueryBuilder':
        """Adiciona ordenação"""
        self._order_by.append((field, direction))
        return self

    def count(self, enabled: bool = True) -> 'SageX3QueryBuilder':
        """Retorna apenas contagem"""
        self._count = enabled
        return self

    def select(self, *fields: str) -> 'SageX3QueryBuilder':
        """Seleciona campos específicos"""
        self._fields.extend(fields)
        return self

    def _build_url(self) -> str:
        """Constrói URL completo"""
        config = self.client.config
        base = f"{config.base_url}/{config.api_version}/{config.app}/{config.env_prefix}"
        url = f"{base}/{config.folder}/{self.endpoint}"
        return url

    def _build_params(self) -> Dict[str, Any]:
        """Constrói parâmetros da query"""
        params = {
            "representation": f"{self.representation}.$query"
        }

        if self._filter:
            params["where"] = self._filter

        if self._top:
            params["$top"] = self._top

        if self._skip:
            params["$skip"] = self._skip

        if self._items_per_page:
            params["$itemsPerPage"] = self._items_per_page

        if self._order_by:
            order_parts = [f"{field} {direction}" for field, direction in self._order_by]
            params["$orderby"] = ", ".join(order_parts)

        if self._count is not None and self._count is not False:
            if isinstance(self._count, bool):
                if self._count:
                    params["count"] = 1
            else:
                params["count"] = self._count

        if self._fields:
            params["$select"] = ",".join(self._fields)

        return params

    def execute(self) -> Dict[str, Any]:
        """Executa a query e retorna resposta completa"""
        url = self._build_url()
        params = self._build_params()

        return self.client._execute_request(url, params)

    def execute_raw(self) -> httpx.Response:
        """Executa e retorna resposta raw"""
        url = self._build_url()
        params = self._build_params()

        return self.client._execute_request_raw(url, params)

    def get_resources(self) -> List[Dict[str, Any]]:
        """Executa a query e retorna apenas a lista de $resources"""
        result = self.execute()
        return result.get("$resources", [])

    def get_first(self) -> Optional[Dict[str, Any]]:
        """Executa a query e retorna apenas o primeiro recurso"""
        resources = self.get_resources()
        return resources[0] if resources else None

    def get_count(self) -> int:
        """Retorna o número de itens (usa $itemsPerPage ou conta $resources)"""
        result = self.execute()
        return result.get("$itemsPerPage", len(result.get("$resources", [])))

    def get_all_resources(self, page_size: int = 100, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Executa a query com paginação automática e retorna TODOS os recursos.
        Segue os links $next fornecidos pelo Sage X3 para buscar todas as páginas.

        Args:
            page_size: Número de items por página (padrão: 100)
            max_pages: Limite máximo de páginas a buscar (None = sem limite)

        Returns:
            Lista com todos os recursos de todas as páginas
        """
        all_resources = []
        page_count = 0

        # Guardar configuração original
        original_items_per_page = self._items_per_page
        self._items_per_page = page_size

        try:
            # Buscar primeira página
            result = self.execute()
            resources = result.get("$resources", [])

            if resources:
                all_resources.extend(resources)
                page_count += 1

            # Seguir links $next enquanto existirem
            while "$links" in result and "$next" in result["$links"]:
                # Verificar limite de páginas
                if max_pages and page_count >= max_pages:
                    break

                # Obter URL da próxima página
                next_url = result["$links"]["$next"]["$url"]

                # Fazer pedido direto ao URL fornecido
                if not self.client._client:
                    raise RuntimeError("Client não inicializado")

                response = self.client._client.get(next_url)
                response.raise_for_status()
                result = response.json()

                resources = result.get("$resources", [])
                if not resources:
                    break

                all_resources.extend(resources)
                page_count += 1

            return all_resources

        finally:
            # Restaurar configuração original
            self._items_per_page = original_items_per_page


class SageX3Requester:
    """Cliente para fazer pedidos ao Sage X3 (síncrono)"""

    def __init__(self, config: SageX3Config):
        self.config = config
        self._client: Optional[httpx.Client] = None

    def __enter__(self):
        """Context manager entry"""
        self._client = httpx.Client(
            auth=(self.config.username, self.config.password.get_secret_value()),
            headers={
                "Accept": "application/json",
                "Accept-Language": self.config.language
            },
            timeout=30.0
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self._client:
            self._client.close()

    def request(self, endpoint: str, representation: str) -> SageX3QueryBuilder:
        """Inicia construção de query"""
        return SageX3QueryBuilder(self, endpoint, representation)

    def get_details(self, endpoint: str, representation: str, resource_id: str) -> Dict[str, Any]:
        """
        Obtém detalhes completos de um recurso específico usando a faceta $details.

        Args:
            endpoint: Nome do endpoint (ex: "YEQEV")
            representation: Nome da representação (ex: "YEQEV2")
            resource_id: ID do recurso (ex: "TRA000000002")

        Returns:
            Dicionário com todos os detalhes do recurso

        Example:
            details = client.get_details("YEQEV", "YEQEV2", "TRA000000002")
            print(details["YEQPEVDES"])
        """
        config = self.config
        base = f"{config.base_url}/{config.api_version}/{config.app}/{config.env_prefix}"
        url = f"{base}/{config.folder}/{endpoint}('{resource_id}')"

        params = {
            "representation": f"{representation}.$details"
        }

        return self._execute_request(url, params)

    def _build_url_with_params(self, url: str, params: Dict[str, Any]) -> str:
        """
        Constrói URL com parâmetros sem fazer encoding de aspas simples.
        O Sage X3 não aceita aspas encoded (%27).
        """
        if not params:
            return url

        param_parts = []
        for key, value in params.items():
            # Converter valor para string
            str_value = str(value)

            # Fazer encoding de espaços e caracteres especiais, mas preservar aspas simples
            encoded_value = quote(str_value, safe="'")
            param_parts.append(f"{key}={encoded_value}")

        query_string = "&".join(param_parts)
        return f"{url}?{query_string}"

    def _execute_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Executa pedido HTTP e retorna JSON"""
        if not self._client:
            raise RuntimeError("Client não inicializado. Use 'with SageX3Requester(config) as client:'")

        # Construir URL manualmente para evitar encoding de aspas simples
        url_with_params = self._build_url_with_params(url, params)
        response = self._client.get(url_with_params)
        response.raise_for_status()
        return response.json()

    def _execute_request_raw(self, url: str, params: Dict[str, Any]) -> httpx.Response:
        """Executa pedido HTTP e retorna resposta raw"""
        if not self._client:
            raise RuntimeError("Client não inicializado. Use 'with SageX3Requester(config) as client:'")

        # Construir URL manualmente para evitar encoding de aspas simples
        url_with_params = self._build_url_with_params(url, params)
        response = self._client.get(url_with_params)
        response.raise_for_status()
        return response


class AsyncSageX3QueryBuilder:
    """Builder assíncrono para construir queries ao Sage X3"""

    def __init__(self, client: 'AsyncSageX3Requester', endpoint: str, representation: str):
        self.client = client
        self.endpoint = endpoint
        self.representation = representation
        self._filter: Optional[str] = None
        self._top: Optional[int] = None
        self._skip: Optional[int] = None
        self._items_per_page: Optional[int] = None
        self._order_by: List[tuple] = []
        self._count: bool = False
        self._fields: List[str] = []

    def filter(self, condition: str) -> 'AsyncSageX3QueryBuilder':
        """Adiciona filtro WHERE"""
        self._filter = condition
        return self

    def top(self, n: int) -> 'AsyncSageX3QueryBuilder':
        """Limita número de resultados"""
        self._top = n
        return self

    def skip(self, n: int) -> 'AsyncSageX3QueryBuilder':
        """Salta N resultados (paginação)"""
        self._skip = n
        return self

    def items_per_page(self, n: int) -> 'AsyncSageX3QueryBuilder':
        """Define items por página"""
        self._items_per_page = n
        return self

    def order_by(self, field: str, direction: str = "asc") -> 'AsyncSageX3QueryBuilder':
        """Adiciona ordenação"""
        self._order_by.append((field, direction))
        return self

    def count(self, enabled: bool = True) -> 'AsyncSageX3QueryBuilder':
        """Retorna apenas contagem"""
        self._count = enabled
        return self

    def select(self, *fields: str) -> 'AsyncSageX3QueryBuilder':
        """Seleciona campos específicos"""
        self._fields.extend(fields)
        return self

    def _build_url(self) -> str:
        """Constrói URL completo"""
        config = self.client.config
        base = f"{config.base_url}/{config.api_version}/{config.app}/{config.env_prefix}"
        url = f"{base}/{config.folder}/{self.endpoint}"
        return url

    def _build_params(self) -> Dict[str, Any]:
        """Constrói parâmetros da query"""
        params = {
            "representation": f"{self.representation}.$query"
        }

        if self._filter:
            params["where"] = self._filter

        if self._top:
            params["$top"] = self._top

        if self._skip:
            params["$skip"] = self._skip

        if self._items_per_page:
            params["$itemsPerPage"] = self._items_per_page

        if self._order_by:
            order_parts = [f"{field} {direction}" for field, direction in self._order_by]
            params["$orderby"] = ", ".join(order_parts)

        if self._count:
            params["count"] = 1

        if self._fields:
            params["$select"] = ",".join(self._fields)

        return params

    async def execute(self) -> Dict[str, Any]:
        """Executa a query e retorna resposta completa"""
        url = self._build_url()
        params = self._build_params()

        return await self.client._execute_request(url, params)

    async def get_resources(self) -> List[Dict[str, Any]]:
        """Executa a query e retorna apenas a lista de $resources"""
        result = await self.execute()
        return result.get("$resources", [])

    async def get_first(self) -> Optional[Dict[str, Any]]:
        """Executa a query e retorna apenas o primeiro recurso"""
        resources = await self.get_resources()
        return resources[0] if resources else None

    async def get_count(self) -> int:
        """Retorna o número de itens"""
        result = await self.execute()
        return result.get("$itemsPerPage", len(result.get("$resources", [])))

    async def get_all_resources(self, page_size: int = 100, max_pages: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Executa a query com paginação automática e retorna TODOS os recursos.
        Segue os links $next fornecidos pelo Sage X3.

        Args:
            page_size: Número de items por página (padrão: 100)
            max_pages: Limite máximo de páginas a buscar (None = sem limite)

        Returns:
            Lista com todos os recursos de todas as páginas
        """
        all_resources = []
        page_count = 0

        # Guardar configuração original
        original_items_per_page = self._items_per_page
        self._items_per_page = page_size

        try:
            # Buscar primeira página
            result = await self.execute()
            resources = result.get("$resources", [])

            if resources:
                all_resources.extend(resources)
                page_count += 1

            # Seguir links $next enquanto existirem
            while "$links" in result and "$next" in result["$links"]:
                # Verificar limite de páginas
                if max_pages and page_count >= max_pages:
                    break

                # Obter URL da próxima página
                next_url = result["$links"]["$next"]["$url"]

                # Fazer pedido direto ao URL fornecido
                if not self.client._client:
                    raise RuntimeError("Client não inicializado")

                response = await self.client._client.get(next_url)
                response.raise_for_status()
                result = response.json()

                resources = result.get("$resources", [])
                if not resources:
                    break

                all_resources.extend(resources)
                page_count += 1

            return all_resources

        finally:
            # Restaurar configuração original
            self._items_per_page = original_items_per_page


class AsyncSageX3Requester:
    """Cliente assíncrono para fazer pedidos ao Sage X3 (até 10x mais rápido) 🚀"""

    def __init__(self, config: SageX3Config):
        self.config = config
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Context manager entry"""
        self._client = httpx.AsyncClient(
            auth=(self.config.username, self.config.password.get_secret_value()),
            headers={
                "Accept": "application/json",
                "Accept-Language": self.config.language
            },
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self._client:
            await self._client.aclose()

    def request(self, endpoint: str, representation: str) -> AsyncSageX3QueryBuilder:
        """Inicia construção de query (mesma sintaxe que a versão sync!)"""
        return AsyncSageX3QueryBuilder(self, endpoint, representation)

    def _build_url_with_params(self, url: str, params: Dict[str, Any]) -> str:
        """Constrói URL com parâmetros preservando aspas simples"""
        if not params:
            return url

        param_parts = []
        for key, value in params.items():
            str_value = str(value)
            encoded_value = quote(str_value, safe="'")
            param_parts.append(f"{key}={encoded_value}")

        query_string = "&".join(param_parts)
        return f"{url}?{query_string}"

    async def _execute_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Executa pedido HTTP assíncrono e retorna JSON"""
        if not self._client:
            raise RuntimeError("Client não inicializado")

        url_with_params = self._build_url_with_params(url, params)
        response = await self._client.get(url_with_params)
        response.raise_for_status()
        return response.json()

    async def get_details(self, endpoint: str, representation: str, resource_id: str) -> Dict[str, Any]:
        """
        Obtém detalhes de um recurso específico (assíncrono).

        Example:
            details = await client.get_details("YEQEV", "YEQEV2", "TRA000000002")
        """
        if not self._client:
            raise RuntimeError("Client não inicializado")

        config = self.config
        base = f"{config.base_url}/{config.api_version}/{config.app}/{config.env_prefix}"
        url = f"{base}/{config.folder}/{endpoint}('{resource_id}')"

        params = {"representation": f"{representation}.$details"}
        url_with_params = self._build_url_with_params(url, params)

        response = await self._client.get(url_with_params)
        response.raise_for_status()
        return response.json()

    async def get_multiple_details(
            self,
            endpoint: str,
            representation: str,
            resource_ids: List[str],
            concurrent_requests: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Busca detalhes de múltiplos recursos em paralelo (MUITO RÁPIDO! 🚀).

        Args:
            endpoint: Nome do endpoint
            representation: Nome da representação
            resource_ids: Lista de IDs para buscar
            concurrent_requests: Número de pedidos simultâneos (padrão: 10)

        Returns:
            Lista com detalhes de todos os recursos

        Example:
            ids = ["TRA000000001", "TRA000000002", "TRA000000003"]
            details = await client.get_multiple_details("YEQEV", "YEQEV2", ids)
        """
        semaphore = asyncio.Semaphore(concurrent_requests)

        async def fetch_one(resource_id: str):
            async with semaphore:
                return await self.get_details(endpoint, representation, resource_id)

        tasks = [fetch_one(rid) for rid in resource_ids]
        return await asyncio.gather(*tasks)
