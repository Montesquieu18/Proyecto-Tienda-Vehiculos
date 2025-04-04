from datetime import datetime

class Envio:
    """
    Clase que representa el envío de una orden de compra a un cliente.

    Atributos:
        fecha_envio (str): Fecha en que se realiza el envío, formato YYYY-MM-DD.
        cliente (ClienteNatural | ClienteJuridico): Cliente asociado al envío.
        orden_compra (Venta): Orden de compra asociada al envío.
        servicio_envio (str): Servicio de envío utilizado (ej. Delivery).
        costo_servicio (float): Costo asociado al servicio de envío.
        nombre_motorizado (str): Nombre del motorizado asignado al envío.
        telefono_motorizado (str): Teléfono del motorizado asignado.
        placa_motorizado (str): Placa del vehículo utilizado para el envío.
        estado (bool): Estado del envío (True si está completado, False si está pendiente).
    """

    def __init__(self, cliente, orden_compra, servicio_envio, costo_servicio, nombre_motorizado, telefono_motorizado, placa_motorizado):
        """
        Inicializa los detalles de un envío, asignando datos del cliente, orden de compra, 
        servicio utilizado y motorizado en caso de que aplique. 
        El estado del envío inicia como pendiente.
        """
        self.fecha_envio = datetime.now().strftime("%Y-%m-%d")
        self.cliente = cliente
        self.orden_compra = orden_compra
        self.servicio_envio = servicio_envio
        self.costo_servicio = costo_servicio
        self.nombre_motorizado = nombre_motorizado
        self.telefono_motorizado = telefono_motorizado
        self.placa_motorizado = placa_motorizado
        self.estado = False

    def show_motorizado(self):
        """
        Devuelve información del motorizado asignado si el servicio de envío es "delivery".
        Si no aplica, devuelve "No asignado".
        """
        if self.servicio_envio.lower() == "delivery":
            return f"{self.nombre_motorizado} - {self.telefono_motorizado}\nPLACA: {self.placa_motorizado}"
        return "No asignado"

    def show_attr(self):
        """
        Devuelve un resumen estructurado del envío, incluyendo fecha, servicio, costo, 
        datos del motorizado y detalles del cliente.
        """
        return f'''- ENVÍO -
Fecha: {self.fecha_envio}
Servicio: {self.servicio_envio} - Costo: {self.costo_servicio}
Motorizado: {self.show_motorizado()}
Cliente: {self.cliente.show_attr()}'''
