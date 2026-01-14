"""
Weni VTEX Concierge - Biblioteca compartilhada para agentes de busca de produtos VTEX

Uso básico:
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

from .concierge import ProductConcierge
from .client import VTEXClient
from .stock import StockManager
from .context import SearchContext

__version__ = "1.0.0"
__all__ = [
    "ProductConcierge",
    "VTEXClient", 
    "StockManager",
    "SearchContext",
]
