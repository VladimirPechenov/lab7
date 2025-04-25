# db.py
import mysql.connector
from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ----------------- CRUD для Category -----------------

def list_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, name, description FROM Category")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

def add_category(name, description):
    conn = get_connection(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO Category (name, description) VALUES (%s, %s)",
        (name, description)
    )
    conn.commit(); cur.close(); conn.close()

def update_category(category_id, name, description):
    conn = get_connection(); cur = conn.cursor()
    cur.execute(
        "UPDATE Category SET name=%s, description=%s WHERE category_id=%s",
        (name, description, category_id)
    )
    conn.commit(); cur.close(); conn.close()

def delete_category(category_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM Category WHERE category_id=%s", (category_id,))
    conn.commit(); cur.close(); conn.close()

# ----------------- CRUD для Brand -----------------

def list_brands():
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT brand_id, name, country FROM Brand")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

# ----------------- CRUD для Product -----------------

def list_products():
    conn = get_connection(); cur = conn.cursor()
    cur.execute(
        """
        SELECT p.product_id, p.name, c.name AS category, b.name AS brand,
               p.availability, p.remaining_stock, p.date_of_addition
        FROM Product p
        LEFT JOIN Category c ON p.category_id = c.category_id
        LEFT JOIN Brand b    ON p.brand_id = b.brand_id
        """
    )
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

def add_product(name, description, availability, date_of_addition,
                remaining_stock, brand_id, category_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO Product (name, description, availability, date_of_addition,"
        " remaining_stock, brand_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (name, description, availability, date_of_addition,
         remaining_stock, brand_id, category_id)
    )
    conn.commit(); cur.close(); conn.close()

def update_product(product_id, name, description, availability,
                   date_of_addition, remaining_stock, brand_id, category_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute(
        "UPDATE Product SET name=%s, description=%s, availability=%s,"
        " date_of_addition=%s, remaining_stock=%s, brand_id=%s,"
        " category_id=%s WHERE product_id=%s",
        (name, description, availability, date_of_addition,
         remaining_stock, brand_id, category_id, product_id)
    )
    conn.commit(); cur.close(); conn.close()

def delete_product(product_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM Product WHERE product_id=%s", (product_id,))
    conn.commit(); cur.close(); conn.close()

# ----------- Аналитические запросы -----------

def get_products_in_category(category_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute(
        """
        SELECT p.name, b.name AS brand, p.remaining_stock
        FROM Product p
        JOIN Brand b ON p.brand_id = b.brand_id
        WHERE p.category_id = %s
        """, (category_id,)
    )
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def get_low_stock_products(threshold):
    conn = get_connection(); cur = conn.cursor()
    cur.execute(
        """
        SELECT p.name, p.remaining_stock, c.name AS category
        FROM Product p
        JOIN Category c ON p.category_id = c.category_id
        WHERE p.remaining_stock < %s
        """, (threshold,)
    )
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

# ----------------- Связи -----------------

def get_products_by_brand(brand_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute(
        """
        SELECT p.product_id, p.name, c.name AS category, p.remaining_stock
        FROM Product p
        JOIN Category c ON p.category_id = c.category_id
        WHERE p.brand_id = %s
        """, (brand_id,)
    )
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def get_brands_in_category(category_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute(
        """
        SELECT DISTINCT b.brand_id, b.name, b.country
        FROM Brand b
        JOIN Product p ON b.brand_id = p.brand_id
        WHERE p.category_id = %s
        """, (category_id,)
    )
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

def get_categories_with_products():
    conn = get_connection(); cur = conn.cursor()
    cur.execute(
        """
        SELECT c.category_id, c.name, COUNT(p.product_id) AS product_count
        FROM Category c
        LEFT JOIN Product p ON c.category_id = p.category_id
        GROUP BY c.category_id, c.name
        """
    )
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows