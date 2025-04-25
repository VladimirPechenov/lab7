import tkinter as tk
from tkinter import ttk, messagebox
from logic import (
    get_categories, create_category, remove_category, modify_category,
    get_products, create_product, remove_product, modify_product,
    get_brands
)
from datetime import datetime
from PIL import Image, ImageTk  # Для работы с изображениями

def show_categories(tree, name_filter="", id_filter=None):
    tree.delete(*tree.get_children())
    for cid, name, desc in get_categories(name_filter, id_filter):
        tree.insert("", "end", values=(cid, name, desc))

def add_category_ui(name_entry, desc_entry, tree):
    name = name_entry.get().strip()
    desc = desc_entry.get().strip()
    try:
        create_category(name, desc)
        show_categories(tree)
        messagebox.showinfo("Успех", "Категория добавлена.")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

def delete_category_ui(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите категорию для удаления.")
        return
    category_id = tree.item(selected_item, "values")[0]
    remove_category(category_id)
    show_categories(tree)
    messagebox.showinfo("Успех", "Категория удалена.")

def update_category_ui(tree, name_entry, desc_entry):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите категорию для обновления.")
        return
    category_id = tree.item(selected_item, "values")[0]
    name = name_entry.get().strip()
    desc = desc_entry.get().strip()
    try:
        modify_category(category_id, name, desc)
        show_categories(tree)
        messagebox.showinfo("Успех", "Категория обновлена.")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

def show_products(tree, name_filter="", category_filter="", brand_filter="", id_filter=None):
    tree.delete(*tree.get_children())
    for pid, name, category, brand, avail, stock, date in get_products(
        name_filter=name_filter, category_filter=category_filter, brand_filter=brand_filter, id_filter=id_filter
    ):
        tree.insert("", "end", values=(pid, name, category, brand, avail, stock, date))

def delete_product_ui(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите продукт для удаления.")
        return
    product_id = tree.item(selected_item, "values")[0]
    try:
        remove_product(product_id)
        show_products(tree)
        messagebox.showinfo("Успех", "Продукт удалён.")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

def update_product_ui(tree, name_entry, desc_entry, avail_var, stock_entry, category_combo, brand_combo):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Выберите продукт для обновления.")
        return
    product_id = tree.item(selected_item, "values")[0]
    name = name_entry.get().strip()
    desc = desc_entry.get().strip()
    avail = avail_var.get()
    stock = stock_entry.get().strip()
    category = category_combo.get()
    brand = brand_combo.get()
    try:
        modify_product(product_id, name, desc, avail, stock, category, brand)
        show_products(tree)
        messagebox.showinfo("Успех", "Продукт обновлён.")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

def add_product_ui(tree, name_entry, desc_entry, avail_var, stock_entry, category_combo, brand_combo):
    name = name_entry.get().strip()
    desc = desc_entry.get().strip()
    avail = avail_var.get()
    stock = stock_entry.get().strip()
    category = category_combo.get()
    brand = brand_combo.get()
    try:
        create_product(name, desc, avail, stock, category, brand)
        show_products(tree)
        messagebox.showinfo("Успех", "Продукт добавлен.")
    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

def show_brands(tree, id_filter=None):
    tree.delete(*tree.get_children())
    for bid, name, country in get_brands(id_filter):
        tree.insert("", "end", values=(bid, name, country))

def show_products_by_category(tree, category_name):
    tree.delete(*tree.get_children())
    for pid, name, category, brand, avail, stock, date in get_products(category_filter=category_name):
        tree.insert("", "end", values=(pid, name, category, brand, avail, stock, date))

def show_products_below_stock(tree, stock_threshold):
    tree.delete(*tree.get_children())
    for pid, name, category, brand, avail, stock, date in get_products():
        if int(stock) < stock_threshold:
            tree.insert("", "end", values=(pid, name, category, brand, avail, stock, date))

def create_main_window():
    root = tk.Tk()
    root.title("Музыкальный магазин")
    root.geometry("800x600")

    # Установка фона
    bg_image = Image.open("d:/Programming/2_курс/DB/lab6/assets/music_background.jpg")
    bg_image = bg_image.resize((800, 600))  # Убираем Image.ANTIALIAS
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    # Стили
    style = ttk.Style()
    style.configure("TNotebook", background="#f5deb3", borderwidth=0)
    style.configure("TNotebook.Tab", font=("Courier", 12, "bold"), padding=[10, 5])
    style.configure("TButton", font=("Courier", 10, "bold"), background="#d2b48c", foreground="#000")
    style.configure("Treeview", font=("Courier", 10), rowheight=25, background="#fffaf0", fieldbackground="#fffaf0")
    style.configure("Treeview.Heading", font=("Courier", 12, "bold"), background="#d2b48c")

    tab_control = ttk.Notebook(root, style="TNotebook")

    # Вкладка "Категории"
    category_tab = ttk.Frame(tab_control)
    tab_control.add(category_tab, text="🎼 Категории")

    category_scroll = ttk.Scrollbar(category_tab, orient="vertical")
    tree_categories = ttk.Treeview(category_tab, columns=("id", "name", "desc"), show="headings", yscrollcommand=category_scroll.set)
    category_scroll.config(command=tree_categories.yview)
    category_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    tree_categories.heading("id", text="ID")
    tree_categories.heading("name", text="Название")
    tree_categories.heading("desc", text="Описание (Названия)")
    tree_categories.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    search_frame_categories = ttk.Frame(category_tab)
    search_frame_categories.pack(fill=tk.X, pady=5)

    ttk.Label(search_frame_categories, text="🔍 Название:").pack(side=tk.LEFT, padx=5)
    name_filter_entry_categories = ttk.Entry(search_frame_categories)
    name_filter_entry_categories.pack(side=tk.LEFT, padx=5)

    ttk.Label(search_frame_categories, text="🔍 ID:").pack(side=tk.LEFT, padx=5)
    id_filter_entry_categories = ttk.Entry(search_frame_categories)
    id_filter_entry_categories.pack(side=tk.LEFT, padx=5)

    ttk.Button(search_frame_categories, text="Поиск", command=lambda: show_categories(
        tree_categories,
        name_filter=name_filter_entry_categories.get(),
        id_filter=int(id_filter_entry_categories.get()) if id_filter_entry_categories.get().isdigit() else None
    )).pack(side=tk.LEFT, padx=5)

    form_frame = ttk.Frame(category_tab)
    form_frame.pack(fill=tk.X)

    ttk.Label(form_frame, text="⚙️ Название:").pack(side=tk.LEFT, padx=5)
    name_entry = ttk.Entry(form_frame)
    name_entry.pack(side=tk.LEFT, padx=5)

    ttk.Label(form_frame, text="⚙️ Описание:").pack(side=tk.LEFT, padx=5)
    desc_entry = ttk.Entry(form_frame)
    desc_entry.pack(side=tk.LEFT, padx=5)

    ttk.Button(form_frame, text="Добавить", command=lambda: add_category_ui(name_entry, desc_entry, tree_categories)).pack(side=tk.LEFT, padx=5)
    ttk.Button(form_frame, text="Удалить", command=lambda: delete_category_ui(tree_categories)).pack(side=tk.LEFT, padx=5)
    ttk.Button(form_frame, text="Обновить", command=lambda: update_category_ui(tree_categories, name_entry, desc_entry)).pack(side=tk.LEFT, padx=5)

    ttk.Button(category_tab, text="Обновить", command=lambda: show_categories(tree_categories)).pack(pady=5)

    # Инициализация данных
    show_categories(tree_categories)

    # Вкладка "Товары"
    product_tab = ttk.Frame(tab_control)
    tab_control.add(product_tab, text="🎻 Товары")

    product_scroll = ttk.Scrollbar(product_tab, orient="vertical")
    tree_products = ttk.Treeview(product_tab, columns=("id", "name", "category", "brand", "avail", "stock", "date"), show="headings", yscrollcommand=product_scroll.set)
    product_scroll.config(command=tree_products.yview)
    product_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    tree_products.heading("id", text="ID")
    tree_products.heading("name", text="Название")
    tree_products.heading("category", text="Категория")
    tree_products.heading("brand", text="Бренд")
    tree_products.heading("avail", text="В наличии")
    tree_products.heading("stock", text="Остаток")
    tree_products.heading("date", text="Дата добавления")
    tree_products.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    search_frame_products = ttk.Frame(product_tab)
    search_frame_products.pack(fill=tk.X, pady=5)

    ttk.Label(search_frame_products, text="🔍 Название:").pack(side=tk.LEFT, padx=5)
    name_filter_entry_products = ttk.Entry(search_frame_products)
    name_filter_entry_products.pack(side=tk.LEFT, padx=5)

    ttk.Label(search_frame_products, text="🔍 ID:").pack(side=tk.LEFT, padx=5)
    id_filter_entry_products = ttk.Entry(search_frame_products)
    id_filter_entry_products.pack(side=tk.LEFT, padx=5)

    ttk.Label(search_frame_products, text="🔍 Категория:").pack(side=tk.LEFT, padx=5)
    category_filter_combo = ttk.Combobox(search_frame_products, values=[c[1] for c in get_categories()])
    category_filter_combo.pack(side=tk.LEFT, padx=5)

    ttk.Label(search_frame_products, text="🔍 Бренд:").pack(side=tk.LEFT, padx=5)
    brand_filter_combo = ttk.Combobox(search_frame_products, values=[b[1] for b in get_brands()])
    brand_filter_combo.pack(side=tk.LEFT, padx=5)

    ttk.Button(search_frame_products, text="Поиск", command=lambda: show_products(
        tree_products,
        name_filter=name_filter_entry_products.get(),
        category_filter=category_filter_combo.get(),
        brand_filter=brand_filter_combo.get(),
        id_filter=int(id_filter_entry_products.get()) if id_filter_entry_products.get().isdigit() else None
    )).pack(side=tk.LEFT, padx=5)

    form_frame_products = ttk.Frame(product_tab)
    form_frame_products.pack(fill=tk.X, pady=5)

    ttk.Label(form_frame_products, text="⚙️ Название:").pack(side=tk.LEFT, padx=5)
    name_entry_products = ttk.Entry(form_frame_products)
    name_entry_products.pack(side=tk.LEFT, padx=5)

    ttk.Label(form_frame_products, text="⚙️ Описание:").pack(side=tk.LEFT, padx=5)
    desc_entry_products = ttk.Entry(form_frame_products)
    desc_entry_products.pack(side=tk.LEFT, padx=5)

    ttk.Label(form_frame_products, text="⚙️ В наличии:").pack(side=tk.LEFT, padx=5)
    avail_var_products = tk.BooleanVar()
    avail_check_products = ttk.Checkbutton(form_frame_products, variable=avail_var_products)
    avail_check_products.pack(side=tk.LEFT, padx=5)

    ttk.Label(form_frame_products, text="⚙️ Остаток:").pack(side=tk.LEFT, padx=5)
    stock_entry_products = ttk.Entry(form_frame_products)
    stock_entry_products.pack(side=tk.LEFT, padx=5)

    ttk.Label(form_frame_products, text="⚙️ Категория:").pack(side=tk.LEFT, padx=5)
    category_combo_products = ttk.Combobox(form_frame_products, values=[c[1] for c in get_categories()])
    category_combo_products.pack(side=tk.LEFT, padx=5)

    ttk.Label(form_frame_products, text="⚙️ Бренд:").pack(side=tk.LEFT, padx=5)
    brand_combo_products = ttk.Combobox(form_frame_products, values=[b[1] for b in get_brands()])
    brand_combo_products.pack(side=tk.LEFT, padx=5)

    ttk.Button(form_frame_products, text="Добавить", command=lambda: add_product_ui(
        tree_products, name_entry_products, desc_entry_products, avail_var_products,
        stock_entry_products, category_combo_products, brand_combo_products
    )).pack(side=tk.LEFT, padx=5)

    ttk.Button(form_frame_products, text="Удалить", command=lambda: delete_product_ui(tree_products)).pack(side=tk.LEFT, padx=5)
    ttk.Button(form_frame_products, text="Обновить", command=lambda: update_product_ui(
        tree_products, name_entry_products, desc_entry_products, avail_var_products,
        stock_entry_products, category_combo_products, brand_combo_products
    )).pack(side=tk.LEFT, padx=5)

    analysis_frame_products = ttk.Frame(product_tab)
    analysis_frame_products.pack(fill=tk.X, pady=10)

    ttk.Label(analysis_frame_products, text="Категория:").pack(side=tk.LEFT, padx=5)
    category_combo_analysis = ttk.Combobox(analysis_frame_products, values=[c[1] for c in get_categories()])
    category_combo_analysis.pack(side=tk.LEFT, padx=5)

    ttk.Button(analysis_frame_products, text="Показать товары категории", command=lambda: show_products_by_category(
        tree_products, category_combo_analysis.get()
    )).pack(side=tk.LEFT, padx=5)

    ttk.Label(analysis_frame_products, text="Порог остатка:").pack(side=tk.LEFT, padx=5)
    stock_threshold_entry = ttk.Entry(analysis_frame_products)
    stock_threshold_entry.pack(side=tk.LEFT, padx=5)

    ttk.Button(analysis_frame_products, text="Показать товары ниже порога", command=lambda: show_products_below_stock(
        tree_products, int(stock_threshold_entry.get()) if stock_threshold_entry.get().isdigit() else 0
    )).pack(side=tk.LEFT, padx=5)

    ttk.Button(product_tab, text="Обновить", command=lambda: show_products(tree_products)).pack(pady=5)

    # Инициализация данных
    show_products(tree_products)

    # Вкладка "Бренды"
    brand_tab = ttk.Frame(tab_control)
    tab_control.add(brand_tab, text="🎵 Бренды")

    brand_scroll = ttk.Scrollbar(brand_tab, orient="vertical")
    tree_brands = ttk.Treeview(brand_tab, columns=("id", "name", "country"), show="headings", yscrollcommand=brand_scroll.set)
    brand_scroll.config(command=tree_brands.yview)
    brand_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    tree_brands.heading("id", text="ID")
    tree_brands.heading("name", text="Название")
    tree_brands.heading("country", text="Страна")
    tree_brands.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    search_frame_brands = ttk.Frame(brand_tab)
    search_frame_brands.pack(fill=tk.X, pady=5)

    ttk.Label(search_frame_brands, text="🔍 ID:").pack(side=tk.LEFT, padx=5)
    id_filter_entry_brands = ttk.Entry(search_frame_brands)
    id_filter_entry_brands.pack(side=tk.LEFT, padx=5)

    ttk.Button(search_frame_brands, text="Поиск", command=lambda: show_brands(
        tree_brands,
        id_filter=int(id_filter_entry_brands.get()) if id_filter_entry_brands.get().isdigit() else None
    )).pack(side=tk.LEFT, padx=5)

    ttk.Button(brand_tab, text="Обновить", command=lambda: show_brands(tree_brands)).pack(pady=5)

    # Инициализация данных
    show_categories(tree_categories)
    show_products(tree_products)
    show_brands(tree_brands)

    tab_control.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    root.mainloop()

if __name__ == '__main__':
    create_main_window()