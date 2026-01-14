"""
Weni VTEX Tools - Biblioteca modular para integração com VTEX

Uso modular (funções independentes):
    from weni_vtex import search_products, simulate_cart, get_region, send_capi
    
    # Buscar produtos
    products = search_products(base_url, "furadeira")
    
    # Obter região por CEP
    region_id, sellers = get_region(base_url, "01310-100")
    
    # Simular carrinho
    available = simulate_cart(base_url, items, postal_code="01310-100")
    
    # Enviar evento CAPI
    send_capi(auth_token, channel_uuid, contact_urn, event_type="lead")

Uso com classe (orquestração):
    from weni_vtex import ProductConcierge
    
    concierge = ProductConcierge(base_url, store_url)
    result = concierge.search("furadeira", postal_code="01310-100")
"""

# Classes principais
from .concierge import ProductConcierge
from .client import VTEXClient
from .stock import StockManager
from .context import SearchContext

# Funções modulares (standalone)
from .functions import (
    # Busca
    search_products,
    search_product_by_sku,
    
    # Regionalização
    get_region,
    get_sellers_by_region,
    
    # Simulação de carrinho
    simulate_cart,
    simulate_cart_batch,
    check_stock_availability,
    
    # Preços
    get_wholesale_price,
    get_product_price,
    
    # Integrações
    send_capi_event,
    trigger_weni_flow,
    send_whatsapp_carousel,
    
    # SKU details
    get_sku_details,
)

__version__ = "1.1.0a1"
__all__ = [
    # Classes
    "ProductConcierge",
    "VTEXClient", 
    "StockManager",
    "SearchContext",
    
    # Funções modulares
    "search_products",
    "search_product_by_sku",
    "get_region",
    "get_sellers_by_region",
    "simulate_cart",
    "simulate_cart_batch",
    "check_stock_availability",
    "get_wholesale_price",
    "get_product_price",
    "send_capi_event",
    "trigger_weni_flow",
    "send_whatsapp_carousel",
    "get_sku_details",
]
