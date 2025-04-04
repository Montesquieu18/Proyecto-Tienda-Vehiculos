class Cliente:
    """
    Clase base que representa un cliente, con atributos generales compartidos 
    por clientes naturales y jurídicos.

    Atributos:
        correo (str): Correo electrónico del cliente.
        direccion (str): Dirección física del cliente.
        telefono (str): Número telefónico del cliente.
    """

    def __init__(self, correo, direccion, telefono):
        """
        Constructor para inicializar un cliente con información básica.

        Args:
            correo (str): Correo electrónico del cliente.
            direccion (str): Dirección física del cliente.
            telefono (str): Número telefónico del cliente.
        """
        self.correo = correo
        self.direccion = direccion
        self.telefono = telefono
