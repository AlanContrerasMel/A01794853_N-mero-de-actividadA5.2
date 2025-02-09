#!/usr/bin/env python3
# pylint: disable=C0103, W0718, C0116
"""
computeSales.py

Este programa calcula el costo total de las ventas registradas en un
archivo JSON, utilizando un catálogo de precios proporcionado en otro
archivo JSON. Los resultados se muestran en pantalla y se escriben en
SalesResults.txt. También se informa el tiempo de ejecución.

Uso:
    python computeSales.py priceCatalogue.json salesRecord.json
"""

import json
import sys
import time


def load_json_file(filename):
    """
    Carga datos JSON desde un archivo.

    Args:
        filename (str): Ruta del archivo JSON.

    Returns:
        Los datos parseados o None si ocurre un error.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error al leer {filename}: {e}")
        return None


def build_price_dict(price_data):
    """
    Construye un diccionario de precios a partir de los datos del catálogo.

    Se espera que los datos tengan el campo "title" como identificador y
    "price" para el precio. El archivo puede ser un objeto único o una lista
    de objetos.

    Args:
        price_data: Datos parseados del catálogo de precios.

    Returns:
        dict: Diccionario con {título_del_producto: precio}
    """
    price_dict = {}

    if isinstance(price_data, list):
        for product in price_data:
            title = product.get("title")
            price = product.get("price")
            if title is None or price is None:
                print("Falta 'title' o 'price' en un producto, se omite.")
                continue
            try:
                price = float(price)
            except ValueError:
                print(f"Precio inválido para el producto '{title}', se omite.")
                continue
            price_dict[title] = price
    elif isinstance(price_data, dict):
        title = price_data.get("title")
        price = price_data.get("price")
        if title is None or price is None:
            print("El catálogo no contiene 'title' o 'price' en el producto.")
        else:
            try:
                price = float(price)
            except ValueError:
                print(f"Precio inválido para el producto '{title}'.")
            else:
                price_dict[title] = price
    else:
        print("El formato del catálogo de precios no es el esperado.")
    return price_dict


def process_sales(price_dict, sales_data):
    """
    Calcula el costo total de las ventas usando el diccionario de precios.

    Se espera que sales_data sea una lista de registros, donde cada uno tenga:
      - "Product": nombre del producto.
      - "Quantity": cantidad vendida.

    Args:
        price_dict (dict): Diccionario {título: precio}.
        sales_data (list): Lista de registros de venta.

    Returns:
        tuple: (costo_total (float), cantidad_de_errores (int))
    """
    total_cost = 0.0
    error_count = 0

    if not isinstance(sales_data, list):
        print("El registro de ventas no está en formato de lista.")
        return total_cost, error_count

    for sale in sales_data:
        if not isinstance(sale, dict):
            print("Registro de venta inválido, se esperaba un diccionario.")
            error_count += 1
            continue

        product = sale.get("Product")
        quantity = sale.get("Quantity")

        if product is None or quantity is None:
            print("Falta 'Product' o 'Quantity' en el registro de venta.")
            error_count += 1
            continue

        try:
            quantity = float(quantity)
        except (ValueError, TypeError):
            print(f"Cantidad inválida para el producto '{product}'.")
            error_count += 1
            continue

        price = price_dict.get(product)
        if price is None:
            print(f"Producto '{product}' no encontrado en el catálogo.")
            error_count += 1
            continue

        total_cost += price * quantity

    return total_cost, error_count


def main():
    """
    Función principal que coordina la carga de archivos,
    el cálculo de las ventas
    y la generación de la salida en consola y en el archivo de resultados.
    """
    start_time = time.time()

    if len(sys.argv) != 3:
        print(
            "Uso: python computeSales.py priceCatalogue.json "
            "salesRecord.json"
        )
        sys.exit(1)

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    price_data = load_json_file(price_file)
    if price_data is None:
        print("Error al cargar el catálogo de precios. Saliendo.")
        sys.exit(1)

    sales_data = load_json_file(sales_file)
    if sales_data is None:
        print("Error al cargar el registro de ventas. Saliendo.")
        sys.exit(1)

    price_dict = build_price_dict(price_data)
    total_cost, error_count = process_sales(price_dict, sales_data)
    elapsed_time = time.time() - start_time

    result_str = (
        "Resultados de la Computación de Ventas\n"
        "-------------------------------------\n"
        f"Costo Total: ${total_cost:.2f}\n"
        f"Errores encontrados: {error_count}\n"
        f"Tiempo de Ejecución: {elapsed_time:.2f} segundos\n"
    )

    print(result_str)

    try:
        with open("SalesResults.txt", "w", encoding="utf-8") as f:
            f.write(result_str)
    except OSError as e:
        print(
            f"Error al escribir en SalesResults.txt: {e}"
        )


if __name__ == "__main__":
    main()
