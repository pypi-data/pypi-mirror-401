"""
ProductConcierge - Classe principal para busca de produtos

Esta é a classe principal que orquestra todo o fluxo de busca,
integrando o cliente VTEX, gerenciador de estoque e plugins.
"""

from typing import Any, Dict, List, Optional, Type
from .client import VTEXClient
from .stock import StockManager
from .context import SearchContext


class PluginBase:
    """
    Classe base para plugins.
    
    Plugins podem implementar os seguintes hooks:
    - before_search: Executado antes da busca (pode modificar contexto)
    - after_search: Executado após a busca (pode modificar produtos)
    - after_stock_check: Executado após verificação de estoque
    - enrich_products: Enriquece produtos com dados adicionais
    """
    
    def before_search(self, context: SearchContext, client: VTEXClient) -> SearchContext:
        """
        Hook executado antes da busca.
        
        Args:
            context: Contexto da busca
            client: Cliente VTEX
            
        Returns:
            Contexto modificado
        """
        return context
    
    def after_search(
        self, 
        products: Dict[str, Dict], 
        context: SearchContext, 
        client: VTEXClient
    ) -> Dict[str, Dict]:
        """
        Hook executado após a busca.
        
        Args:
            products: Produtos encontrados
            context: Contexto da busca
            client: Cliente VTEX
            
        Returns:
            Produtos modificados
        """
        return products
    
    def after_stock_check(
        self,
        products_with_stock: List[Dict],
        context: SearchContext,
        client: VTEXClient
    ) -> List[Dict]:
        """
        Hook executado após verificação de estoque.
        
        Args:
            products_with_stock: Produtos com estoque
            context: Contexto da busca
            client: Cliente VTEX
            
        Returns:
            Produtos modificados
        """
        return products_with_stock
    
    def enrich_products(
        self,
        products: Dict[str, Dict],
        context: SearchContext,
        client: VTEXClient
    ) -> Dict[str, Dict]:
        """
        Hook para enriquecer produtos com dados adicionais.
        
        Args:
            products: Produtos para enriquecer
            context: Contexto da busca
            client: Cliente VTEX
            
        Returns:
            Produtos enriquecidos
        """
        return products
    
    def finalize_result(
        self,
        result: Dict[str, Any],
        context: SearchContext
    ) -> Dict[str, Any]:
        """
        Hook para finalizar o resultado antes de retornar.
        
        Args:
            result: Resultado final
            context: Contexto da busca
            
        Returns:
            Resultado modificado
        """
        return result


class ProductConcierge:
    """
    Classe principal para busca de produtos VTEX.
    
    Orquestra o fluxo completo de busca:
    1. Executa hooks before_search dos plugins
    2. Realiza busca inteligente
    3. Executa hooks after_search dos plugins
    4. Verifica disponibilidade de estoque
    5. Executa hooks after_stock_check dos plugins
    6. Enriquece produtos com plugins
    7. Filtra e formata resultado final
    
    Example:
        from weni_vtex import ProductConcierge
        from weni_vtex.plugins import Regionalization, Wholesale
        
        concierge = ProductConcierge(
            base_url="https://loja.vtexcommercestable.com.br",
            store_url="https://loja.com.br",
            plugins=[Regionalization(), Wholesale()]
        )
        
        result = concierge.search(
            product_name="furadeira",
            postal_code="01310-100"
        )
    """
    
    def __init__(
        self,
        base_url: str,
        store_url: str,
        vtex_app_key: Optional[str] = None,
        vtex_app_token: Optional[str] = None,
        plugins: Optional[List[PluginBase]] = None,
        max_products: int = 20,
        max_variations: int = 5,
        max_payload_kb: int = 20,
        utm_source: Optional[str] = None,
        priority_categories: Optional[List[str]] = None,
    ):
        """
        Inicializa o ProductConcierge.
        
        Args:
            base_url: URL base da API VTEX
            store_url: URL da loja
            vtex_app_key: App Key VTEX (opcional)
            vtex_app_token: App Token VTEX (opcional)
            plugins: Lista de plugins a utilizar
            max_products: Máximo de produtos a retornar
            max_variations: Máximo de variações por produto
            max_payload_kb: Tamanho máximo do payload em KB
            utm_source: UTM source para links
            priority_categories: Categorias com lógica especial de estoque
        """
        self.client = VTEXClient(
            base_url=base_url,
            store_url=store_url,
            vtex_app_key=vtex_app_key,
            vtex_app_token=vtex_app_token
        )
        self.stock_manager = StockManager()
        self.plugins = plugins or []
        
        # Configurações
        self.max_products = max_products
        self.max_variations = max_variations
        self.max_payload_kb = max_payload_kb
        self.utm_source = utm_source
        self.priority_categories = priority_categories or []
    
    def search(
        self,
        product_name: str,
        brand_name: str = "",
        postal_code: Optional[str] = None,
        quantity: int = 1,
        delivery_type: Optional[str] = None,
        credentials: Optional[Dict[str, Any]] = None,
        contact_info: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Executa busca completa de produtos.
        
        Args:
            product_name: Nome do produto a buscar
            brand_name: Marca do produto (opcional)
            postal_code: CEP para regionalização (opcional)
            quantity: Quantidade desejada
            delivery_type: Tipo de entrega (opcional)
            credentials: Credenciais extras para plugins
            contact_info: Informações do contato para plugins
            **kwargs: Parâmetros extras para plugins
            
        Returns:
            Dicionário com produtos encontrados e informações extras
        """
        # 1. Cria contexto de busca
        context = SearchContext(
            product_name=product_name,
            brand_name=brand_name,
            postal_code=postal_code,
            quantity=quantity,
            delivery_type=delivery_type,
            credentials=credentials or {},
            contact_info=contact_info or {},
        )
        
        # Adiciona kwargs extras ao contexto
        for key, value in kwargs.items():
            if hasattr(context, key):
                setattr(context, key, value)
        
        # 2. Executa hooks before_search
        for plugin in self.plugins:
            context = plugin.before_search(context, self.client)
        
        # 3. Realiza busca inteligente
        products = self.client.intelligent_search(
            product_name=context.product_name,
            brand_name=context.brand_name,
            region_id=context.region_id,
            max_products=self.max_products,
            max_variations=self.max_variations,
            utm_source=self.utm_source
        )
        
        # 4. Executa hooks after_search
        for plugin in self.plugins:
            products = plugin.after_search(products, context, self.client)
        
        # 5. Verifica disponibilidade de estoque
        if context.sellers:
            # Usa simulação com sellers específicos
            products_with_stock = self.stock_manager.check_availability_with_sellers(
                client=self.client,
                products=products,
                context=context,
                priority_categories=self.priority_categories
            )
        else:
            # Usa simulação simples
            products_with_stock = self.stock_manager.check_availability_simple(
                client=self.client,
                products=products,
                context=context
            )
        
        # 6. Executa hooks after_stock_check
        for plugin in self.plugins:
            products_with_stock = plugin.after_stock_check(
                products_with_stock, context, self.client
            )
        
        # 7. Filtra produtos mantendo apenas os com estoque
        filtered_products = self.stock_manager.filter_products_with_stock(
            products, products_with_stock
        )
        
        # 8. Executa hooks de enriquecimento
        for plugin in self.plugins:
            filtered_products = plugin.enrich_products(
                filtered_products, context, self.client
            )
        
        # 9. Limita tamanho do payload
        filtered_products = self.stock_manager.limit_payload_size(
            filtered_products, self.max_payload_kb
        )
        
        # 10. Monta resultado final
        result = self._build_result(filtered_products, context)
        
        # 11. Executa hooks de finalização
        for plugin in self.plugins:
            result = plugin.finalize_result(result, context)
        
        return result
    
    def _build_result(
        self, 
        products: Dict[str, Dict], 
        context: SearchContext
    ) -> Dict[str, Any]:
        """
        Monta o resultado final da busca.
        
        Args:
            products: Produtos filtrados
            context: Contexto da busca
            
        Returns:
            Resultado formatado
        """
        result = {}
        
        # Adiciona dados extras do contexto primeiro
        if context.extra_data:
            result.update(context.extra_data)
        
        # Adiciona mensagem de região se houver
        if context.region_error:
            result["region_message"] = context.region_error
        
        # Adiciona produtos
        result.update(products)
        
        return result
    
    def search_by_sku(self, sku_id: str) -> Optional[Dict]:
        """
        Busca um produto específico pelo SKU.
        
        Args:
            sku_id: ID do SKU
            
        Returns:
            Dados do produto ou None
        """
        return self.client.get_product_by_sku(sku_id)
    
    def get_sku_details(self, sku_id: str) -> Dict:
        """
        Obtém detalhes de um SKU (dimensões, peso, etc).
        
        Args:
            sku_id: ID do SKU
            
        Returns:
            Detalhes do SKU
        """
        return self.client.get_sku_details(sku_id)
