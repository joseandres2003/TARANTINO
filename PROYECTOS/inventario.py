# sistema_inventario.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Archivos para persistencia
ARCHIVO_INVENTARIO = 'inventario.json'
ARCHIVO_VENTAS = 'ventas.json'
ARCHIVO_HISTORIAL = 'historial.json'

inventario = []
ventas = []
historial = []
sucursales = ["Todas", "Sucursal norte", "Sucursal sur", "Sucursal urubo", "Sucursal villa", "Sucursal centro"]
carrito = []
traslados = []

# ====================
# FUNCIONES DE ARCHIVOS
# ====================
def guardar_datos():
    with open(ARCHIVO_INVENTARIO, 'w') as f:
        json.dump(inventario, f)
    with open(ARCHIVO_VENTAS, 'w') as f:
        json.dump(ventas, f)
    with open(ARCHIVO_HISTORIAL, 'w') as f:
        json.dump(historial, f)

def cargar_datos():
    global inventario, ventas, historial
    if os.path.exists(ARCHIVO_INVENTARIO):
        with open(ARCHIVO_INVENTARIO, 'r') as f:
            inventario = json.load(f)
    if os.path.exists(ARCHIVO_VENTAS):
        with open(ARCHIVO_VENTAS, 'r') as f:
            ventas = json.load(f)
    if os.path.exists(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, 'r') as f:
            historial = json.load(f)

# ====================
# FUNCIONES DEL SISTEMA
# ====================
def registrar_historial(accion):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historial.append(f"[{timestamp}] {accion}")

def agregar_producto():
    sku = sku_entry.get()
    nombre = nombre_entry.get()
    precio = precio_entry.get()
    stock = stock_entry.get()
    sucursal = sucursal_entry.get()

    if not sku or not nombre or not precio or not stock or not sucursal:
        messagebox.showwarning("Campos Vacíos", "Completa todos los campos.")
        return

    producto = {
        'sku': sku,
        'nombre': nombre,
        'precio': float(precio),
        'stock': int(stock),
        'sucursal': sucursal
    }
    inventario.append(producto)
    registrar_historial(f"Agregado producto: {nombre} (SKU: {sku}) en {sucursal}.")
    limpiar_campos()
    actualizar_tabla()
    messagebox.showinfo("Producto agregado", f"{nombre} agregado correctamente.")

def eliminar_producto():
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Selecciona un producto", "No hay producto seleccionado.")
        return
    item = tree.item(seleccionado)
    sku = item['values'][0]
    for prod in inventario:
        if prod['sku'] == sku:
            inventario.remove(prod)
            registrar_historial(f"Eliminado producto: {prod['nombre']} (SKU: {sku})")
            break
    actualizar_tabla()
    messagebox.showinfo("Eliminado", "Producto eliminado exitosamente.")

def limpiar_campos():
    sku_entry.delete(0, tk.END)
    nombre_entry.delete(0, tk.END)
    precio_entry.delete(0, tk.END)
    stock_entry.delete(0, tk.END)
    sucursal_entry.set("")

def actualizar_tabla():
    seleccion = filtro_sucursal.get()
    busqueda = buscar_entry.get().lower()
    tree.delete(*tree.get_children())
    for prod in inventario:
        if (seleccion == "Todas" or prod['sucursal'] == seleccion) and \
           (busqueda in prod['sku'].lower() or busqueda in prod['nombre'].lower()):
            tree.insert("", tk.END, values=(prod['sku'], prod['nombre'], prod['precio'], prod['stock'], prod['sucursal']))

def cambiar_filtro(event=None):
    actualizar_tabla()

def resumen():
    productos_unicos = set(p['sku'] for p in inventario)
    total_unidades = sum(p['stock'] for p in inventario)
    bajo_stock = len([p for p in inventario if p['stock'] < 10])

    resumen_text = (
        f"Productos únicos: {len(productos_unicos)}\n"
        f"Unidades totales: {total_unidades}\n"
        f"Productos con bajo stock (<10): {bajo_stock}\n\n"
        "Historial de actividades recientes:\n\n" + "\n".join(historial[-10:])
    )
    messagebox.showinfo("Resumen del sistema", resumen_text)

def agregar_al_carrito():
    sku = venta_sku_entry.get()
    cantidad_str = venta_cantidad_entry.get()
    if not sku or not cantidad_str:
        messagebox.showwarning("Campos vacíos", "Completa los campos de venta.")
        return

    cantidad = int(cantidad_str)
    for prod in inventario:
        if prod['sku'] == sku:
            if prod['stock'] >= cantidad:
                carrito.append({
                    'sku': prod['sku'],
                    'nombre': prod['nombre'],
                    'cantidad': cantidad,
                    'precio': prod['precio'],
                    'total': cantidad * prod['precio']
                })
                actualizar_carrito()
                venta_sku_entry.delete(0, tk.END)
                venta_cantidad_entry.delete(0, tk.END)
                return
            else:
                messagebox.showerror("Stock insuficiente", f"Solo hay {prod['stock']} unidades disponibles.")
                return
    messagebox.showerror("Producto no encontrado", "El SKU no existe.")

def actualizar_carrito():
    carrito_tree.delete(*carrito_tree.get_children())
    for item in carrito:
        carrito_tree.insert("", tk.END, values=(item['sku'], item['nombre'], item['cantidad'], item['precio'], item['total']))
    total = sum(item['total'] for item in carrito)
    total_label.config(text=f"Total: ${total:.2f}")

def quitar_del_carrito():
    seleccionado = carrito_tree.selection()
    if not seleccionado:
        messagebox.showwarning("Nada seleccionado", "Selecciona un producto del carrito.")
        return
    item = carrito_tree.item(seleccionado)
    sku = item['values'][0]
    for c in carrito:
        if c['sku'] == sku:
            carrito.remove(c)
            break
    actualizar_carrito()

def confirmar_venta():
    if not carrito:
        messagebox.showinfo("Carrito vacío", "No hay productos en el carrito.")
        return
    texto_factura = "FACTURA DE VENTA\n\n"
    total_general = 0
    for item in carrito:
        for prod in inventario:
            if prod['sku'] == item['sku']:
                prod['stock'] -= item['cantidad']
                ventas.append(item)
        total_general += item['total']
        texto_factura += f"{item['cantidad']} x {item['nombre']} @ {item['precio']} = {item['total']}\n"
        registrar_historial(f"Venta: {item['cantidad']} x {item['nombre']} (SKU: {item['sku']})")
    texto_factura += f"\nTOTAL: ${total_general:.2f}"
    carrito.clear()
    actualizar_tabla()
    actualizar_carrito()
    messagebox.showinfo("Factura", texto_factura)

def trasladar_producto():
    sku = traslado_sku_entry.get()
    destino = traslado_sucursal_destino.get()
    cantidad = traslado_cantidad_entry.get()

    if not sku or not destino or not cantidad:
        messagebox.showwarning("Campos vacíos", "Completa todos los campos de traslado.")
        return

    cantidad = int(cantidad)
    for prod in inventario:
        if prod['sku'] == sku:
            if prod['stock'] >= cantidad:
                prod['stock'] -= cantidad
                nuevo = prod.copy()
                nuevo['stock'] = cantidad
                nuevo['sucursal'] = destino
                inventario.append(nuevo)
                registrar_historial(f"Traslado: {cantidad} x {prod['nombre']} (SKU: {sku}) a {destino}")
                traslado_log.insert(tk.END, f"{cantidad} x {prod['nombre']} trasladado a {destino}\n")
                traslado_sku_entry.delete(0, tk.END)
                traslado_cantidad_entry.delete(0, tk.END)
                traslado_sucursal_destino.set("")
                actualizar_tabla()
                return
            else:
                messagebox.showerror("Stock insuficiente", "No hay suficiente stock para trasladar.")
                return
    messagebox.showerror("Producto no encontrado", "SKU no encontrado.")

# ====================
# INTERFAZ
# ====================
cargar_datos()

root = tk.Tk()
root.title("Sistema de Inventario Empresarial")
root.geometry("980x720")
root.protocol("WM_DELETE_WINDOW", lambda: (guardar_datos(), root.destroy()))

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# --- GESTIÓN DE INVENTARIO ---
frame_inventario = ttk.Frame(notebook)
notebook.add(frame_inventario, text="Gestión de Inventario")

# --- Entradas y botones de Gestión de Inventario ---

tk.Label(frame_inventario, text="SKU").grid(row=0, column=0, sticky="w")
sku_entry = tk.Entry(frame_inventario)
sku_entry.grid(row=0, column=1)

tk.Label(frame_inventario, text="Nombre").grid(row=1, column=0, sticky="w")
nombre_entry = tk.Entry(frame_inventario)
nombre_entry.grid(row=1, column=1)

tk.Label(frame_inventario, text="Precio").grid(row=2, column=0, sticky="w")
precio_entry = tk.Entry(frame_inventario)
precio_entry.grid(row=2, column=1)

tk.Label(frame_inventario, text="Stock").grid(row=3, column=0, sticky="w")
stock_entry = tk.Entry(frame_inventario)
stock_entry.grid(row=3, column=1)

tk.Label(frame_inventario, text="Sucursal").grid(row=4, column=0, sticky="w")
sucursal_entry = ttk.Combobox(frame_inventario, values=sucursales[1:])
sucursal_entry.grid(row=4, column=1)

tk.Button(frame_inventario, text="Agregar Producto", command=agregar_producto).grid(row=5, column=1, pady=5)
tk.Button(frame_inventario, text="Eliminar Producto", command=eliminar_producto).grid(row=5, column=2, pady=5)

# Filtros para tabla inventario
tk.Label(frame_inventario, text="Sucursal:").grid(row=0, column=3, sticky="w")
filtro_sucursal = ttk.Combobox(frame_inventario, values=sucursales)
filtro_sucursal.current(0)
filtro_sucursal.grid(row=0, column=4)
filtro_sucursal.bind("<<ComboboxSelected>>", cambiar_filtro)

tk.Label(frame_inventario, text="Buscar:").grid(row=1, column=3, sticky="w")
buscar_entry = tk.Entry(frame_inventario)
buscar_entry.grid(row=1, column=4)
buscar_entry.bind("<KeyRelease>", lambda e: actualizar_tabla())

cols = ("SKU", "Nombre", "Precio", "Stock", "Sucursal")
tree = ttk.Treeview(frame_inventario, columns=cols, show="headings", height=12)
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=100)
tree.grid(row=6, column=0, columnspan=5, pady=10, padx=10, sticky="nsew")

tk.Button(frame_inventario, text="Resumen del Sistema", command=resumen).grid(row=7, column=2, pady=10)

# --- Pestaña Punto de Venta ---
frame_ventas = ttk.Frame(notebook)
notebook.add(frame_ventas, text="Punto de Venta")

tk.Label(frame_ventas, text="Venta: SKU").grid(row=0, column=0, sticky="w")
venta_sku_entry = tk.Entry(frame_ventas)
venta_sku_entry.grid(row=0, column=1)

tk.Label(frame_ventas, text="Cantidad").grid(row=1, column=0, sticky="w")
venta_cantidad_entry = tk.Entry(frame_ventas)
venta_cantidad_entry.grid(row=1, column=1)

tk.Button(frame_ventas, text="Agregar al Carrito", command=agregar_al_carrito).grid(row=2, column=1, pady=5)
tk.Button(frame_ventas, text="Quitar del Carrito", command=quitar_del_carrito).grid(row=2, column=2, pady=5)

tk.Label(frame_ventas, text="Carrito de Venta").grid(row=3, column=0, columnspan=3)
carrito_cols = ("SKU", "Nombre", "Cantidad", "Precio Unitario", "Total")
carrito_tree = ttk.Treeview(frame_ventas, columns=carrito_cols, show="headings", height=12)
for c in carrito_cols:
    carrito_tree.heading(c, text=c)
    carrito_tree.column(c, width=100)
carrito_tree.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

total_label = tk.Label(frame_ventas, text="Total: $0.00", font=('Arial', 12, 'bold'))
total_label.grid(row=5, column=1)

tk.Button(frame_ventas, text="Confirmar Venta", command=confirmar_venta).grid(row=6, column=1, pady=10)

# --- Pestaña Traslado de Productos ---
frame_traslado = ttk.Frame(notebook)
notebook.add(frame_traslado, text="Traslado de Productos")

tk.Label(frame_traslado, text="SKU Producto").grid(row=0, column=0, sticky="w")
traslado_sku_entry = tk.Entry(frame_traslado)
traslado_sku_entry.grid(row=0, column=1)

tk.Label(frame_traslado, text="Cantidad a trasladar").grid(row=1, column=0, sticky="w")
traslado_cantidad_entry = tk.Entry(frame_traslado)
traslado_cantidad_entry.grid(row=1, column=1)

tk.Label(frame_traslado, text="Sucursal destino").grid(row=2, column=0, sticky="w")
traslado_sucursal_destino = ttk.Combobox(frame_traslado, values=sucursales[1:])
traslado_sucursal_destino.grid(row=2, column=1)

tk.Button(frame_traslado, text="Realizar Traslado", command=trasladar_producto).grid(row=3, column=1, pady=10)

tk.Label(frame_traslado, text="Productos trasladados:").grid(row=4, column=0, sticky="w")
traslado_log = tk.Listbox(frame_traslado, height=10, width=50)
traslado_log.grid(row=5, column=0, columnspan=2, pady=10)

# Ajustar configuración de filas y columnas para que se expanda bien
for frame in (frame_inventario, frame_ventas, frame_traslado):
    for i in range(7):
        frame.rowconfigure(i, weight=1)
    for j in range(5):
        frame.columnconfigure(j, weight=1)

# Inicializar tabla al arrancar
actualizar_tabla()

root.mainloop()