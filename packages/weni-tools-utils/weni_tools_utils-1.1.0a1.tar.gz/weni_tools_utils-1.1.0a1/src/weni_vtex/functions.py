"""
Funções modulares para integração VTEX

Cada função é independente e pode ser chamada separadamente.
Todos os parâmetros são configuráveis com valores default sensíveis.
"""

import requests
import json
from typing import Any, Dict, List, Optional, Tuple


# =============================================================================
# BUSCA DE PRODUTOS
# =============================================================================

def search_products(
    base_url: str,
    product_name: str,
    brand_name: str = "",
    region_id: Optional[str] = None,
    store_url: Optional[str] = None,
    hide_unavailable: bool = True,
    max_products: int = 20,
    max_variations: int = 5,
    utm_source: Optional[str] = None,
    timeout: int = 30
) -> Dict[str, Dict]:
    """
    Busca produtos usando a API Intelligent Search da VTEX.
    
    Args:
        base_url: URL base da API VTEX (ex: https://loja.vtexcommercestable.com.br)
        product_name: Nome do produto a buscar
        brand_name: Marca do produto (opcional)
        region_id: ID da região para regionalização (opcional)
        store_url: URL da loja para montar links (opcional, usa base_url se não informado)
        hide_unavailable: Se deve ocultar produtos indisponíveis (default: True)
        max_products: Número máximo de produtos (default: 20)
        max_variations: Número máximo de variações por produto (default: 5)
        utm_source: UTM source para links (opcional)
        timeout: Timeout da requisição em segundos (default: 30)
        
    Returns:
        Dicionário com produtos estruturados {nome_produto: dados}
        
    Example:
        products = search_products(
            base_url="https://www.obramax.com.br",
            product_name="furadeira",
            max_products=10
        )
    """
    store_url = store_url or base_url
    products_structured = {}
    product_count = 0
    
    # Constrói a URL
    query = f"{product_name} {brand_name}".strip()
    
    if region_id:
        search_url = (
            f"{base_url}/api/io/_v/api/intelligent-search/product_search/"
            f"region-id/{region_id}?query={query}&simulationBehavior=default"
            f"&hideUnavailableItems={str(hide_unavailable).lower()}"
        )
    else:
        search_url = (
            f"{base_url}/api/io/_v/api/intelligent-search/product_search/"
            f"?query={query}&simulationBehavior=default"
            f"&hideUnavailableItems={str(hide_unavailable).lower()}&allowRedirect=false"
        )
    
    try:
        response = requests.get(search_url, timeout=timeout)
        response.raise_for_status()
        products = response.json().get("products", [])
        
        for product in products:
            if product_count >= max_products:
                break
            
            if not product.get("items"):
                continue
            
            product_name_vtex = product.get("productName", "")
            categories = product.get("categories", [])
            
            # Processa variações
            variations = []
            for item in product.get("items", []):
                sku_id = item.get("itemId")
                if not sku_id:
                    continue
                
                sku_name = item.get("nameComplete")
                variation_items = item.get("variations", [])
                variations_text = _format_variations(variation_items)
                
                # Extrai imagem
                image_url = ""
                if item.get("images") and isinstance(item["images"], list):
                    for img in item["images"]:
                        img_url = img.get("imageUrl", "")
                        if img_url:
                            image_url = _clean_image_url(img_url)
                            break
                
                # Seleciona melhor seller e extrai preços
                seller_data, seller_id = _select_best_seller(item.get("sellers", []))
                
                prices = {}
                if seller_data:
                    prices = _extract_prices_from_seller(seller_data)
                
                variation = {
                    "sku_id": sku_id,
                    "sku_name": sku_name,
                    "variations": variations_text,
                    "price": prices.get("price"),
                    "spotPrice": prices.get("spot_price"),
                    "listPrice": prices.get("list_price"),
                    "pixPrice": prices.get("pix_price"),
                    "creditCardPrice": prices.get("credit_card_price"),
                    "imageUrl": image_url,
                    "sellerId": seller_id,
                }
                variations.append(variation)
            
            if variations:
                limited_variations = variations[:max_variations]
                
                # Descrição truncada
                description = product.get("description", "")
                if len(description) > 200:
                    description = description[:200] + "..."
                
                # Especificações formatadas
                spec_groups = product.get("specificationGroups", [])
                simplified_specs = _format_specifications(spec_groups)
                
                # Imagem do produto
                product_image_url = ""
                first_item = product.get("items", [None])[0]
                if first_item and "images" in first_item and first_item["images"]:
                    product_image_url = _clean_image_url(
                        first_item["images"][0].get("imageUrl", "")
                    )
                
                # Link do produto
                product_link = f"{store_url}{product.get('link', '')}"
                if utm_source:
                    product_link += f"?utm_source={utm_source}"
                
                products_structured[product_name_vtex] = {
                    "variations": limited_variations,
                    "description": description,
                    "brand": product.get("brand", ""),
                    "specification_groups": simplified_specs,
                    "productLink": product_link,
                    "imageUrl": product_image_url,
                    "categories": categories,
                }
                product_count += 1
    
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Erro na busca de produtos: {e}")
    except json.JSONDecodeError as e:
        print(f"ERROR: Erro ao processar JSON: {e}")
    
    return products_structured


def search_product_by_sku(
    base_url: str,
    sku_id: str,
    store_url: Optional[str] = None,
    timeout: int = 30
) -> Optional[Dict]:
    """
    Busca um produto específico pelo SKU ID.
    
    Args:
        base_url: URL base da API VTEX
        sku_id: ID do SKU
        store_url: URL da loja (opcional)
        timeout: Timeout da requisição (default: 30)
        
    Returns:
        Dados do produto ou None se não encontrado
        
    Example:
        product = search_product_by_sku(
            base_url="https://www.obramax.com.br",
            sku_id="61556"
        )
    """
    search_url = f"{base_url}/api/io/_v/api/intelligent-search/product_search/?query=sku.id:{sku_id}"
    
    try:
        response = requests.get(search_url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        
        products = data.get("products", [])
        if not products:
            return None
        
        return products[0]
    
    except Exception as e:
        print(f"ERROR: Erro ao buscar SKU {sku_id}: {e}")
        return None


# =============================================================================
# REGIONALIZAÇÃO
# =============================================================================

def get_region(
    base_url: str,
    postal_code: str,
    country: str = "BRA",
    sales_channel: int = 1,
    timeout: int = 30
) -> Tuple[Optional[str], Optional[str], List[str]]:
    """
    Consulta a API de regionalização para obter região e sellers.
    
    Args:
        base_url: URL base da API VTEX
        postal_code: CEP (formato: 00000-000 ou 00000000)
        country: Código do país (default: "BRA")
        sales_channel: Canal de vendas (default: 1)
        timeout: Timeout da requisição (default: 30)
        
    Returns:
        Tuple (region_id, error_message, sellers_list)
        
    Example:
        region_id, error, sellers = get_region(
            base_url="https://www.obramax.com.br",
            postal_code="01310-100"
        )
        
        if error:
            print(f"Erro: {error}")
        else:
            print(f"Região: {region_id}, Sellers: {sellers}")
    """
    region_url = f"{base_url}/api/checkout/pub/regions?country={country}&postalCode={postal_code}&sc={sales_channel}"
    
    try:
        response = requests.get(region_url, timeout=timeout)
        response.raise_for_status()
        regions_data = response.json()
        
        if not regions_data:
            return None, "Região não atendida. Compre presencialmente em nossas lojas.", []
        
        region = regions_data[0]
        sellers = region.get("sellers", [])
        
        if not sellers:
            return None, "Nenhum seller disponível para esta região.", []
        
        region_id = region.get("id")
        seller_ids = [seller.get("id") for seller in sellers]
        
        return region_id, None, seller_ids
    
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Erro na regionalização: {e}")
        return None, f"Erro ao consultar regionalização: {e}", []


def get_sellers_by_region(
    base_url: str,
    postal_code: str,
    country: str = "BRA",
    timeout: int = 30
) -> List[str]:
    """
    Retorna apenas a lista de sellers para uma região.
    
    Args:
        base_url: URL base da API VTEX
        postal_code: CEP
        country: Código do país (default: "BRA")
        timeout: Timeout (default: 30)
        
    Returns:
        Lista de IDs de sellers
        
    Example:
        sellers = get_sellers_by_region(
            base_url="https://www.obramax.com.br",
            postal_code="01310-100"
        )
        # ['lojaobramax1000', 'lojaobramax1003', 'lojaobramax1500']
    """
    _, _, sellers = get_region(base_url, postal_code, country, timeout=timeout)
    return sellers


# =============================================================================
# SIMULAÇÃO DE CARRINHO
# =============================================================================

def simulate_cart(
    base_url: str,
    items: List[Dict],
    country: str = "BRA",
    postal_code: Optional[str] = None,
    timeout: int = 30
) -> Dict:
    """
    Realiza simulação de carrinho para verificar disponibilidade.
    
    Args:
        base_url: URL base da API VTEX
        items: Lista de itens [{"id": "sku_id", "quantity": 1, "seller": "1"}]
        country: Código do país (default: "BRA")
        postal_code: CEP (opcional)
        timeout: Timeout (default: 30)
        
    Returns:
        Resposta da simulação com disponibilidade
        
    Example:
        result = simulate_cart(
            base_url="https://www.obramax.com.br",
            items=[
                {"id": "61556", "quantity": 1, "seller": "1"},
                {"id": "82598", "quantity": 2, "seller": "1"}
            ],
            postal_code="01310-100"
        )
        
        for item in result.get("items", []):
            print(f"SKU {item['id']}: {item['availability']}")
    """
    url = f"{base_url}/api/checkout/pub/orderForms/simulation"
    
    payload = {
        "items": items,
        "country": country
    }
    
    if postal_code:
        payload["postalCode"] = postal_code
    
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Erro na simulação de carrinho: {e}")
        return {"items": []}


def simulate_cart_batch(
    base_url: str,
    sku_id: str,
    sellers: List[str],
    postal_code: str,
    quantity: int = 1,
    max_quantity_per_seller: int = 8000,
    max_total_quantity: int = 24000,
    timeout: int = 30
) -> Optional[Dict]:
    """
    Simula um SKU específico com múltiplos sellers (usado para regionalização).
    
    Args:
        base_url: URL base da API VTEX
        sku_id: ID do SKU
        sellers: Lista de sellers
        postal_code: CEP
        quantity: Quantidade desejada (default: 1)
        max_quantity_per_seller: Quantidade máxima por seller (default: 8000)
        max_total_quantity: Quantidade máxima total (default: 24000)
        timeout: Timeout (default: 30)
        
    Returns:
        Melhor resultado da simulação ou None
        
    Example:
        result = simulate_cart_batch(
            base_url="https://www.obramax.com.br",
            sku_id="61556",
            sellers=["lojaobramax1000", "lojaobramax1003"],
            postal_code="01310-100",
            quantity=10
        )
    """
    quantity = int(quantity)
    
    # Calcula quantidade por seller
    if len(sellers) > 1:
        total_quantity = min(quantity * len(sellers), max_total_quantity)
        quantity_per_seller = min(total_quantity // len(sellers), max_quantity_per_seller)
    else:
        quantity_per_seller = min(quantity, max_quantity_per_seller)
    
    items = [{"id": sku_id, "quantity": quantity_per_seller, "seller": seller} 
             for seller in sellers]
    
    url = f"{base_url}/_v/api/simulations-batches?sc=1&RnbBehavior=1"
    payload = {
        "items": items,
        "country": "BRA",
        "postalCode": postal_code
    }
    
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        simulation_data = response.json()
        
        data_content = simulation_data.get("data", {})
        if not data_content:
            return None
        
        sku_simulations = data_content.get(sku_id, [])
        if not sku_simulations:
            return None
        
        # Retorna a simulação com maior quantidade
        return max(sku_simulations, key=lambda x: x.get("quantity", 0))
    
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Erro na simulação batch: {e}")
        return None


def check_stock_availability(
    base_url: str,
    sku_ids: List[str],
    seller: str = "1",
    quantity: int = 1,
    country: str = "BRA",
    postal_code: Optional[str] = None,
    timeout: int = 30
) -> Dict[str, bool]:
    """
    Verifica disponibilidade de estoque para uma lista de SKUs.
    
    Args:
        base_url: URL base da API VTEX
        sku_ids: Lista de SKU IDs
        seller: ID do seller (default: "1")
        quantity: Quantidade a verificar (default: 1)
        country: Código do país (default: "BRA")
        postal_code: CEP (opcional)
        timeout: Timeout (default: 30)
        
    Returns:
        Dicionário {sku_id: disponivel}
        
    Example:
        availability = check_stock_availability(
            base_url="https://www.obramax.com.br",
            sku_ids=["61556", "82598", "40240"],
            quantity=2
        )
        # {"61556": True, "82598": True, "40240": False}
    """
    items = [{"id": sku_id, "quantity": quantity, "seller": seller} for sku_id in sku_ids]
    
    result = simulate_cart(
        base_url=base_url,
        items=items,
        country=country,
        postal_code=postal_code,
        timeout=timeout
    )
    
    availability = {}
    for item in result.get("items", []):
        sku_id = item.get("id")
        is_available = item.get("availability", "").lower() == "available"
        availability[sku_id] = is_available
    
    # SKUs que não vieram na resposta são indisponíveis
    for sku_id in sku_ids:
        if sku_id not in availability:
            availability[sku_id] = False
    
    return availability


# =============================================================================
# PREÇOS
# =============================================================================

def get_wholesale_price(
    sku_id: str,
    seller_id: str,
    base_url: str = "https://www.obramax.com.br/fixedprices",
    timeout: int = 10
) -> Dict[str, Optional[Any]]:
    """
    Busca preço de atacado (quantidade mínima e valor) para um SKU.
    
    Args:
        sku_id: ID do SKU
        seller_id: ID do seller
        base_url: URL base da API de preços fixos
        timeout: Timeout (default: 10)
        
    Returns:
        Dicionário com minQuantity e valueAtacado
        
    Example:
        price = get_wholesale_price(
            sku_id="61556",
            seller_id="lojaobramax1000",
            base_url="https://www.obramax.com.br/fixedprices"
        )
        # {"minQuantity": 10, "valueAtacado": 179.90}
    """
    url = f"{base_url}/{seller_id}/{sku_id}/1"
    
    default_response = {"minQuantity": None, "valueAtacado": None}
    
    try:
        response = requests.get(url, timeout=timeout)
        
        if response.status_code != 200:
            return default_response
        
        data = response.json()
        
        return {
            "minQuantity": data.get("minQuantity") if isinstance(data, dict) else None,
            "valueAtacado": data.get("value") if isinstance(data, dict) else None
        }
    
    except Exception as e:
        print(f"ERROR: Erro ao buscar preço de atacado: {e}")
        return default_response


def get_product_price(
    base_url: str,
    sku_id: str,
    seller_id: str = "1",
    quantity: int = 1,
    country: str = "BRA",
    timeout: int = 30
) -> Dict[str, Optional[float]]:
    """
    Obtém preço de um produto via simulação de carrinho.
    
    Args:
        base_url: URL base da API VTEX
        sku_id: ID do SKU
        seller_id: ID do seller (default: "1")
        quantity: Quantidade (default: 1)
        country: Código do país (default: "BRA")
        timeout: Timeout (default: 30)
        
    Returns:
        Dicionário com price e list_price
        
    Example:
        price = get_product_price(
            base_url="https://www.obramax.com.br",
            sku_id="61556"
        )
        # {"price": 198.90, "list_price": 249.90}
    """
    result = simulate_cart(
        base_url=base_url,
        items=[{"id": sku_id, "quantity": quantity, "seller": seller_id}],
        country=country,
        timeout=timeout
    )
    
    items = result.get("items", [])
    if not items:
        return {"price": None, "list_price": None}
    
    item = items[0]
    price = item.get("price")
    list_price = item.get("listPrice")
    
    # Converte de centavos se necessário
    if price and price > 1000:
        price = price / 100
    if list_price and list_price > 1000:
        list_price = list_price / 100
    
    return {"price": price, "list_price": list_price}


# =============================================================================
# SKU DETAILS
# =============================================================================

def get_sku_details(
    base_url: str,
    sku_id: str,
    vtex_app_key: Optional[str] = None,
    vtex_app_token: Optional[str] = None,
    timeout: int = 30
) -> Dict:
    """
    Busca detalhes de um SKU (dimensões, peso, etc).
    Requer credenciais VTEX para API privada.
    
    Args:
        base_url: URL base da API VTEX
        sku_id: ID do SKU
        vtex_app_key: App Key VTEX (opcional, necessário para dados completos)
        vtex_app_token: App Token VTEX (opcional, necessário para dados completos)
        timeout: Timeout (default: 30)
        
    Returns:
        Dicionário com detalhes do SKU
        
    Example:
        details = get_sku_details(
            base_url="https://www.obramax.com.br",
            sku_id="61556",
            vtex_app_key="sua-app-key",
            vtex_app_token="seu-app-token"
        )
    """
    default_response = {
        "PackagedHeight": None,
        "PackagedLength": None,
        "PackagedWidth": None,
        "PackagedWeightKg": None,
        "Height": None,
        "Length": None,
        "Width": None,
        "WeightKg": None,
        "CubicWeight": None
    }
    
    if not vtex_app_key or not vtex_app_token:
        return default_response
    
    url = f"{base_url}/api/catalog/pvt/stockkeepingunit/{sku_id}"
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-VTEX-API-AppKey': vtex_app_key,
        'X-VTEX-API-AppToken': vtex_app_token
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        
        if response.status_code != 200:
            return default_response
        
        data = response.json()
        
        return {
            "PackagedHeight": data.get('PackagedHeight'),
            "PackagedLength": data.get('PackagedLength'),
            "PackagedWidth": data.get('PackagedWidth'),
            "PackagedWeightKg": data.get('PackagedWeightKg'),
            "Height": data.get('Height'),
            "Length": data.get('Length'),
            "Width": data.get('Width'),
            "WeightKg": data.get('WeightKg'),
            "CubicWeight": data.get('CubicWeight')
        }
    
    except Exception:
        return default_response


# =============================================================================
# INTEGRAÇÕES EXTERNAS
# =============================================================================

def send_capi_event(
    auth_token: str,
    channel_uuid: str,
    contact_urn: str,
    event_type: str = "lead",
    api_url: str = "https://flows.weni.ai/conversion/",
    timeout: int = 10
) -> bool:
    """
    Envia evento de conversão para a Meta (CAPI - Conversions API).
    
    Args:
        auth_token: Token de autenticação
        channel_uuid: UUID do canal
        contact_urn: URN do contato (ex: whatsapp:5511999999999)
        event_type: Tipo de evento - "lead" ou "purchase" (default: "lead")
        api_url: URL da API de conversões (default: Weni)
        timeout: Timeout (default: 10)
        
    Returns:
        True se enviado com sucesso
        
    Example:
        success = send_capi_event(
            auth_token="seu-token",
            channel_uuid="uuid-do-canal",
            contact_urn="whatsapp:5511999999999",
            event_type="lead"
        )
    """
    if event_type not in ["lead", "purchase"]:
        print(f"ERROR: event_type deve ser 'lead' ou 'purchase', recebido: {event_type}")
        return False
    
    if not all([auth_token, channel_uuid, contact_urn]):
        print("ERROR: auth_token, channel_uuid e contact_urn são obrigatórios")
        return False
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "channel_uuid": channel_uuid,
        "contact_urn": contact_urn,
        "event_type": event_type,
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=timeout)
        
        if response.status_code == 200:
            print(f"CAPI: Evento '{event_type}' enviado com sucesso")
            return True
        else:
            print(f"CAPI: Falha ao enviar evento: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"CAPI: Erro ao enviar evento: {e}")
        return False


def trigger_weni_flow(
    api_token: str,
    flow_uuid: str,
    contact_urn: str,
    params: Optional[Dict[str, Any]] = None,
    api_url: str = "https://flows.weni.ai/api/v2/flow_starts.json",
    timeout: int = 10
) -> bool:
    """
    Dispara um fluxo Weni para um contato.
    
    Args:
        api_token: Token de autenticação da API Weni
        flow_uuid: UUID do fluxo a disparar
        contact_urn: URN do contato
        params: Parâmetros extras para o fluxo (default: {"executions": 1})
        api_url: URL da API de fluxos (default: Weni)
        timeout: Timeout (default: 10)
        
    Returns:
        True se disparado com sucesso
        
    Example:
        success = trigger_weni_flow(
            api_token="seu-token",
            flow_uuid="uuid-do-fluxo",
            contact_urn="whatsapp:5511999999999",
            params={"source": "concierge"}
        )
    """
    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "flow": flow_uuid,
        "urns": [contact_urn],
        "params": params or {"executions": 1}
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=timeout)
        
        if response.status_code == 200:
            print(f"WeniFlow: Fluxo disparado com sucesso")
            return True
        else:
            print(f"WeniFlow: Falha ao disparar fluxo: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"WeniFlow: Erro ao disparar fluxo: {e}")
        return False


def send_whatsapp_carousel(
    auth_token: str,
    contact_urn: str,
    products: List[Dict],
    api_url: str = "https://flows.weni.ai/api/v2/whatsapp_broadcasts.json",
    max_items: int = 10,
    timeout: int = 30
) -> bool:
    """
    Envia um carousel de produtos via WhatsApp.
    
    Args:
        auth_token: Token de autenticação Weni
        contact_urn: URN do contato
        products: Lista de produtos com campos: name, price, image, product_link
        api_url: URL da API de broadcast (default: Weni)
        max_items: Número máximo de itens no carousel (default: 10)
        timeout: Timeout (default: 30)
        
    Returns:
        True se enviado com sucesso
        
    Example:
        success = send_whatsapp_carousel(
            auth_token="seu-token",
            contact_urn="whatsapp:5511999999999",
            products=[
                {
                    "name": "Furadeira Bosch",
                    "price": 429.90,
                    "image": "https://...",
                    "product_link": "https://..."
                }
            ]
        )
    """
    if not products:
        print("ERROR: Lista de produtos vazia")
        return False
    
    # Limita quantidade de produtos
    products = products[:max_items]
    
    # Cria XML do carousel
    carousel_items = []
    for product in products:
        name = product.get("name", "Produto")
        price = product.get("price")
        image_url = product.get("image", "")
        product_link = product.get("product_link", "")
        
        # Formata preço
        price_str = f"R$ {price:.2f}".replace(".", ",") if price else "Consulte"
        
        # Formata imagem em Markdown
        formatted_image = ""
        if image_url:
            alt_text = image_url.split('/')[-1] if '/' in image_url else "produto"
            formatted_image = f"![{alt_text}]({image_url})"
        
        carousel_item = f'''     <carousel-item>
         <name>{name}</name>
         <price>{price_str}</price>
         <description>{name}</description>
         <product_link>{product_link}</product_link>
         <image>{formatted_image}</image>
     </carousel-item>'''
        
        carousel_items.append(carousel_item)
    
    xml_content = '''<?xml version="1.0" encoding="UTF-8" ?>
''' + '\n'.join(carousel_items)
    
    # Envia
    headers = {
        "Authorization": f"Token {auth_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "urns": [contact_urn],
        "msg": {"text": xml_content}
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()
        print("Carousel: Enviado com sucesso")
        return True
    
    except Exception as e:
        print(f"Carousel: Erro ao enviar: {e}")
        return False


# =============================================================================
# FUNÇÕES AUXILIARES (PRIVADAS)
# =============================================================================

def _clean_image_url(img_url: str) -> str:
    """Remove query parameters da URL da imagem."""
    if not img_url:
        return ""
    if '?' in img_url:
        img_url = img_url.split('?')[0]
    if '#' in img_url:
        img_url = img_url.split('#')[0]
    return img_url


def _format_variations(variation_items: List[Dict]) -> str:
    """Formata variações para string compacta."""
    compact_variations = []
    for var in variation_items:
        name = var.get("name", "")
        values = var.get("values", [])
        if name and values:
            value = values[0] if values else ""
            compact_variations.append(f"{name}: {value}")
    return f"[{', '.join(compact_variations)}]" if compact_variations else "[]"


def _format_specifications(spec_groups: List[Dict], max_groups: int = 3) -> List[Dict]:
    """Formata especificações de forma simplificada."""
    simplified_specs = []
    
    # Procura allSpecifications
    all_specs_group = None
    for group in spec_groups:
        if group.get("name") == "allSpecifications" and group.get("specifications"):
            all_specs_group = group
            break
    
    if all_specs_group:
        specs = all_specs_group["specifications"]
        compact_specs = []
        for spec in specs:
            name = spec.get("name", "")
            values = spec.get("values", [])
            if name and values:
                value = values[0] if values else ""
                compact_specs.append(f"{name}: {value}")
        
        simplified_specs.append({
            "name": "allSpecifications",
            "specifications": f"[{', '.join(compact_specs)}]" if compact_specs else "[]"
        })
    else:
        for group in spec_groups[:max_groups]:
            if group.get("specifications"):
                limited_specs = group["specifications"][:5]
                compact_specs = []
                for spec in limited_specs:
                    name = spec.get("name", "")
                    values = spec.get("values", [])
                    if name and values:
                        value = values[0] if values else ""
                        compact_specs.append(f"{name}: {value}")
                
                simplified_specs.append({
                    "name": group.get("name", ""),
                    "specifications": f"[{', '.join(compact_specs)}]" if compact_specs else "[]"
                })
    
    return simplified_specs


def _select_best_seller(sellers: List[Dict]) -> Tuple[Optional[Dict], Optional[str]]:
    """Seleciona o melhor seller para um item."""
    if not sellers:
        return None, None
    
    # Tenta seller padrão com estoque
    for seller in sellers:
        if (seller.get("sellerDefault", False) and 
            seller.get("commertialOffer", {}).get("AvailableQuantity", 0) > 0):
            return seller, seller.get("sellerId")
    
    # Tenta primeiro com estoque
    for seller in sellers:
        if seller.get("commertialOffer", {}).get("AvailableQuantity", 0) > 0:
            return seller, seller.get("sellerId")
    
    # Fallback: primeiro disponível
    return sellers[0], sellers[0].get("sellerId")


def _extract_prices_from_seller(seller_data: Dict) -> Dict[str, Optional[float]]:
    """Extrai preços de um seller."""
    commercial_offer = seller_data.get("commertialOffer", {})
    installments = commercial_offer.get("Installments", [])
    
    prices = {
        "price": commercial_offer.get("Price"),
        "spot_price": commercial_offer.get("spotPrice"),
        "list_price": commercial_offer.get("ListPrice"),
        "pix_price": None,
        "credit_card_price": None,
    }
    
    for installment in installments:
        if installment.get("PaymentSystemName") == "Pix":
            prices["pix_price"] = installment.get("Value")
            break
    
    for installment in installments:
        if (installment.get("PaymentSystemName") == "Visa" and 
            installment.get("NumberOfInstallments") == 1):
            prices["credit_card_price"] = installment.get("Value")
            break
    
    return prices
