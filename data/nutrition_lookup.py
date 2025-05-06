import requests

def get_nutritional_info(product_name):
    url = f"https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": product_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        products = data.get("products")
        if products:
            product = products[0]
            nutriments = product.get("nutriments", {})
            return {
                "Kalória": f"{nutriments.get('energy-kcal_100g', 'n/a')} kcal",
                "Fehérje": f"{nutriments.get('proteins_100g', 'n/a')} g",
                "Zsír": f"{nutriments.get('fat_100g', 'n/a')} g",
                "Szénhidrát": f"{nutriments.get('carbohydrates_100g', 'n/a')} g",
                "Cukor": f"{nutriments.get('sugars_100g', 'n/a')} g"
            }
    return None
