import requests
import json
from datetime import datetime, timedelta
from Producto import Producto
from ClienteNatural import ClienteNatural
from ClienteJuridico import ClienteJuridico
from Venta import Venta
from Pago import Pago
from Envio import Envio

class App:
    """
    Clase principal de la aplicación, gestiona la información de clientes, productos, ventas,
    envíos y pagos, incluyendo su persistencia en archivos JSON y la carga de datos desde una API.

    Atributos:
        clientes (list): Lista de clientes (naturales y jurídicos).
        productos (list): Lista de productos disponibles.
        ventas (list): Lista de ventas realizadas.
        envios (list): Lista de envíos realizados.
        pagos (list): Lista de pagos registrados.
    """

    def __init__(self):
        """
        Inicializa la aplicación con listas vacías para clientes, productos, ventas, envíos y pagos.
        """
        self.clientes = []
        self.productos = []
        self.ventas = []
        self.envios = []  
        self.pagos = []

    def cargar_data_api(self):
        """
        Carga datos de productos desde una API y los almacena en la lista de productos.
        La API proporciona información como ID, nombre, descripción, precio, categoría,
        inventario y vehículos compatibles.
        """
        data = requests.get("https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/products.json").json()

        for producto_info in data:
            id = producto_info['id']
            nombre = producto_info['name']
            descripcion = producto_info['description']
            precio = producto_info['price']
            categoria = producto_info['category']
            inventario = producto_info['inventory']
            compatible = []

            for vehiculo in producto_info['compatible_vehicles']:
                compatible.append(vehiculo)
            producto = Producto(id, nombre, descripcion, precio, categoria, inventario, compatible)

            self.productos.append(producto)

    def guardar_JSON(self):     
        """
        Guarda los datos de clientes, productos, ventas, envíos y pagos en archivos JSON.
        Los datos se estructuran según su tipo (ClienteNatural, ClienteJuridico, Venta, Envio, Pago)
        y se almacenan en archivos independientes.
        """
        # Guardar clientes en clientes.json
        clientes_data = []
        for cliente in self.clientes:
            if isinstance(cliente, ClienteNatural):
                clientes_data.append({
                    "tipo": "Natural",
                    "correo": cliente.correo,
                    "direccion": cliente.direccion,
                    "telefono": cliente.telefono,
                    "nombre": cliente.nombre,
                    "cedula": cliente.cedula
                })
            elif isinstance(cliente, ClienteJuridico):
                clientes_data.append({
                    "tipo": "Juridico",
                    "correo": cliente.correo,
                    "direccion": cliente.direccion,
                    "telefono": cliente.telefono,
                    "razon_social": cliente.razon_social,
                    "rif": cliente.rif,
                    "nombre_contacto": cliente.nombre_contacto,
                    "telf_contacto": cliente.telf_contacto,
                    "correo_contacto": cliente.correo_contacto
                })
        with open("clientes.json", "w") as file:
            json.dump(clientes_data, file, indent=4)
        
        # Guardar productos en productos.json
        productos_data = []
        for producto in self.productos:
            productos_data.append({
                "id": producto.id,
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "precio": producto.precio,
                "categoria": producto.categoria,
                "inventario": producto.inventario,
                "compatible_vehicles": producto.compatible
            })
        with open("productos.json", "w") as file:
            json.dump(productos_data, file, indent=4)

        # Guardar ventas en ventas.json
        ventas_data = []
        for venta in self.ventas:
            ventas_data.append({
                "id": venta.id,
                "fecha": venta.fecha,
                "cliente_cedula": venta.cliente.cedula if isinstance(venta.cliente, ClienteNatural) else None,
                "cliente_rif": venta.cliente.rif if isinstance(venta.cliente, ClienteJuridico) else None,
                "productos": [{"id": p.id, "cantidad": c} for p, c in venta.productos.items()],
                "metodo_pago": venta.metodo_pago,
                "metodo_envio": venta.metodo_envio,
                "subtotal": venta.subtotal,
                "descuento": venta.descuento,
                "iva": venta.iva,
                "igtf": venta.igtf,
                "total": venta.total
            })
        with open("ventas.json", "w") as file:
            json.dump(ventas_data, file, indent=4)

        # Guardar envíos en envios.json
        envios_data = []
        for envio in self.envios:
            envios_data.append({
                "cliente_cedula": envio.cliente.cedula if isinstance(envio.cliente, ClienteNatural) else None,
                "cliente_rif": envio.cliente.rif if isinstance(envio.cliente, ClienteJuridico) else None,
                "venta_id": envio.orden_compra.id,
                "servicio_envio": envio.servicio_envio,
                "costo_servicio": envio.costo_servicio,
                "nombre_motorizado": envio.nombre_motorizado,
                "telefono_motorizado": envio.telefono_motorizado,
                "placa_motorizado": envio.placa_motorizado,
                "fecha": envio.fecha_envio,
            })
        with open("envios.json", "w") as file:
            json.dump(envios_data, file, indent=4)

        # Guardar pagos en pagos.json
        pagos_data = []
        for pago in self.pagos:
            pagos_data.append({
                "cliente_cedula": pago.cliente.cedula if isinstance(pago.cliente, ClienteNatural) else None,
                "cliente_rif": pago.cliente.rif if isinstance(pago.cliente, ClienteJuridico) else None,
                "venta_id": pago.venta.id,
                "monto_pago": pago.monto_pago,
                "metodo_pago": pago.metodo_pago,
                "moneda_pago": pago.moneda_pago,
                "estado": pago.estado,
                "fecha": pago.fecha
            })
        with open("pagos.json", "w") as file:
            json.dump(pagos_data, file, indent=4)




    def buscar_pago_pendiente(self, cliente):
        """
        Busca un pago pendiente asociado a un cliente específico.

        Args:
            cliente (ClienteNatural | ClienteJuridico): El cliente cuya lista de pagos será revisada.

        Returns:
            bool: True si existe un pago pendiente, False en caso contrario.
        """
        for pago in self.pagos:
            if pago.cliente == cliente and not pago.estado:  # Verifica si el pago pertenece al cliente y está pendiente
                print(f"\nPAGO PENDIENTE ENCONTRADO: {pago.show_attr()}")
                return True
        return False

    def existe_cedula(self, cedula):
        """
        Verifica si existe un cliente natural registrado con una cédula específica.

        Args:
            cedula (str): La cédula a buscar entre los clientes.

        Returns:
            bool: True si se encuentra un cliente natural con esa cédula, False en caso contrario.
        """
        for cliente in self.clientes:
            if isinstance(cliente, ClienteNatural) and cliente.cedula == cedula:  # Verifica si el cliente es natural y coincide la cédula
                return True
        return False

    def existe_rif(self, rif):
        """
        Verifica si existe un cliente jurídico registrado con un RIF específico.

        Args:
            rif (str): El RIF a buscar entre los clientes.

        Returns:
            bool: True si se encuentra un cliente jurídico con ese RIF, False en caso contrario.
        """
        for cliente in self.clientes:
            if isinstance(cliente, ClienteJuridico) and cliente.rif == rif:  # Verifica si el cliente es jurídico y coincide el RIF
                return True
        return False



    def gestion_productos(self):
        while True:
            print(f'\n GESTIÓN DE PRODUCTOS ')
            opcion = input('''
1 -. Agregar Productos
2 -. Buscar Productos
3 -. Modificar Productos
4 -. Eliminar Productos
5 -. Salir
> Ingrese un número: ''')
            while (not opcion.isnumeric()) or (not int(opcion) in range(1,    6)):
                opcion = input("Opción inválida. Ingrese un número entre 1 y 5\n> Ingrese un número: ")
            
            if opcion == "1":
                self.agregar_productos()
            elif opcion == "2":
                self.buscar_productos()
            elif opcion == "3":
                self.modificar_productos()
            elif opcion == "4":
                self.eliminar_producto()
            else:
                print("\nSaliendo de 'Gestion de Productos'.")
                break 

    def agregar_productos(self):
        """
        Permite agregar un nuevo producto al inventario de productos.

        Solicita al usuario los datos del producto, como nombre, descripción, precio, 
        categoría, inventario y vehículos compatibles. Valida que los datos ingresados 
        sean correctos y agrega el producto a la lista de productos.

        El usuario puede ingresar múltiples vehículos compatibles, verificando que no se repitan.
        """
        while True:
            print("\n AGREGAR PRODUCTO ")

            # Solicita y valida el nombre del producto
            nombre = input("Ingrese el nombre del producto: ")
            while len(nombre) == 0:
                print("No puede estar vacío.")
                nombre = input("Ingrese el nombre del producto: ")

            # Solicita y valida la descripción del producto
            descripcion = input("Ingrese la descripción del producto: ").lower()
            while len(descripcion) == 0:
                print("No puede estar vacío.")
                descripcion = input("Ingrese la descripción del producto: ").lower()

            # Solicita y valida el precio del producto
            while True:
                try:
                    precio = float(input("Ingrese el precio del producto: "))
                    break
                except ValueError:
                    print("Precio inválido. Debe ser un número.")

            # Solicita y valida la categoría del producto
            categoria = input("Ingrese la categoría del producto: ")
            while len(categoria) == 0:
                print("No puede estar vacío.")
                categoria = input("Ingrese la categoría del producto: ")

            # Solicita y valida el inventario del producto
            inventario = input("Ingrese el inventario del producto: ")
            while not inventario.isnumeric() or int(inventario) == 0:
                print("Debe ser un número entero positivo.")
                inventario = input("Ingrese el inventario del producto: ")

            # Permite agregar vehículos compatibles al producto
            compatibilidad = []
            while True:
                print("\n¿Agregar un carro compatible?\n1 -. Si\n2 -. No")
                opcion = input("Ingrese una opción: ")
                while opcion not in ['1', '2']:
                    opcion = input("Error. Ingrese una opción: ")

                if opcion == '1':
                    # Solicita y valida el nombre del vehículo compatible
                    nombre_carro = input("Ingrese el nombre del carro compatible: ")
                    while len(nombre_carro) == 0:
                        print("No puede estar vacío.")
                        nombre_carro = input("Ingrese el nombre del carro compatible: ")

                    # Verifica si el vehículo ya está en la lista
                    if nombre_carro in compatibilidad:
                        print(f'El carro {nombre_carro} ya se encuentra en la lista')
                    else:
                        compatibilidad.append(nombre_carro)

                elif opcion == '2':
                    # Finaliza la edición de vehículos compatibles
                    break

            # Crea un nuevo producto con los datos ingresados y lo agrega al inventario
            producto = Producto(
                len(self.productos), nombre, descripcion, float(precio),
                categoria, int(inventario), compatibilidad
            )
            self.productos.append(producto)
            print("\nProducto Agregado!")
            print(producto.show_attr())

            break  # Finaliza la adición de productos

    def buscar_productos(self):
        """
        Permite realizar búsquedas de productos según diferentes criterios: categoría, rango de precios, 
        coincidencia de nombre y disponibilidad en inventario.

        El usuario selecciona una opción del menú y proporciona los valores necesarios para el criterio
        de búsqueda seleccionado. Los productos encontrados se muestran con su información detallada.
        Si no se encuentran coincidencias, se informa al usuario.
        """
        while True:
            print("\n BUSQUEDA DE PRODUCTOS ")
            opcion = input('''
    1 -. Categoria
    2 -. Precio
    3 -. Nombre
    4 -. Disponibilidad de Inventario
    5 -. Salir
    > Ingrese un número: ''')
            
            # Validación del input del usuario para asegurar que la opción sea válida
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 6)):
                print("Error. Ingrese un número entre 1 y 5.")
                opcion = input("\nIngrese el número correspondiente a la acción que desea realizar: ")
            
            # Opción 1: Buscar productos por categoría
            if opcion == "1":
                categoria_buscar = input("Ingrese la categoría a buscar: ").lower()
                encontrados = [
                    producto for producto in self.productos 
                    if categoria_buscar in producto.categoria.lower()
                ]
                
                if encontrados:
                    print(f"\nDE LA CATEGORÍA '{categoria_buscar.upper()}':")
                    for i, producto in enumerate(encontrados):
                        print(f"{i+1} -. {producto.show_attr()}")
                else:
                    print("No se encontraron productos en esa categoría.")

            # Opción 2: Buscar productos por rango de precios
            elif opcion == "2":
                while True:
                    try:
                        # Solicita el rango de precios y asegura que sean válidos
                        precio_min = float(input("Ingrese el precio mínimo: "))
                        while precio_min < 0:
                            print("Error. Ingrese un precio válido.")
                            precio_min = float(input("Ingrese el precio mínimo: "))

                        precio_max = float(input("Ingrese el precio máximo: "))
                        while precio_max < 0 or precio_max < precio_min:
                            print("Error. Ingrese un precio válido.")
                            if precio_max < precio_min:
                                print("El precio máximo debe ser mayor o igual que el precio mínimo.")
                            precio_max = float(input("Ingrese el precio máximo: "))
                        break
                    except ValueError:
                        print("Por favor ingrese valores numéricos válidos para los precios.")

                encontrados = [
                    producto for producto in self.productos 
                    if precio_min <= producto.precio <= precio_max
                ]

                if encontrados:
                    print(f"\nDE PRECIOS ${precio_min} a ${precio_max}:")
                    for i, producto in enumerate(encontrados):
                        print(f"{i+1} -. {producto.show_attr()}")
                else:
                    print("No se encontraron productos en ese rango de precios.")

            # Opción 3: Buscar productos por nombre
            elif opcion == "3":
                nombre_buscar = input("Ingrese el nombre del producto a buscar: ")
                encontrados = [
                    producto for producto in self.productos 
                    if nombre_buscar.lower() in producto.nombre.lower()
                ]
                
                if encontrados:
                    print(f"\nDE NOMBRE '{nombre_buscar}':")
                    for i, producto in enumerate(encontrados):
                        print(f"{i+1} -. {producto.show_attr()}")
                else:
                    print("No se encontraron productos con ese nombre.")

            # Opción 4: Buscar productos por disponibilidad de inventario
            elif opcion == "4":
                while True:
                    try:
                        # Solicita la cantidad mínima de inventario requerida
                        inventario_min = int(input("Ingrese la cantidad mínima de inventario disponible que busca: "))
                        while not inventario_min >= 0:
                            print("Error. El minimo debe ser un numero entero positivo")
                            inventario_min = int(input("Ingrese la cantidad mínima de inventario disponible que busca: "))
                        break
                    except ValueError:
                        print("Por favor ingrese un número válido para el inventario.")

                encontrados = [
                    producto for producto in self.productos 
                    if producto.inventario >= inventario_min
                ]

                if encontrados:
                    print(f"\nDE INVENTARIO MÍNIMO {inventario_min}")
                    for i, producto in enumerate(encontrados):
                        print(f"{i+1} -. {producto.show_attr()}")
                else:
                    print("No se encontraron productos con ese inventario mínimo.")

            # Opción 5: Salir del menú
            else:
                break


    def modificar_productos(self):
        """
        Permite modificar los atributos de un producto existente en el inventario.

        Funcionalidad:
            - El usuario selecciona un producto de la lista mediante su índice.
            - Muestra un menú para modificar diferentes atributos del producto, incluyendo:
                1. Nombre
                2. Descripción
                3. Categoría
                4. Inventario
                5. Compatibilidad (Agregar o eliminar vehículos compatibles)
            - Valida los datos ingresados para asegurar que sean correctos.
            - Permite al usuario salir del proceso de modificación en cualquier momento.

        Este método garantiza que los datos del producto se mantengan actualizados y consistentes.
        """
        print(f'\n  MODIFICAR PRODUCTO  ')

        # Muestra los productos disponibles para modificación
        for i, producto in enumerate(self.productos):
            print(f"{i+1} -. {producto.nombre}")

        # Solicita al usuario que seleccione un producto por su índice
        indice_producto = input("Ingrese el número del producto que desea modificar: ")
        while not indice_producto.isnumeric() or int(indice_producto) not in range(1, len(self.productos) + 1):
            print(f"Opción inválida. Ingresa un número entre 1 y {len(self.productos)}")
            indice_producto = input("Ingrese el ID del producto que desea modificar: ")

        producto = self.productos[int(indice_producto) - 1]  # Selecciona el producto correspondiente

        # Menú de opciones para modificar los atributos del producto
        while True:
            print(f"\nSe ha seleccionado: {producto.show_attr()}")
            opcion = input('''¿Qué desea modificar?
    1 -. Nombre
    2 -. Descripción
    3 -. Categoría
    4 -. Inventario
    5 -. Compatibilidad
    6 -. Salir
    > Ingrese un número: ''')

            # Valida la opción seleccionada
            while not opcion.isnumeric() or not int(opcion) in range(1, 7):
                print("Opción inválida. Ingrese un número entre 1 y 6)")
                opcion = input('''> Ingrese un número: ''')

            # Modificación del nombre del producto
            if opcion == "1":
                while True:
                    nuevo_nombre = input("Ingrese el nuevo nombre del producto: ")
                    if len(nuevo_nombre) >= 0:
                        producto.nombre = nuevo_nombre
                        print(f"Nombre Actualizado!")
                        break
                    else:
                        print("\nNo debe estar vacío")

            # Modificación de la descripción del producto
            elif opcion == "2":
                while True:
                    nueva_descripcion = input("Ingrese la nueva descripción del producto: ").lower()
                    if len(nueva_descripcion) >= 0:
                        producto.descripcion = nueva_descripcion
                        print(f"Descripción Actualizada!")
                        break
                    else:
                        print("\nNo debe estar vacío.")

            # Modificación de la categoría del producto
            elif opcion == "3":
                while True:
                    nueva_categoria = input("Ingrese la nueva categoría del producto: ")
                    if len(nueva_categoria) >= 0:
                        producto.categoria = nueva_categoria
                        print(f"Categoría Actualizada!")
                        break
                    else:
                        print("\nNo debe estar vacío")

            # Modificación del inventario del producto
            elif opcion == "4":
                while True:
                    nuevo_inventario = input("Ingrese la nueva CANTIDAD DE inventario: ")
                    if nuevo_inventario.isnumeric() and int(nuevo_inventario) >= 0:
                        producto.inventario = int(nuevo_inventario)
                        print(f"Inventario Actualizado!")
                        break
                    else:
                        print("Ingrese un número entero positivo.")

            # Modificación de la lista de compatibilidad del producto
            elif opcion == "5":
                while True:
                    print("\n")
                    print(producto.show_compatibles())
                    print("\nModificar Compatibles\n1 -. Agregar\n2 -. Eliminar\n3 -. Salir")
                    opcion = input("Ingrese una opción: ")
                    while opcion not in ['1', '2', '3']:
                        opcion = input("Error. Ingrese una opción: ")

                    if opcion == '1':  # Agregar un vehículo compatible
                        nombre_carro = input("Ingrese el nombre del carro compatible: ")
                        while len(nombre_carro) == 0:
                            print("No puede estar vacío.")
                            nombre_carro = input("Ingrese el nombre del carro compatible: ")

                        if producto.verificar_vehiculos_compatibles(nombre_carro):
                            print(f'El carro {nombre_carro} ya se encuentra en la lista')
                        else:
                            producto.compatible.append(nombre_carro)

                    elif opcion == '2':  # Eliminar un vehículo compatible
                        if len(producto.compatible) > 0:
                            for i in range(len(producto.compatible)):
                                print(f'{i+1} -. {producto.compatible[i]}')

                            indice_carro = input("Ingrese una opción: ")
                            while not indice_carro.isnumeric() or int(indice_carro) not in range(1, len(producto.compatible) + 1):
                                indice_carro = input("Ingrese una opción VÁLIDA: ")

                            print(f'{producto.compatible[int(indice_carro) - 1]} ELIMINADO')
                            producto.compatible.pop(int(indice_carro) - 1)

                        else:
                            print("No hay vehiculos para eliminar")

                    else:  # Salir del submenú de compatibilidad
                        break

            # Salir del menú de modificación
            elif opcion == "6":
                break

    def eliminar_producto(self):
        while True:
            print(f'\n  ELIMINAR PRODUCTO  ')

            for i, producto in enumerate(self.productos):
                print(f"{i+1} -. {producto.nombre}")

            indice_producto = input("Ingrese el número del producto que desea eliminar: ")

            while not indice_producto.isnumeric() or int(indice_producto) not in range(1, len(self.productos) +1):
                indice_producto = input("Ingrese un número VÁLIDO del producto que desea eliminar: ")

            producto = self.productos[int(indice_producto) - 1]
            self.productos.remove(producto)
            print(f"{producto.nombre.upper()} ELIMINADO.")
            break



    def gestion_ventas(self):
        while True:
            print(f'\n  GESTIÓN DE VENTAS  ')
            opcion = input('''
1 -. Registrar Venta
2 -. Buscar Ventas
3 -. Salir
> Ingrese un número: ''')

            while not opcion.isnumeric() or int(opcion) not in range(1,4):
                print("Opción inválida. Ingrese un número entre 1 y     3)")
                opcion = input("Ingrese un número: ")

            if opcion == "1":
                if len(self.clientes) == 0:
                    print("No hay clientes registrados.")
                else:
                    self.registrar_venta()
            elif opcion == "2":
                if len(self.ventas) == 0:
                    print("No hay ventas registradas.")
                else:
                    self.buscar_ventas()
            else:
                break

    def registrar_venta(self):
        """
        Registra una nueva venta en el sistema, asociándola a un cliente existente y permitiendo
        seleccionar productos disponibles en inventario. Calcula el subtotal, descuentos, IVA, IGTF, 
        y el total de la venta según el método de pago y moneda seleccionados.

        Flujo del método:
            1. Selección de cliente:
            - El usuario elige un cliente de la lista de clientes registrados.
            - Si el cliente tiene pagos pendientes, no se permite registrar la venta.
            2. Selección de productos:
            - Se muestran los productos disponibles con precios e inventario.
            - El usuario selecciona productos, especifica la cantidad deseada y actualiza el inventario.
            3. Determinación del método de pago:
            - Dependiendo del cliente (jurídico o natural), se calcula un descuento o se permite crédito.
            - Se selecciona el tipo de pago (efectivo, Zelle, transferencia, etc.) y la moneda (USD o bolívares).
            4. Método de envío:
            - Se elige el método de envío (Zoom o Delivery).
            5. Cálculo de montos:
            - Calcula descuentos, IVA, IGTF, y el total de la venta.
            6. Registro de la venta:
            - Crea un objeto `Venta` y lo agrega a la lista de ventas.
            7. Registro de pagos:
            - Si el método de pago es crédito, registra el pago inicial y el crédito restante.
            - Si es contado, registra el pago completo.
            8. Registro de envío:
            - Crea un objeto `Envio` asociado a la venta y lo agrega a la lista de envíos.

        Nota:
            - Valida todas las entradas para asegurar que sean correctas (números válidos, cantidades disponibles, etc.).
            - Proporciona mensajes claros al usuario en cada paso del proceso.
        """
        print(f'\n  REGISTRAR VENTA  ')

        # Verifica si hay clientes registrados
        if len(self.clientes) == 0:
            print("Aún no hay clientes registrados.")
            return

        # Selección de cliente
        print("\nPor favor, selecciona un cliente:")
        for i, cliente in enumerate(self.clientes):
            if isinstance(cliente, ClienteNatural):
                print(f"{i+1} -. {cliente.nombre}")
            else:
                print(f"{i+1} -. {cliente.razon_social}")

        indice_cliente = input("Ingrese un número: ")
        while not indice_cliente.isnumeric() or not int(indice_cliente) in range(len(self.clientes) + 1):
            indice_cliente = input("Introduce el número correspondiente al cliente: ")

        cliente = self.clientes[int(indice_cliente) - 1]

        # Verifica si el cliente tiene pagos pendientes
        if self.buscar_pago_pendiente(cliente):
            print("No se puede proceder sin antes efectuar el pago pendiente.")
            return

        # Selección de productos
        productos_seleccionados = {}
        subtotal_venta = 0
        while True:
            for i, producto in enumerate(self.productos):
                print(f"{i+1} -. {producto.nombre}\n{'-'*30}Precio: ${producto.precio:.2f} <<>> Inventario disponible: {producto.inventario}\n")

            indice_producto = input("\nIntroduce el número del producto que desea agregar: ")
            while not indice_producto.isnumeric() or not int(indice_producto) in range(len(self.productos) + 1):
                print("Selección no válida. Ingresa un número correcto.")
                indice_producto = input("Introduce el número del producto que desea agregar: ")

            producto = self.productos[int(indice_producto) - 1]

            # Solicita la cantidad deseada y actualiza inventario
            cantidad = input(f"\n¿Cuántas unidades desea comprar? ")
            while not cantidad.isnumeric() or int(cantidad) <= 0 or int(cantidad) > producto.inventario:
                print(f"Cantidad inválida.")
                cantidad = input(f"¿Cuántas unidades desea comprar? ")

            producto.inventario -= int(cantidad)
            subtotal_venta += producto.precio * int(cantidad)

            if producto in productos_seleccionados:
                productos_seleccionados[producto] += int(cantidad)
            else:
                productos_seleccionados[producto] = int(cantidad)

            continuar = input("¿Agregar otro producto? (s/n): ").lower()
            while continuar not in ["s", "n"]:
                print("Opción no válida. Ingrese 's' para sí o 'n' para no.")
                continuar = input("\n¿Agregar otro producto? (s/n): ").lower()

            if continuar != "s":
                break

        # Métodos de pago para cliente jurídico
        descuento = 0
        if isinstance(cliente, ClienteJuridico):
            metodo_pago = input('''
    ¿Cuál es su método de pago?
    1 -. Pago Contado
    2 -. Crédito
    > Ingresa el número de la opción deseada: ''')

            while not metodo_pago.isnumeric() or int(metodo_pago) not in range(1, 3):
                metodo_pago = input('Error.\nIngresa el número de la opción deseada: ')

            if metodo_pago == "1":
                descuento += subtotal_venta * 0.05
                metodo_pago = "Contado"
            else:
                dias = input("1 -. 15\n2 -. 30\n ¿Dentro de cuántos días realizará el segundo pago?:")
                while not dias.isnumeric() or not int(dias) in range(1, 3):
                    dias = input("Error. Ingresa la cantidad de días: ")

                dias = 15 if dias == '1' else 30
                metodo_pago = "Crédito"
        else:
            metodo_pago = "Contado"

        # Selección de tipo de pago
        tipo_pago = input('''TIPO DE PAGO
    1 -. Punto de Venta (Bolivares)
    2 -. Pago Móvil (Bolivares)
    3 -. Transferencia (Bolivares)
    4 -. Zelle (USD)
    5 -. PayPal (USD)
    6 -. Efectivo (USD)
    > Ingresa un número: ''')

        while not tipo_pago.isnumeric() or not int(tipo_pago) in range(1, 7):
            tipo_pago = input("Error.\nIngresa un número: ")

        moneda, tipo_pago = (
            ("Bolívares", "Punto de Venta") if tipo_pago == "1" else
            ("Bolívares", "Pago móvil") if tipo_pago == "2" else
            ("Bolívares", "Transferencia") if tipo_pago == "3" else
            ("USD", "Zelle") if tipo_pago == "4" else
            ("USD", "PayPal") if tipo_pago == "5" else
            ("USD", "Efectivo")
        )

        # Selección de método de envío
        metodo_envio = input("\nMÉTODO DE ENVÍO:\n1 -. Zoom\n2 -. Delivery\n> Ingresa el número de la opción deseada: ")
        while not metodo_envio.isnumeric() or not int(metodo_envio) in range(1, 3):
            print("Opción no válida. Ingresa un número entre 1 y 2.")
            metodo_envio = input("> Ingresa el número de la opción deseada para el método de envío: ")

        metodo_envio = "Zoom" if metodo_envio == "1" else "Delivery"

        # Cálculo de montos
        iva = (subtotal_venta - descuento) * 0.16
        total_venta = (subtotal_venta - descuento) + iva
        igtf = 0
        if moneda == "USD":
            igtf += total_venta * 0.03

        # Crear y registrar la venta
        nueva_venta = Venta(len(self.ventas), datetime.now().strftime("%Y-%m-%d"), cliente, productos_seleccionados, metodo_pago, metodo_envio, subtotal_venta, descuento, iva, igtf, total_venta)
        print("\n  -- RESUMEN DE LA VENTA --  ")
        print(nueva_venta.show_attr())
        self.ventas.append(nueva_venta)
        print("\nVENTA REGISTRADA.")

        # Registro de pagos
        if metodo_pago == "Crédito":
            monto_inicial = (total_venta / 2)
            igtf = 0
            if moneda == "USD":
                igtf += monto_inicial * 0.03
                monto_inicial += igtf
            self.pago_registrado_venta(nueva_venta, moneda, tipo_pago, monto_inicial, False)
            self.pago_credito_venta(nueva_venta, (monto_inicial - igtf), int(dias))
        else:
            self.pago_registrado_venta(nueva_venta, moneda, tipo_pago, total_venta, True)

        # Registro de envío
        nuevo_envio = Envio(nueva_venta.cliente, nueva_venta, metodo_envio, None, None, None, None)
        self.envios.append(nuevo_envio)
        print("Dirígase al apartado de envíos para enviar su compra")


    def pago_registrado_venta(self, nueva_venta, moneda, tipo_pago, monto, metodo_pago):
        """
        Registra un pago asociado a una venta.

        Args:
            nueva_venta (Venta): Venta para la que se está registrando el pago.
            moneda (str): Moneda del pago (USD o Bolívares).
            tipo_pago (str): Método de pago utilizado (Zelle, Transferencia, etc.).
            monto (float): Monto total del pago.
            metodo_pago (bool): Indica si el pago es inmediato (True) o si es parte de un crédito (False).

        Funcionalidad:
            - Si el método de pago es inmediato, muestra un mensaje indicando el registro del pago.
            - Crea un objeto `Pago` con estado `True` (pagado).
            - Agrega el pago a la lista de pagos registrados y muestra su información.
        """
        if metodo_pago:
            print("\n! REGISTRANDO PAGO !")

        nuevo_pago = Pago(nueva_venta.cliente, nueva_venta, monto, tipo_pago, moneda)
        nuevo_pago.estado = True  # Marca el pago como completado
        self.pagos.append(nuevo_pago)
        print(f'PAGO GENERADO -\n{nuevo_pago.show_attr()}\n')

    def pago_credito_venta(self, nueva_venta, monto_inicial, dias):
        """
        Genera un pago pendiente como parte de un plan de crédito.

        Args:
            nueva_venta (Venta): Venta para la que se está generando el pago pendiente.
            monto_inicial (float): Monto inicial que debe pagarse como parte del crédito.
            dias (int): Plazo en días para efectuar el pago pendiente.

        Funcionalidad:
            - Muestra un mensaje indicando el registro del pago pendiente.
            - Crea un objeto `Pago` con estado `False` (pendiente), sin especificar tipo de pago ni moneda.
            - Calcula la fecha límite para realizar el pago, sumando los días del plazo al día actual.
            - Agrega el pago a la lista de pagos registrados y muestra su información.
        """
        print("\n! REGISTRANDO PAGO PENDIENTE !")
        tipo_pago = None
        moneda = None
        nuevo_pago = Pago(nueva_venta.cliente, nueva_venta, monto_inicial, tipo_pago, moneda)

        # Calcula la fecha límite del pago pendiente
        nueva_fecha = datetime.strptime(nuevo_pago.fecha, "%Y-%m-%d %H:%M:%S") + timedelta(days=dias)
        nuevo_pago.fecha = nueva_fecha.strftime("%Y-%m-%d %H:%M:%S")

        self.pagos.append(nuevo_pago)
        print(f"\nPAGO PENDIENTE GENERADO -\n{nuevo_pago.show_attr()}")
        print(f"PUEDE CANCELAR HASTA DENTRO DE {dias} DÍAS\nACCEDE AL MÓDULO DE PAGOS PARA EFECTUARLO")


    def buscar_ventas(self):
        """
        Permite buscar ventas registradas en el sistema mediante dos criterios: 
        por cliente o por fecha.

        Flujo del método:
            1. Solicita al usuario seleccionar el criterio de búsqueda:
            - **Por Cliente:** Muestra una lista de clientes y permite seleccionar uno. Busca
                y muestra todas las ventas asociadas al cliente seleccionado.
            - **Por Fecha:** Solicita una fecha en formato `YYYY-MM-DD`. Busca y muestra todas 
                las ventas realizadas en la fecha ingresada.
            2. Validaciones:
            - Para la búsqueda por cliente, valida que el índice ingresado sea correcto.
            - Para la búsqueda por fecha, valida el formato y la consistencia de la fecha.
            3. Resultados:
            - Si no se encuentran ventas según el criterio seleccionado, informa al usuario.
            - Si se encuentran ventas, muestra un resumen detallado de cada una.

        Este método organiza las ventas por criterios clave, facilitando el acceso y revisión 
        de información relevante para el usuario.
        """
        print(f'\n  BÚSQUEDA DE VENTAS  ')

        # Selección del criterio de búsqueda
        opcion_busqueda = input('''
    1 -. Por Cliente
    2 -. Por Fecha
    > Ingrese un número: ''')
        while not opcion_busqueda.isnumeric() or not int(opcion_busqueda) in range(1, 3):
            opcion_busqueda = input('''Error.\nIngrese un número: ''')

        if opcion_busqueda == "1":  # Búsqueda por cliente
            print("\n  BÚSQUEDA POR CLIENTE  ")

            # Lista de clientes disponibles para búsqueda
            for i, cliente in enumerate(self.clientes):
                if isinstance(cliente, ClienteNatural):
                    print(f"{i+1} -. {cliente.nombre} - CLIENTE NATURAL")
                else:
                    print(f"{i+1} -. {cliente.razon_social} - CLIENTE JURÍDICO")

            # Selección de cliente
            cliente_indice = input("Seleccione el cliente para buscar sus ventas: ")
            while not cliente_indice.isnumeric() or not int(cliente_indice) in range(1, len(self.clientes) + 1):
                cliente_indice = input("Error.\nSeleccione el cliente para buscar sus ventas: ")

            cliente = self.clientes[int(cliente_indice) - 1]

            # Búsqueda de ventas asociadas al cliente
            ventas_cliente = []
            for venta in self.ventas:
                if venta.cliente == cliente:
                    ventas_cliente.append(venta)

            # Muestra los resultados de la búsqueda por cliente
            if not ventas_cliente:
                print("No se encontraron ventas para este cliente.")
            else:
                print(f"\n CON EL CLIENTE {cliente.nombre if isinstance(cliente,ClienteNatural) else cliente.razon_social}")
                for i, venta in enumerate(ventas_cliente):
                    print(f'{i+1} -. {venta.show_attr()}')

        elif opcion_busqueda == "2":  # Búsqueda por fecha
            print("\n  BÚSQUEDA POR FECHA  ")

            # Solicitud y validación de la fecha
            fecha_busqueda = input("Introduzca la fecha (YYYY-MM-DD): ")
            fecha_lista = fecha_busqueda.split("-")
            while not (fecha_lista[0].isnumeric() or len(fecha_lista[0]) == 4) or \
                    not (fecha_lista[1].isnumeric() or int(fecha_lista[1]) in range(1, 13) or len(fecha_lista[1]) == 2) or \
                    not (fecha_lista[2].isnumeric() or int(fecha_lista[2]) in range(1, 32) or len(fecha_lista[1]) == 2):
                print("Fecha inválida.")
                fecha_busqueda = input("Introduzca la fecha (YYYY-MM-DD): ")
                fecha_lista[0], fecha_lista[1], fecha_lista[2] = fecha_busqueda.split("-")

            fecha = f"{fecha_lista[0]}-{fecha_lista[1]}-{fecha_lista[2]}"

            # Búsqueda de ventas asociadas a la fecha
            ventas_fecha = []
            for venta in self.ventas:
                if venta.fecha.split(" ")[0] == fecha:
                    ventas_fecha.append(venta)

            # Muestra los resultados de la búsqueda por fecha
            if not ventas_fecha:
                print(f"No se encontraron ventas en esta fecha: {fecha}.")
            else:
                print(f"\nDE LA FECHA {fecha}:")
                for i, venta in enumerate(ventas_fecha):
                    print(f'{i+1} -. {venta.show_attr()}')


    def gestion_clientes(self):
        while True:
            print(f'\n  GESTIÓN DE CLIENTES  ')
            opcion = input('''
1 -. Registrar Cliente
2 -. Modificar Cliente
3 -. Eliminar Cliente
4 -. Buscar Cliente
5 -. Salir
> Ingrese un número: ''')

            while not opcion.isnumeric() or not int(opcion) in range(1,6):
                print("Error. Seleccione una opción entre 1 y 5.")
                opcion = input('''> Ingrese un número: ''')

            if opcion == "1":
                self.registrar_cliente()
            elif opcion == "2":
                if len(self.clientes) == 0:
                    print("No hay clientes registrados.")
                else:
                    self.modificar_cliente()
            elif opcion == "3":
                if len(self.clientes) == 0:
                    print("No hay clientes registrados.")
                else:
                    self.eliminar_cliente()
            elif opcion == "4":
                if len(self.clientes) == 0:
                    print("No hay clientes registrados.")
                else:
                    self.buscar_cliente()
            else:
                break

    def registrar_cliente(self):
        """
        Registra un nuevo cliente en el sistema, permitiendo al usuario ingresar los datos
        necesarios y asegurando que sean válidos.

        Flujo del método:
            1. Solicita datos básicos comunes para cualquier cliente (correo, dirección y teléfono),
            validando que sean correctos.
            2. Solicita al usuario seleccionar el tipo de cliente:
            - **Cliente Natural:** Requiere nombre completo y cédula. Valida que la cédula no exista
                previamente y que su longitud sea adecuada.
            - **Cliente Jurídico:** Requiere razón social, RIF, nombre del contacto, teléfono de contacto,
                y correo del contacto. Valida que el RIF no exista previamente, que su formato sea correcto
                y que los datos del contacto sean válidos.
            3. Crea una instancia del cliente correspondiente (`ClienteNatural` o `ClienteJuridico`) y la 
            agrega a la lista de clientes.
            4. Muestra un mensaje de confirmación con los detalles del cliente registrado.

        Validaciones:
            - El correo, dirección y nombre no pueden estar vacíos.
            - El teléfono debe tener exactamente 11 dígitos numéricos.
            - La cédula debe ser única, numérica, y de longitud adecuada.
            - El RIF debe ser único, alfanumérico, y con una longitud mínima.

        Este método asegura que los datos ingresados sean consistentes antes de agregar el cliente.
        """
        print(f'\n  REGISTRAR CLIENTE  ')

        # Solicita y valida datos comunes para cualquier cliente
        correo = input("Ingrese el correo del cliente: ")
        while len(correo) == 0:
            print("No debe estar vacío.")
            correo = input("Ingrese el correo del cliente: ")

        direccion = input("Ingrese la dirección del cliente: ")
        while len(direccion) == 0:
            print("No debe estar vacío.")
            direccion = input("Ingrese la dirección del cliente: ")

        telefono = input("Ingrese el teléfono del cliente: ")
        while not telefono.isnumeric() or len(telefono) != 11:
            print("Debe tener 11 dígitos numéricos")
            telefono = input("Ingrese el teléfono del cliente: ")

        # Selección del tipo de cliente
        opcion = input('''
    1 -. Cliente Natural
    2 -. Cliente Jurídico
    > Seleccione el tipo de cliente: ''')
        while not opcion.isnumeric() or not int(opcion) in range(1, 3):
            print("Opción inválida. Ingrese 1 o 2")
            opcion = input('''> Seleccione el tipo de cliente: ''')

        if opcion == "1":  # Cliente Natural
            # Solicita y valida los datos específicos del cliente natural
            nombre = input("\nIngrese el nombre COMPLETO del cliente: ")
            while len(nombre) == 0:
                print("No debe estar vacío.")
                nombre = input("Ingrese el nombre del cliente: ")

            cedula = input("Ingrese la cédula del cliente: ")
            while not cedula.isnumeric() or self.existe_cedula(cedula) or len(cedula) not in range(6, 9):
                print("Error. Asegúrese de que no existe la cédula ingresada.")
                cedula = input("Ingrese la cédula del cliente: ")

            # Crea una instancia de ClienteNatural
            cliente = ClienteNatural(correo, direccion, telefono, nombre, cedula)
            self.clientes.append(cliente)

        elif opcion == "2":  # Cliente Jurídico
            # Solicita y valida los datos específicos del cliente jurídico
            razon_social = input("\nIngrese la razón social del cliente: ")
            while len(razon_social) == 0:
                print("No debe estar vacío.")
                razon_social = input("Ingrese la razón social del cliente: ")

            rif = input("Ingrese el RIF del cliente: ")
            while not rif.isalnum() or len(rif) < 8 or self.existe_rif(rif):
                print("Error. Asegúrese de que no existe el RIF ingresado.")
                rif = input("Ingrese el RIF del cliente: ")

            nombre_contacto = input("Ingrese el nombre COMPLETO del contacto: ")
            while len(nombre_contacto) == 0:
                print("No debe estar vacío.")
                nombre_contacto = input("Ingrese el nombre COMPLETO del contacto: ")

            telf_contacto = input("Ingrese el teléfono DE CONTACTO: ")
            while not telf_contacto.isnumeric() or len(telf_contacto) != 11:
                print("Debe tener 11 dígitos numéricos")
                telf_contacto = input("Ingrese el teléfono DE CONTACTO: ")

            correo_contacto = input("Ingrese el correo DE CONTACTO: ")
            while len(correo_contacto) == 0:
                print("No debe estar vacío.")
                correo_contacto = input("Ingrese un correo válido para el contacto: ")

            # Crea una instancia de ClienteJuridico
            cliente = ClienteJuridico(correo, direccion, telefono, razon_social, rif, nombre_contacto, telf_contacto, correo_contacto)
            self.clientes.append(cliente)

        # Muestra un mensaje de confirmación
        print("\nCliente registrado.\n")
        print(cliente.show_attr())
        print("\n")

    
    def modificar_cliente(self):
        """
        Permite modificar los datos de un cliente registrado en el sistema, ya sea un cliente natural o jurídico.

        Flujo del método:
            1. Muestra una lista de clientes registrados para que el usuario seleccione uno.
            2. Según el tipo de cliente seleccionado:
            - **Cliente Natural:** Permite modificar dirección, teléfono y correo.
            - **Cliente Jurídico:** Permite modificar dirección, teléfono, correo, nombre del contacto, 
                teléfono del contacto y correo del contacto.
            3. Solicita los nuevos datos, valida que sean correctos, y actualiza el cliente seleccionado.
            4. Muestra mensajes de confirmación tras cada modificación.

        Validaciones:
            - Dirección y correos no pueden estar vacíos.
            - Teléfonos deben tener exactamente 11 dígitos numéricos.
            - Nombre del contacto no puede estar vacío para clientes jurídicos.

        Este método asegura que los datos de los clientes se mantengan actualizados y consistentes.
        """
        print("\n  MODIFICAR CLIENTE  ")

        # Verifica si hay clientes registrados
        if len(self.clientes) == 0:
            print("No hay clientes registrados para modificar.")
            return

        # Muestra la lista de clientes disponibles para modificación
        for i, cliente in enumerate(self.clientes):
            if isinstance(cliente, ClienteNatural):
                print(f"{i+1} -. {cliente.nombre} - CLIENTE NATURAL")
            else:
                print(f"{i+1} -. {cliente.razon_social} - CLIENTE JURÍDICO")

        # Selección de cliente
        seleccion = input("\nSeleccione el número del cliente a modificar: ")
        while not seleccion.isnumeric() or int(seleccion) not in range(1, len(self.clientes) + 1):
            seleccion = input("Error.\nSeleccione el número del cliente a modificar: ")

        cliente_seleccionado = self.clientes[int(seleccion) - 1]

        # Modificación para Cliente Natural
        if isinstance(cliente_seleccionado, ClienteNatural):
            while True:
                print(f'\n  MODIFICAR CLIENTE  ')
                print(f'\n{cliente_seleccionado.show_attr()}')
                opcion = input('''
    1 -. Dirección
    2 -. Teléfono
    3 -. Correo
    4 -. Salir
    > Ingrese un número: ''')
                while not opcion.isnumeric() or not int(opcion) in range(1, 5):
                    print("Opción inválida. Ingrese un número entre 1 y 4.")
                    opcion = input('''> Ingrese un número: ''')

                if opcion == "1":
                    nueva_direccion = input("Ingrese la nueva dirección: ")
                    while len(nueva_direccion) == 0:
                        print("No debe estar vacío.")
                        nueva_direccion = input("Ingrese la nueva dirección: ")
                    cliente_seleccionado.direccion = nueva_direccion
                    print("Dirección modificada!")

                elif opcion == "2":
                    nuevo_telefono = input("Ingrese el nuevo teléfono: ")
                    while not nuevo_telefono.isnumeric() or len(nuevo_telefono) != 11:
                        print("Debe tener 11 dígitos numéricos")
                        nuevo_telefono = input("Ingrese el nuevo teléfono: ")
                    cliente_seleccionado.telefono = nuevo_telefono
                    print("Teléfono modificado exitosamente.")

                elif opcion == "3":
                    nuevo_correo = input("Ingrese el nuevo correo: ")
                    while len(nuevo_correo) == 0:
                        print("No debe estar vacío.")
                        nuevo_correo = input("Ingrese un correo válido: ")
                    cliente_seleccionado.correo = nuevo_correo
                    print("Correo modificado!")

                elif opcion == "4":
                    break

        # Modificación para Cliente Jurídico
        elif isinstance(cliente_seleccionado, ClienteJuridico):
            while True:
                print(f'\n  MODIFICAR CLIENTE JURÍDICO  ')
                print(f'\n{cliente_seleccionado.show_attr()}')
                opcion = input('''
    1 -. Dirección
    2 -. Teléfono
    3 -. Correo
    4 -. Nombre de contacto
    5 -. Teléfono de contacto
    6 -. Correo de contacto
    7 -. Salir
    > Ingrese un número: ''')
                while not opcion.isnumeric() or not int(opcion) in range(1, 8):
                    print("Opción inválida. Ingrese un número entre 1 y 7.")
                    opcion = input('''> Ingrese un número: ''')

                if opcion == "1":
                    nueva_direccion = input("Ingrese la nueva dirección: ")
                    while len(nueva_direccion) == 0:
                        print("No debe estar vacío.")
                        nueva_direccion = input("Ingrese la nueva dirección: ")
                    cliente_seleccionado.direccion = nueva_direccion
                    print("Dirección modificada exitosamente.")

                elif opcion == "2":
                    nuevo_telefono = input("Ingrese el nuevo teléfono: ")
                    while not nuevo_telefono.isnumeric() or len(nuevo_telefono) != 11:
                        print("Debe tener 11 dígitos numéricos")
                        nuevo_telefono = input("Ingrese el nuevo teléfono: ")
                    cliente_seleccionado.telefono = nuevo_telefono
                    print("Teléfono modificado exitosamente.")

                elif opcion == "3":
                    nuevo_correo = input("Ingrese el nuevo correo: ")
                    while len(nuevo_correo) == 0:
                        print("No debe estar vacío.")
                        nuevo_correo = input("Ingrese un correo válido: ")
                    cliente_seleccionado.correo = nuevo_correo
                    print("Correo modificado exitosamente.")

                elif opcion == "4":
                    nuevo_nombre_contacto = input("Ingrese el nuevo nombre de contacto: ")
                    while len(nuevo_nombre_contacto) == 0:
                        print("No debe estar vacío.")
                        nuevo_nombre_contacto = input("Ingrese el nuevo nombre de contacto: ")
                    cliente_seleccionado.nombre_contacto = nuevo_nombre_contacto
                    print("Nombre de contacto modificado exitosamente.")

                elif opcion == "5":
                    nuevo_telf_contacto = input("Ingrese el nuevo teléfono de contacto: ")
                    while not nuevo_telf_contacto.isnumeric() or len(nuevo_telf_contacto) != 11:
                        print("Debe tener 11 dígitos numéricos")
                        nuevo_telf_contacto = input("Ingrese el nuevo teléfono de contacto: ")
                    cliente_seleccionado.telf_contacto = nuevo_telf_contacto
                    print("Teléfono de contacto modificado exitosamente.")

                elif opcion == "6":
                    nuevo_correo_contacto = input("Ingrese el nuevo correo: ")
                    while len(nuevo_correo_contacto) == 0:
                        print("No debe estar vacío.")
                        nuevo_correo_contacto = input("Ingrese un correo válido para el contacto: ")
                    cliente_seleccionado.correo_contacto = nuevo_correo_contacto
                    print("Correo de contacto modificado exitosamente.")

                elif opcion == "7":
                    break

    def eliminar_cliente(self):
        print("\n  ELIMINAR CLIENTE  ")

        # Mostrar los clientes registrados
        if len(self.clientes) == 0:
            print("No hay clientes registrados.")
            return

        print("\nSelecciona el cliente que deseas eliminar:")
        for i, cliente in enumerate(self.clientes):
            if isinstance(cliente, ClienteNatural):
                print(f"{i+1} -. {cliente.nombre} - CLIENTE NATURAL")
            else:
                print(f"{i+1} -. {cliente.razon_social} - CLIENTE JURÍDICO")

        seleccion = input("\nSeleccione el número del cliente a eliminar: ")
        
        while not seleccion.isnumeric() or int(seleccion) not in range(len(self.clientes)+1):
            print("Opción inválida. Por favor, seleccione un cliente válido.")
            seleccion = input("\nSeleccione el número del cliente a eliminar: ")


        cliente_seleccionado = self.clientes[int(seleccion) - 1]

        self.clientes.remove(cliente_seleccionado)
        print(f"\n{cliente_seleccionado.nombre if isinstance(cliente_seleccionado, ClienteNatural) else cliente_seleccionado.razon_social} eliminado.")
        
    def buscar_cliente(self):
        """
        Permite buscar clientes registrados en el sistema mediante dos criterios:
        por identificación (cédula o RIF) o por correo.

        Flujo del método:
            1. Solicita al usuario seleccionar un criterio de búsqueda:
            - **Por Identificación:** Busca un cliente natural o jurídico cuya cédula o RIF coincida con la identificación ingresada.
            - **Por Correo:** Busca un cliente cuyo correo coincida con el ingresado.
            2. Itera sobre la lista de clientes registrados, verificando coincidencias según el criterio seleccionado.
            3. Si encuentra un cliente, muestra su información detallada utilizando el método `show_attr`.
            4. Si no encuentra coincidencias, informa al usuario.
            5. Permite salir del menú de búsqueda seleccionando la opción correspondiente.

        Validaciones:
            - Asegura que la opción seleccionada sea válida (1-3).
            - Los datos ingresados (identificación o correo) se verifican con los clientes registrados.

        Este método facilita encontrar y visualizar información específica de los clientes registrados.
        """
        while True:
            print(f'\n  BÚSQUEDA DE CLIENTES  ')
            opcion = input('''
    1 -. Buscar por Identificación (Cédula/RIF)
    2 -. Buscar por Correo
    3 -. Salir
    > Ingrese un número: ''')

            # Validación de la opción seleccionada
            while not opcion.isnumeric() or int(opcion) not in range(1, 4):
                print("Opción inválida. Ingrese un número entre 1 y 3")
                opcion = input('''> Ingrese un número: ''')

            # Búsqueda por identificación
            if opcion == "1":
                print("\n  BÚSQUEDA POR IDENTIFICACIÓN  ")

                id_cliente = input("\nIngrese la identificación del cliente (cédula/RIF): ")
                cliente_encontrado = False

                # Itera por la lista de clientes y verifica coincidencias con cédula o RIF
                for cliente in self.clientes:
                    if isinstance(cliente, ClienteNatural) and cliente.cedula == id_cliente:
                        cliente_encontrado = True
                        print(f"\nCliente encontrado:\n{cliente.show_attr()}")
                        break
                    elif isinstance(cliente, ClienteJuridico) and cliente.rif == id_cliente:
                        cliente_encontrado = True
                        print(f"\nCliente encontrado:\n{cliente.show_attr()}")
                        break

                if not cliente_encontrado:
                    print("No se encontró ningún cliente con esa identificación.")

            # Búsqueda por correo
            elif opcion == "2":
                print("\n  BÚSQUEDA POR CORREO  ")
                correo = input("Ingrese el correo del cliente: ")
                cliente_encontrado = False

                # Itera por la lista de clientes y verifica coincidencias con el correo
                for cliente in self.clientes:
                    if cliente.correo == correo:
                        cliente_encontrado = True
                        print(f"\nCliente encontrado:\n{cliente.show_attr()}")
                        break

                if not cliente_encontrado:
                    print("No se encontró ningún cliente con esa identificación.")

            # Salida del menú
            else:
                break

    def gestion_pagos(self):
        while True:
            print(f'\n  GESTIÓN DE PAGOS  ')
            opcion = input('''
1 -. Registrar Pago
2 -. Buscar Pagos
3 -. Salir
> Ingrese un número: ''')

            while not opcion.isnumeric() or int(opcion) not in range(1,     4):
                print("Opción inválida. Ingrese un número entre 1 y     3)")
                opcion = input("Ingrese un número: ")

            if opcion == "1":
                self.registrar_pago()  # Función para registrar pago
            elif opcion == "2":
                self.buscar_pagos()  # Función para buscar pagos
            else:
                break
    
    def registrar_pago(self):
        """
        Permite registrar un pago pendiente y actualizar su estado como completado.

        Flujo del método:
            1. Busca todos los pagos pendientes en el sistema.
            - Si no hay pagos pendientes, informa al usuario y finaliza el proceso.
            - Muestra una lista de pagos pendientes con información relevante, como ID de la venta,
                monto a pagar, fecha de vencimiento y estado actual.
            2. Solicita al usuario seleccionar un pago pendiente de la lista.
            - Valida que la opción ingresada sea válida.
            3. Solicita al usuario ingresar el tipo de pago realizado (Punto de Venta, Zelle, etc.) y 
            actualiza la moneda asociada.
            - Valida que la selección del tipo de pago sea correcta.
            4. Actualiza los atributos del pago:
            - Cambia el estado del pago a completado (`True`).
            - Actualiza la fecha del pago a la fecha actual.
            - Registra el tipo de pago y la moneda utilizada.
            5. Muestra un mensaje de confirmación con los detalles del pago actualizado.

        Validaciones:
            - Verifica que existan pagos pendientes antes de iniciar el proceso.
            - Asegura que las selecciones del usuario (pago y tipo de pago) sean válidas.

        Este método asegura que los pagos pendientes se gestionen adecuadamente y que los datos 
        asociados al pago sean consistentes.
        """
        while True:
            print(f'\n  REGISTRAR PAGO  ')
            pagos_pendientes = []
            
            # Busca pagos pendientes
            for pago in self.pagos:
                if not pago.estado:
                    pagos_pendientes.append(pago)

            # Verifica si hay pagos pendientes
            if not pagos_pendientes:
                print("No hay pagos pendientes.")
                break

            # Muestra pagos pendientes
            for i, pago in enumerate(pagos_pendientes):
                print(f"{i+1} -. ID: {pago.venta.id} - MONTO A PAGAR: ${pago.monto_pago:.2f}\n"
                    f"FECHA DE VENCIMIENTO: {pago.fecha} - ESTADO DEL PAGO: PENDIENTE")

            # Selección del pago pendiente a completar
            indice_pago = input("\nIngrese el número del pago PENDIENTE a completar: ")
            while not indice_pago.isnumeric() or not int(indice_pago) in range(1, len(pagos_pendientes) + 1):
                print("Selección inválida. Ingrese un número válido.")
                indice_pago = input("\nIngrese el número del pago PENDIENTE a completar: ")

            pago_seleccionado = pagos_pendientes[int(indice_pago) - 1]

            # Selección del tipo de pago
            tipo_pago = input('''
    TIPO DE PAGO
    1 -. Punto de Venta (Bolivares)
    2 -. Pago Móvil (Bolivares)
    3 -. Transferencia (Bolivares)
    4 -. Zelle (USD)
    5 -. PayPal (USD)
    6 -. Efectivo (USD)
    > Ingresa el número de la opción deseada: ''')
            while not tipo_pago.isnumeric() or not int(tipo_pago) in range(1, 7):
                print("Opción inválida. Ingrese un número entre 1 y 6")
                tipo_pago = input("> Ingrese un número del tipo de pago: ")

            # Asigna tipo de pago y moneda según la selección
            if tipo_pago == "1":
                tipo_pago = "Punto de Venta"
                moneda = "Bolívares"
            elif tipo_pago == "2":
                tipo_pago = "Pago móvil"
                moneda = "Bolívares"
            elif tipo_pago == "3":
                tipo_pago = "Transferencia"
                moneda = "Bolívares"
            elif tipo_pago == "4":
                tipo_pago = "Zelle"
                moneda = "USD"
            elif tipo_pago == "5":
                tipo_pago = "PayPal"
                moneda = "USD"
            else:
                tipo_pago = "Efectivo"
                moneda = "USD"

            # Actualiza el estado del pago
            pago_seleccionado.metodo_pago = tipo_pago
            pago_seleccionado.moneda_pago = moneda
            pago_seleccionado.estado = True
            pago_seleccionado.fecha = datetime.now().strftime("%Y-%m-%d")

            # Muestra el estado actualizado del pago
            print(f'\nESTADO DEL PAGO ACTUALIZADO:\n{pago_seleccionado.show_attr()}')
            break


    def buscar_pagos(self):
        """
        Permite buscar pagos registrados en el sistema según diversos criterios:
        por cliente, por fecha, por tipo de pago, o por moneda utilizada.

        Flujo del método:
            1. Verifica si hay pagos registrados.
            - Si no hay pagos registrados, informa al usuario y finaliza el proceso.
            2. Solicita al usuario seleccionar un criterio de búsqueda:
            - **Por Cliente:** Busca todos los pagos asociados a un cliente seleccionado.
            - **Por Fecha:** Busca todos los pagos realizados en una fecha específica.
            - **Por Tipo de Pago:** Busca pagos según el método utilizado (Zelle, Transferencia, etc.).
            - **Por Moneda:** Busca pagos realizados en una moneda específica (USD o Bolívares).
            3. Según el criterio seleccionado:
            - Filtra y muestra los pagos que cumplen con el criterio.
            - Si no hay coincidencias, informa al usuario.
            4. Permite salir del menú seleccionando la opción correspondiente.

        Validaciones:
            - Verifica que existan pagos registrados antes de iniciar el proceso.
            - Asegura que las entradas del usuario sean válidas (números correctos, formatos adecuados).
            - Para fechas, valida que se ingresen en el formato `YYYY-MM-DD`.

        Este método organiza y facilita la búsqueda de pagos según criterios clave, 
        asegurando una experiencia clara y estructurada para el usuario.
        """
        while True:
            print(f'\n  BUSCAR PAGOS  ')

            # Verifica si hay pagos registrados
            if len(self.pagos) == 0:
                print("No hay pagos registrados.")
                return

            # Solicita al usuario seleccionar un criterio de búsqueda
            opcion = input('''
    1 -. Por Cliente
    2 -. Por Fecha
    3 -. Por Tipo de Pago
    4 -. Por Moneda
    5 -. Salir
    > Seleccione un criterio de búsqueda: ''')
            
            while not opcion.isnumeric() or not int(opcion) in range(1, 6):
                print("Opción inválida. Ingrese un número entre 1 y 5)")
                opcion = input("> Seleccione un criterio de búsqueda: ")

            if opcion == "1":  # Búsqueda por cliente
                print("\n  BÚSQUEDA POR CLIENTE  ")
                for i, cliente in enumerate(self.clientes):
                    if isinstance(cliente, ClienteNatural):
                        print(f"{i+1} -. {cliente.nombre} - CLIENTE NATURAL")
                    else:
                        print(f"{i+1} -. {cliente.razon_social} - CLIENTE JURÍDICO")

                cliente_indice = input("Seleccione el cliente para buscar sus pagos: ")
                while not cliente_indice.isnumeric() or not int(cliente_indice) in range(1, len(self.clientes) + 1):
                    cliente_indice = input("Error.\nSeleccione el cliente para buscar sus pagos: ")

                cliente = self.clientes[int(cliente_indice) - 1]
                pagos_cliente = [pago for pago in self.pagos if pago.cliente == cliente]

                if not pagos_cliente:
                    print("No se encontraron pagos con este cliente.")
                else:
                    print(f"\n CON EL CLIENTE {cliente.nombre if isinstance(cliente, ClienteNatural) else cliente.razon_social}")
                    for i, pago in enumerate(pagos_cliente):
                        print(f'{i+1} -. {pago.show_attr()}')

            elif opcion == "2":  # Búsqueda por fecha
                fecha_busqueda = input("Introduzca la fecha (YYYY-MM-DD): ")
                fecha_lista = fecha_busqueda.split("-")

                while not (fecha_lista[0].isnumeric() or len(fecha_lista[0]) == 4) or \
                        not (fecha_lista[1].isnumeric() or int(fecha_lista[1]) in range(1, 13) or len(fecha_lista[1]) == 2) or \
                        not (fecha_lista[2].isnumeric() or int(fecha_lista[2]) in range(1, 32) or len(fecha_lista[2]) == 2):
                    print("Fecha inválida.")
                    fecha_busqueda = input("Introduzca la fecha (YYYY-MM-DD): ")
                    fecha_lista = fecha_busqueda.split("-")

                fecha = f"{fecha_lista[0]}-{fecha_lista[1]}-{fecha_lista[2]}"
                pagos_fecha = [pago for pago in self.pagos if pago.fecha.split(" ")[0] == fecha]

                if not pagos_fecha:
                    print(f"No se encontraron pagos en esta fecha: {fecha}.")
                else:
                    print(f"\nDE LA FECHA {fecha}:")
                    for i, pago in enumerate(pagos_fecha):
                        print(f'{i+1} -. {pago.show_attr()}')

            elif opcion == "3":  # Búsqueda por tipo de pago
                print("\n  BÚSQUEDA POR TIPO DE PAGO  ")

                tipo_pago = input('''
    1 -. Punto de Venta
    2 -. Pago móvil
    3 -. Transferencia
    4 -. Zelle
    5 -. PayPal
    6 -. Efectivo
    > Selecciona el tipo de pago: ''')
                while not tipo_pago.isnumeric() or int(tipo_pago) not in range(1, 7):
                    print("Opción inválida. Ingrese un número entre 1 y 6)")
                    tipo_pago = input("> Selecciona el tipo de pago: ")

                tipo_seleccionado = {
                    "1": "Punto de Venta",
                    "2": "Pago móvil",
                    "3": "Transferencia",
                    "4": "Zelle",
                    "5": "PayPal",
                    "6": "Efectivo"
                }[tipo_pago]

                pagos_encontrados = [pago for pago in self.pagos if pago.metodo_pago == tipo_seleccionado]

                if pagos_encontrados:
                    print(f"\nDEL TIPO '{tipo_seleccionado}':")
                    for i, pago in enumerate(pagos_encontrados):
                        print(f"{i+1} -. {pago.show_attr()}")
                else:
                    print(f"No se encontraron pagos del tipo '{tipo_seleccionado}'.")

            elif opcion == "4":  # Búsqueda por moneda
                print("\n  BÚSQUEDA POR MONEDA DE PAGO  ")

                moneda = input("1 -. USD\n2 -. Bolivares\n> Selecciona la moneda: ")
                while not moneda.isnumeric() or int(moneda) not in range(1, 3):
                    print("Opción inválida. Ingrese un 1 o 2")
                    moneda = input("Selecciona la moneda: ")

                moneda_seleccionada = "USD" if moneda == "1" else "Bolivares"
                pagos_encontrados = [pago for pago in self.pagos if pago.moneda_pago and pago.moneda_pago.lower() == moneda_seleccionada.lower()]

                if pagos_encontrados:
                    print(f"\nDEL LA MONEDA '{moneda_seleccionada}':")
                    for i, pago in enumerate(pagos_encontrados):
                        print(f"{i+1} -. {pago.show_attr()}")
                else:
                    print(f"No se encontraron pagos en la moneda '{moneda_seleccionada}'.")

            else:  # Salir
                break

    def gestion_envios(self):
        while True:
            print("\n  GESTIÓN DE ENVÍOS  ")
            opcion = input('''
1 -. Registrar envío
2 -. Buscar envíos
3 -. Salir
> Ingrese un número: ''')
            
            while not opcion.isnumeric() or not int(opcion) in range(1,4):
                print("Opción inválida. Ingrese un número entre 1 y 3)")
                opcion = input("> Ingrese un número: ")

            if opcion == "1":
                if len(self.ventas) == 0:
                    print("No hay ventas a ser enviadas")
                else:
                    self.registrar_envio()
            elif opcion == "2":
                if len(self.envios) == 0:
                    print("No hay envíos registrados para buscar")
                else:
                    self.buscar_envios()
            else:
                break

    def registrar_envio(self):
        """
        Permite registrar un envío pendiente de una venta, actualizando su estado y 
        registrando detalles del servicio de envío.

        Flujo del método:
            1. Identifica envíos pendientes:
            - Busca en la lista de envíos aquellos que aún no han sido completados.
            - Si no hay envíos pendientes, informa al usuario y finaliza el proceso.
            2. Muestra las ventas con envíos pendientes y solicita al usuario seleccionar una.
            3. Según el método de envío:
            - Si el método es "delivery", solicita al usuario los datos del motorizado 
                (nombre, teléfono y placa).
            - Solicita el costo del servicio de envío.
            4. Actualiza el estado del envío a completado (`True`) y guarda los datos ingresados.
            5. Muestra un mensaje confirmando que el envío ha sido actualizado y completado.

        Validaciones:
            - Verifica que existan envíos pendientes antes de iniciar el proceso.
            - Asegura que la selección del usuario sea válida (número del envío).
            - Valida que el costo del servicio sea un valor numérico.

        Este método asegura que los envíos pendientes sean gestionados adecuadamente, 
        registrando información relevante y actualizando su estado.
        """
        while True:
            print("\n  REGISTRAR ENVÍO  ")

            # Busca envíos pendientes
            envios_pendientes = []
            for envio in self.envios:
                if not envio.estado:
                    envios_pendientes.append(envio)

            # Verifica si hay envíos pendientes
            if not envios_pendientes:
                print("No hay ventas pendientes de envío.")
                return

            # Muestra envíos pendientes
            print("VENTAS CON ENVÍOS PENDIENTES:")
            for i, envio in enumerate(envios_pendientes):
                print(f"{i+1} -. {envio.orden_compra.show_attr()}")

            # Selección del envío
            seleccion = input("\nSelecciona el número del envío que deseas efectuar: ")
            while not seleccion.isnumeric() or int(seleccion) not in range(1, len(envios_pendientes) + 1):
                seleccion = input("Error.\nSelecciona el número del envío que deseas efectuar: ")

            envio_seleccionado = envios_pendientes[int(seleccion) - 1]

            # Solicita datos adicionales si el método de envío es "delivery"
            metodo_envio = envio_seleccionado.servicio_envio
            if metodo_envio.lower() == "delivery":
                print("\n  INFORMACIÓN DEL MOTORIZADO  ")
                envio.nombre_motorizado = input("Introduce el nombre del motorizado: ")
                envio.telefono_motorizado = input("Introduce el teléfono del motorizado: ")
                envio.placa_motorizado = input("Introduce la placa del motorizado: ")

            # Solicita el costo del servicio de envío
            while True:
                try:
                    costo_servicio = float(input("Introduce el costo del servicio de envío: $"))
                    envio.costo_servicio = costo_servicio
                    break
                except ValueError:
                    print("Precio inválido\n")

            # Actualiza el estado del envío
            envio_seleccionado.estado = True
            print("\nEnvio Actualizado! Su compra está en camino...")
            break

    def buscar_envios(self):
        """
        Permite buscar envíos registrados en el sistema según dos criterios:
        por cliente o por fecha.

        Flujo del método:
            1. Verifica si hay envíos registrados.
            - Si no hay envíos registrados, informa al usuario y finaliza el proceso.
            2. Solicita al usuario seleccionar un criterio de búsqueda:
            - **Por Cliente:** Muestra una lista de clientes registrados. Permite seleccionar 
                un cliente y muestra los envíos asociados a este.
            - **Por Fecha:** Solicita una fecha en formato `YYYY-MM-DD` y muestra los envíos realizados
                en dicha fecha.
            3. Filtra los envíos según el criterio seleccionado y muestra los resultados.
            4. Permite salir del menú seleccionando la opción correspondiente.

        Validaciones:
            - Verifica que existan envíos registrados antes de iniciar el proceso.
            - Asegura que las selecciones del usuario sean válidas (número del cliente o formato de fecha).
            - Informa al usuario si no se encuentran envíos que coincidan con el criterio seleccionado.

        Este método organiza y facilita la búsqueda de envíos registrados en el sistema, 
        proporcionando información clara y estructurada.
        """
        while True:
            print(f'\n  BUSCAR ENVÍOS  ')

            # Verifica si hay envíos registrados
            if len(self.envios) == 0:
                print("No hay envíos registrados.")
                return

            # Solicita al usuario seleccionar un criterio de búsqueda
            opcion = input('''
    1 -. Por Cliente
    2 -. Por Fecha
    3 -. Salir
    > Seleccione un criterio de búsqueda: ''')
            while not opcion.isnumeric() or not int(opcion) in range(1, 4):
                opcion = input('Error.\nSeleccione un criterio de búsqueda: ')

            if opcion == '1':  # Búsqueda por cliente
                print("\n  BÚSQUEDA POR CLIENTE  ")
                for i, cliente in enumerate(self.clientes):
                    if isinstance(cliente, ClienteNatural):
                        print(f"{i+1} -. {cliente.nombre} - CLIENTE NATURAL")
                    else:
                        print(f"{i+1} -. {cliente.razon_social} - CLIENTE JURÍDICO")

                # Selección del cliente
                cliente_indice = input("Seleccione el cliente para buscar sus envíos: ")
                while not cliente_indice.isnumeric() or not int(cliente_indice) in range(1, len(self.clientes) + 1):
                    cliente_indice = input("Error.\nSeleccione el cliente para buscar sus envíos: ")

                cliente = self.clientes[int(cliente_indice) - 1]
                envios_cliente = [envio for envio in self.envios if envio.cliente == cliente]

                # Muestra los resultados de la búsqueda
                if not envios_cliente:
                    print("No se encontraron envíos con este cliente.")
                else:
                    print(f"\nCON EL CLIENTE {cliente.nombre if isinstance(cliente, ClienteNatural) else cliente.razon_social}")
                    for i, envio in enumerate(envios_cliente):
                        print(f'{i+1} - {envio.show_attr()}')

            elif opcion == '2':  # Búsqueda por fecha
                fecha_busqueda = input("Introduzca la fecha (YYYY-MM-DD): ")
                fecha_lista = fecha_busqueda.split("-")

                # Validación del formato de fecha
                while not (fecha_lista[0].isnumeric() or len(fecha_lista[0]) == 4) or \
                        not (fecha_lista[1].isnumeric() or int(fecha_lista[1]) in range(1, 13) or len(fecha_lista[1]) == 2) or \
                        not (fecha_lista[2].isnumeric() or int(fecha_lista[2]) in range(1, 32) or len(fecha_lista[2]) == 2):
                    print("Fecha inválida.")
                    fecha_busqueda = input("Introduzca la fecha (YYYY-MM-DD): ")
                    fecha_lista = fecha_busqueda.split("-")

                fecha = f"{fecha_lista[0]}-{fecha_lista[1]}-{fecha_lista[2]}"
                envios_fecha = [envio for envio in self.envios if envio.fecha.split(" ")[0] == fecha]

                # Muestra los resultados de la búsqueda
                if not envios_fecha:
                    print(f"No se encontraron envíos en esta fecha: {fecha}.")
                else:
                    print(f"\nDE LA FECHA {fecha}:")
                    for i, envio in enumerate(envios_fecha):
                        print(f'{i+1} -. {envio.show_attr()}')

            else:  # Salir
                break


    def estadisticas(self):
        """
        Proporciona estadísticas del sistema en tres áreas principales: ventas, pagos y envíos.

        Flujo del método:
            1. Presenta un menú principal con opciones para acceder a informes de ventas, pagos o envíos.
            2. Según la selección del usuario:
            - **Informes de Ventas:**
                - Ventas totales (pendiente de implementación).
                - Productos más vendidos (muestra los tres productos más vendidos).
                - Clientes frecuentes (muestra los tres clientes con más compras).
            - **Informes de Pagos:**
                - Pagos totales (pendiente de implementación).
                - Clientes con pagos pendientes (lista los clientes con pagos incompletos).
            - **Informes de Envíos:**
                - Envíos totales (pendiente de implementación).
                - Productos más enviados (muestra los tres productos más enviados).
                - Clientes con envíos pendientes (lista los clientes con pedidos pendientes de envío).
            3. Incluye validaciones para garantizar que las selecciones del usuario sean correctas.
            4. Permite salir del menú seleccionando la opción correspondiente.

        Validaciones:
            - Verifica que las entradas del usuario sean números válidos dentro del rango permitido.
            - Informa al usuario si no hay datos suficientes para generar ciertas estadísticas.

        Este método organiza y resume información clave del sistema, facilitando la visualización de estadísticas importantes.
        """
        while True:
            print("\n GESTIÓN DE ESTADÍSTICAS ")
            opcion = input('''
    1 -. Informes Ventas
    2 -. Informes Pagos
    3 -. Informes Envíos
    4 -. Salir
    > Ingrese un número''')

            # Validación de la selección principal
            while not opcion.isnumeric() or int(opcion) not in range(1, 5):
                opcion = input("Error.\nIngrese un número: ")

            if opcion == "1":  # Informes de ventas
                while True:
                    print("\n INFORMES DE VENTAS ")
                    print("1 -. Ventas totales\n2 -. Productos más vendidos\n3 -. Clientes frecuentes\n4 -. Salir")
                    opcion = input("\n> Ingrese el número de la opción deseada:  ")

                    while not opcion.isnumeric() or not int(opcion) in range(1, 5):
                        print("Error. Selección inválida.")
                        opcion = input("> Ingrese el número de la opción deseada:  ")

                    if opcion == "1":
                        print("Pendiente...")  # Ventas totales (por implementar)

                    elif opcion == "2":  # Productos más vendidos
                        print("\n 3 PRODUCTOS MÁS VENDIDOS ")
                        productos = {}
                        for venta in self.ventas:
                            for producto, cantidad in venta.productos.items():
                                if producto.nombre not in productos:
                                    productos[producto.nombre] = cantidad
                                else:
                                    productos[producto.nombre] += cantidad

                        for i in range(min(3, len(productos))):
                            max_cantidad = None
                            nombre_producto = ""
                            for producto, cantidad in productos.items():
                                if max_cantidad is None or cantidad > max_cantidad:
                                    max_cantidad = cantidad
                                    nombre_producto = producto

                            print(f"{i + 1}. {nombre_producto.upper()}: {max_cantidad}")
                            del productos[nombre_producto]
                        print("\n")

                    elif opcion == "3":  # Clientes frecuentes
                        print("\n 3 CLIENTES MÁS FRECUENTES")
                        clientes = {}
                        for venta in self.ventas:
                            if venta.cliente not in clientes:
                                clientes[venta.cliente] = 1
                            else:
                                clientes[venta.cliente] += 1

                        for i in range(min(3, len(clientes))):
                            frecuencia = None
                            cliente = ""
                            for cliente_obj, frecuencia_compra in clientes.items():
                                if frecuencia is None or frecuencia_compra > frecuencia:
                                    frecuencia = frecuencia_compra
                                    cliente = cliente_obj

                            print(f"{i + 1}. {cliente.show_attr()} --> {frecuencia}")
                            del clientes[cliente]

                    else:  # Salir de informes de ventas
                        break

            elif opcion == "2":  # Informes de pagos
                while True:
                    print("\n INFORMES DE PAGOS ")
                    print("1 -. Ver pagos totales\n2 -. Ver clientes con pagos pendientes\n3 -. Salir")
                    opcion = input("\n> Ingrese el número de la opción deseada:  ")

                    while not opcion.isnumeric() or not int(opcion) in range(1, 4):
                        print("Error. Selección inválida.")
                        opcion = input("> Ingrese el número de la opción deseada:  ")

                    if opcion == "1":
                        print("Pendiente...")  # Pagos totales (por implementar)

                    elif opcion == "2":  # Clientes con pagos pendientes
                        print("\n PAGOS PENDIENTES ")
                        clientes_con_pagos_pendientes = [pago.cliente for pago in self.pagos if not pago.estado]

                        if clientes_con_pagos_pendientes:
                            for i, cliente in enumerate(clientes_con_pagos_pendientes):
                                print(f"\n{i+1}. {cliente.show_attr()}\n{'='*30}")
                        else:
                            print("No hay clientes con pagos pendientes.")

                    else:  # Salir de informes de pagos
                        break

            elif opcion == "3":  # Informes de envíos
                while True:
                    print("\n INFORMES ENVÍOS ")
                    print("1 -. Envíos totales\n2 -. Productos más enviados\n3 -. Clientes con envíos pendientes\n4 -. Salir")
                    opcion = input("\n> Ingrese el número de la opción deseada:  ")

                    while not opcion.isnumeric() or not int(opcion) in range(1, 5):
                        print("Error. Selección inválida.")
                        opcion = input("> Ingrese el número de la opción deseada:  ")

                    if opcion == "1":
                        print("Pendiente")  # Envíos totales (por implementar)

                    elif opcion == "2":  # Productos más enviados
                        productos = {}
                        for envio in self.envios:
                            for producto, cantidad in envio.orden_compra.productos.items():
                                if producto.nombre not in productos:
                                    productos[producto.nombre] = cantidad
                                else:
                                    productos[producto.nombre] += cantidad

                        print("\n 3 PRODUCTOS MÁS ENVIADOS ")
                        for i in range(min(3, len(productos))):
                            max_cantidad = None
                            nombre_producto = ""
                            for product, quantity in productos.items():
                                if max_cantidad is None or max_cantidad < quantity:
                                    max_cantidad = quantity
                                    nombre_producto = product

                            print(f'{i + 1}). {nombre_producto.upper()}: {max_cantidad}')
                            del productos[nombre_producto]

                    elif opcion == "3":  # Clientes con envíos pendientes
                        print("\n ENVÍOS PENDIENTES ")
                        envios_pendientes = [envio.cliente for envio in self.envios if not envio.estado]

                        if envios_pendientes:
                            for i, cliente in enumerate(envios_pendientes):
                                print(f'\n{i+1}) {cliente.show_attr()}\n')
                        else:
                            print("No hay clientes con envíos pendientes...")

                    else:  # Salir de informes de envíos
                        break

            else:  # Salir del menú de estadísticas
                break
    
    
    def start(self):
        print('\nCargando datos de la API\n')
        self.cargar_data_api()

        while True:
            print("\nTIENDA DE VEHÍCULOS - MENÚ")
            opcion = input('''
1 -. Gestión de productos    
2 -. Gestión de ventas       
3 -. Gestión de clientes     
4 -. Gestión de pagos        
5 -. Gestión de envíos       
6 -. Gestión de estadísticas 
7 -. Salir                   

> Ingrese un número: ''')
            while (not opcion.isnumeric()) or (not int(opcion) in range(1, 8)):
                opcion = input("Debe ingresar el número de la opción deseada.> Ingrese un número: ")
            if opcion == "1":
                self.gestion_productos()
            elif opcion == "2":
                self.gestion_ventas()
            elif opcion == "3":
                self.gestion_clientes()
            elif opcion == "4":
                self.gestion_pagos()
            elif opcion == "5":
                self.gestion_envios()
            elif opcion == "6":
                self.estadisticas()
            else:
                self.guardar_JSON()
                print("\nHasta Luego!")
                break