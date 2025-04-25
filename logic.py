from db import (
    list_categories, add_category, update_category, delete_category,
    list_brands, list_products, add_product, update_product, delete_product
)
from datetime import datetime

def get_categories(name_filter="", id_filter=None):
    categories = list_categories()
    return [
        (cid, name, desc) for cid, name, desc in categories
        if (name_filter.lower() in name.lower() and
            (id_filter is None or cid == id_filter))
    ]

def create_category(name, description):
    if not name:
        raise ValueError("Название категории не может быть пустым.")
    add_category(name, description)

def remove_category(category_id):
    delete_category(category_id)

def modify_category(category_id, name, description):
    if not name:
        raise ValueError("Название категории не может быть пустым.")
    update_category(category_id, name, description)

def get_products(name_filter="", category_filter="", brand_filter="", id_filter=None):
    products = list_products()
    return [
        (pid, name, category, brand, avail, stock, date) for pid, name, category, brand, avail, stock, date in products
        if (name_filter.lower() in name.lower() and
            (not category_filter or category_filter == category) and
            (not brand_filter or brand_filter == brand) and
            (id_filter is None or pid == id_filter))
    ]

def get_category_id_by_name(name):
    categories = list_categories()
    for cid, cname, _ in categories:
        if cname == name:
            return cid
    raise ValueError(f"Категория '{name}' не найдена.")

def get_brand_id_by_name(name):
    brands = list_brands()
    for bid, bname, _ in brands:
        if bname == name:
            return bid
    raise ValueError(f"Бренд '{name}' не найден.")

def create_product(name, description, availability, stock, category, brand):
    if not name or not stock.isdigit() or not category or not brand:
        raise ValueError("Заполните все поля корректно.")
    category_id = get_category_id_by_name(category)
    brand_id = get_brand_id_by_name(brand)
    date_of_addition = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Текущая дата и время
    add_product(name, description, availability, date_of_addition, int(stock), brand_id, category_id)

def remove_product(product_id):
    delete_product(product_id)

def modify_product(product_id, name, description, availability, stock, category, brand):
    if not name or not stock.isdigit() or not category or not brand:
        raise ValueError("Заполните все поля корректно.")
    category_id = get_category_id_by_name(category)
    brand_id = get_brand_id_by_name(brand)
    update_product(product_id, name, description, availability, None, int(stock), brand_id, category_id)

def get_brands(id_filter=None):
    brands = list_brands()
    return [
        (bid, name, country) for bid, name, country in brands
        if id_filter is None or bid == id_filter
    ]
