from Cliente import Cliente

class ClienteJuridico(Cliente):
    """
    Clase que representa a un cliente jurídico. Hereda de la clase Cliente.

    Atributos:
        razon_social (str): Razón social de la empresa o cliente jurídico.
        rif (str): Registro de Información Fiscal del cliente jurídico.
        nombre_contacto (str): Nombre de la persona de contacto asociada al cliente jurídico.
        telf_contacto (str): Teléfono de la persona de contacto.
        correo_contacto (str): Correo electrónico de la persona de contacto.
    """

    def __init__(self, correo, direccion, telefono, razon_social, rif, nombre_contacto, telf_contacto, correo_contacto):
        """
        Constructor para inicializar un cliente jurídico. 
        Incluye los datos generales del cliente (heredados de Cliente) 
        y los específicos de ClienteJuridico.

        Args:
            correo (str): Correo electrónico del cliente.
            direccion (str): Dirección física del cliente.
            telefono (str): Número telefónico del cliente.
            razon_social (str): Razón social del cliente jurídico.
            rif (str): Registro de Información Fiscal del cliente jurídico.
            nombre_contacto (str): Nombre de la persona de contacto.
            telf_contacto (str): Teléfono de la persona de contacto.
            correo_contacto (str): Correo electrónico de la persona de contacto.
        """
        super().__init__(correo, direccion, telefono)
        self.razon_social = razon_social
        self.rif = rif
        self.nombre_contacto = nombre_contacto
        self.telf_contacto = telf_contacto
        self.correo_contacto = correo_contacto

    def show_attr(self):
        """
        Devuelve una representación en texto de los atributos del cliente jurídico,
        incluyendo los generales y los particulares.

        Returns:
            str: Información detallada del cliente jurídico.
        """
        return f'''
Información general: (correo) {self.correo} - (telefono) {self.telefono}
                    (direccion) {self.direccion}

Información particular del Cliente Jurídico:
Razón social: {self.razon_social} - RIF: {self.rif}
Persona de contacto: {self.nombre_contacto} - {self.telf_contacto} - {self.correo_contacto}'''
