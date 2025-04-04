class Producto:
    """
    Clase que representa un producto en el sistema.

    Atributos:
        id (int): Identificador único del producto.
        nombre (str): Nombre del producto.
        descripcion (str): Descripción detallada del producto.
        precio (float): Precio unitario del producto.
        categoria (str): Categoría a la que pertenece el producto.
        inventario (int): Cantidad de productos disponibles en inventario.
        compatible (list): Lista de vehículos compatibles con el producto.
    """

    def __init__(self, id, nombre, descripcion, precio, categoria, inventario, compatible):
        """
        Inicializa un producto con los datos básicos y compatibilidades.

        Args:
            id (int): Identificador único del producto.
            nombre (str): Nombre del producto.
            descripcion (str): Descripción del producto.
            precio (float): Precio del producto.
            categoria (str): Categoría a la que pertenece.
            inventario (int): Cantidad disponible en inventario.
            compatible (list): Lista de vehículos compatibles.
        """
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria
        self.inventario = inventario
        self.compatible = compatible

    def show_compatibles(self):
        """
        Devuelve una lista enumerada de vehículos compatibles con el producto.
        
        Returns:
            str: Lista de vehículos enumerada o "No aplica" si no hay compatibilidades.
        """
        info_compatibles = ""
        for i in range(len(self.compatible)):  # Recorre los vehículos compatibles
            info_compatibles += f"\t{i+1}. {self.compatible[i]}\n"  # Agrega un vehículo con su índice
        return info_compatibles

    def verificar_vehiculos_compatibles(self, nombre):
        """
        Verifica si un vehículo específico es compatible con el producto.

        Args:
            nombre (str): Nombre del vehículo a verificar.

        Returns:
            bool: True si el vehículo es compatible, False en caso contrario.
        """
        for carro in self.compatible:  # Itera sobre la lista de vehículos compatibles
            if carro.lower() == nombre.lower():  # Compara sin diferenciar mayúsculas/minúsculas
                return True
        return False  # Devuelve False si no se encuentra compatibilidad

    def show_attr(self):
        """
        Devuelve un resumen detallado del producto, incluyendo su inventario y vehículos compatibles.

        Returns:
            str: Información estructurada del producto.
        """
        return f'''Información del Producto - ID: {self.id}
Nombre: {self.nombre} - Precio: {self.precio} - Categoría: {self.categoria}
Descripción: {self.descripcion}

Inventario: {self.inventario}

Vehículos Compatibles:
{self.show_compatibles() if len(self.compatible) else "No aplica"}'''
