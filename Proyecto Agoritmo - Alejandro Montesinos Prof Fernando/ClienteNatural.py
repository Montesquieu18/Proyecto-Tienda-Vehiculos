from Cliente import Cliente

class ClienteNatural(Cliente):
    """
    Clase que representa a un cliente natural, hereda de la clase Cliente.

    Atributos:
        nombre (str): Nombre completo del cliente.
        cedula (str): Número de cédula del cliente.
    """

    def __init__(self, correo, direccion, telefono, nombre, cedula):
        """
        Inicializa un cliente natural con los datos generales heredados de Cliente,
        y sus datos particulares como nombre y cédula.

        Args:
            correo (str): Correo electrónico del cliente.
            direccion (str): Dirección del cliente.
            telefono (str): Teléfono del cliente.
            nombre (str): Nombre completo del cliente.
            cedula (str): Número de cédula del cliente.
        """
        super().__init__(correo, direccion, telefono)
        self.nombre = nombre
        self.cedula = cedula

    def show_attr(self):
        """
        Devuelve un resumen detallado de los atributos del cliente natural, 
        incluyendo los datos generales heredados y sus datos particulares.

        Returns:
            str: Información estructurada del cliente natural.
        """
        return f'''
Información general: (correo) {self.correo} - (telefono) {self.telefono}
                    (direccion) {self.direccion}

Información particular del Cliente Natural:
Nombre: {self.nombre} - Cedula: {self.cedula}'''
