from ClienteNatural import ClienteNatural

class Venta:
    """
    Clase que representa una venta realizada en el sistema.

    Atributos:
        id (int): Identificador único de la venta.
        fecha (str): Fecha en la que se realizó la venta.
        cliente (ClienteNatural | ClienteJuridico): Cliente asociado a la venta.
        productos (dict): Productos vendidos con su cantidad (clave: Producto, valor: cantidad).
        metodo_pago (str): Método de pago utilizado.
        metodo_envio (str): Método de envío seleccionado.
        subtotal (float): Subtotal antes de aplicar impuestos y descuentos.
        descuento (float): Descuento aplicado a la venta.
        iva (float): Impuesto al valor agregado.
        igtf (float): Impuesto a las grandes transacciones financieras.
        total (float): Total final a pagar.
    """

    def __init__(self, id, fecha, cliente, productos, metodo_pago, metodo_envio, subtotal, descuento, iva, igtf, total):
        self.id = id
        self.fecha = fecha
        self.cliente = cliente
        self.productos = productos
        self.metodo_pago = metodo_pago
        self.metodo_envio = metodo_envio
        self.subtotal = subtotal
        self.descuento = descuento
        self.iva = iva
        self.igtf = igtf
        self.total = total

    def show_products(self):
        """
        Devuelve una representación detallada de los productos vendidos,
        incluyendo precio por unidad, cantidad y precio total.
        """
        productos = ""
        for producto, cantidad in self.productos.items():
            precio_unitario = producto.precio  # Precio unitario del producto
            precio_total = precio_unitario * cantidad  # Precio total para el producto
            productos += f"\n{producto.nombre}, Precio Por Unidad: ${precio_unitario:.2f}, Cantidad: {cantidad}, Precio Total: ${precio_total:.2f}"
        return productos

    def show_client(self):
        """
        Devuelve información del cliente dependiendo de su tipo (natural o jurídico).
        """
        if isinstance(self.cliente, ClienteNatural):
            return f"{self.cliente.nombre} {self.cliente.cedula}"
        else:
            return f"{self.cliente.razon_social} {self.cliente.rif}"

    def show_attr(self):
        """
        Devuelve un resumen detallado de la venta, incluyendo productos, cliente,
        métodos de pago/envío y desglose de costos.
        """
        return f'''Información de la Venta - ID: {self.id} - Fecha: {self.fecha}
Productos: {self.show_products()}
Cliente: {self.cliente.show_attr()}

Método de Pago: {self.metodo_pago}
Subtotal: {self.subtotal} - Descuento: {self.descuento if self.descuento != 0 else "No aplica"}
IVA: {self.iva} - IGTF: {self.igtf}

----- Total: {self.total}
'''
