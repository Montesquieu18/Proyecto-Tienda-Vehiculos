from datetime import datetime
from ClienteNatural import ClienteNatural

class Pago:
    """
    Clase que representa un pago asociado a una venta en el sistema.

    Atributos:
        fecha (str): Fecha y hora en que se realizó el pago.
        cliente (ClienteNatural | ClienteJuridico): Cliente asociado al pago.
        venta (Venta): Venta asociada al pago.
        monto_pago (float): Monto del pago realizado.
        metodo_pago (str): Método utilizado para realizar el pago (ej. Tarjeta, Efectivo).
        moneda_pago (str): Moneda en la que se realizó el pago.
        estado (bool): Estado del pago (True si está completado, False si está pendiente).
    """

    def __init__(self, cliente, venta, monto_pago, metodo_pago, moneda_pago):
        """
        Inicializa los detalles de un pago.

        Args:
            cliente (ClienteNatural | ClienteJuridico): Cliente que realiza el pago.
            venta (Venta): Objeto de la venta asociada.
            monto_pago (float): Monto total del pago.
            metodo_pago (str): Método de pago utilizado.
            moneda_pago (str): Moneda del pago.
        """
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha y hora actual en formato legible
        self.cliente = cliente 
        self.venta = venta 
        self.monto_pago = monto_pago 
        self.metodo_pago = metodo_pago  
        self.moneda_pago = moneda_pago  
        self.estado = False  # Estado inicial del pago (pendiente)

    def show_client(self):
        """
        Devuelve una representación del cliente dependiendo de su tipo (natural o jurídico).
        
        Returns:
            str: Información del cliente, incluyendo nombre/razón social y cédula/RIF.
        """
        if isinstance(self.cliente, ClienteNatural):  # Si el cliente es natural
            return self.cliente.nombre + " " + self.cliente.cedula
        else:  # Si el cliente es jurídico
            return self.cliente.razon_social + " " + self.cliente.rif

    def show_attr(self):
        """
        Devuelve un resumen detallado del pago, incluyendo estado, fecha, cliente y productos de la venta.

        Returns:
            str: Información estructurada del pago.
        """
        return f'''Información del Pago - Estado: { "Completado" if self.estado else "Pendiente"}
Fecha: {self.fecha} - Monto: {self.monto_pago} - Moneda: {self.moneda_pago} - Tipo: {self.metodo_pago}
Cliente: {self.show_client()}
Productos: {self.venta.show_products()}
'''
