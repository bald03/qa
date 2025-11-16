import requests
import json

BASE_URL = "http://shop2.qatl.ru/shop/" 

def get_all_products():
    url = f"{BASE_URL}/api/products"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Get all products error: {url}: {e}")
        return None

def get_product_by_id(product_id):
    all_products = get_all_products()
    if all_products:
        for product in all_products:
            if product.get('id') == str(product_id):
                return product

    print(f"Get product by id {product_id} error")
    return None

def delete_product(product_id):
    url = f"{BASE_URL}/api/deleteproduct?id={product_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Delete product error: {url}: {e}")
        return None

def add_product(data):
    url = f"{BASE_URL}/api/addproduct"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Add product erroe {url}: {e}\nRequest body: {json.dumps(data)}")
        return None

def edit_product(data):
    url = f"{BASE_URL}/api/editproduct"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Edit product error {url}: {e}\nRequest body: {json.dumps(data)}")
        return None