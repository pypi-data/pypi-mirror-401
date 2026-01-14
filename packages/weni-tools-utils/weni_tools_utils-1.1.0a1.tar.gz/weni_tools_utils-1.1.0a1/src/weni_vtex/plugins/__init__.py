"""
Plugins para o Weni VTEX Concierge

Plugins são extensões opcionais que adicionam funcionalidades específicas.
Cada cliente pode escolher quais plugins utilizar.

Uso:
    from weni_vtex.plugins import Regionalization, Wholesale, Carousel, CAPI
    
    concierge = ProductConcierge(
        base_url="...",
        store_url="...",
        plugins=[
            Regionalization(),
            Wholesale(fixed_price_url="..."),
        ]
    )
"""

from .base import PluginBase
from .regionalization import Regionalization
from .wholesale import Wholesale
from .carousel import Carousel
from .capi import CAPI
from .weni_flow import WeniFlowTrigger

__all__ = [
    "PluginBase",
    "Regionalization",
    "Wholesale", 
    "Carousel",
    "CAPI",
    "WeniFlowTrigger",
]
