class Persona:
    """
    descripción: Inicializa los atributos principales de la clase.
    #E: nombre, apellido, fecha_nacimiento, nacionalidad
    #S: inicializa la clase Persona
    #R: nombre debe ser un string apellido debe ser un string fecha_nacimiento debe ser un string nacionalidad debe ser un string
    Objetivo: Establecer el estado inicial del objeto para su correcto funcionamiento en el sistema.
    """
    def __init__(self, nombre, apellido, fecha_nacimiento, nacionalidad):
        if not isinstance (nombre, str):
            return "Error: nombre debe ser un string"
        if not isinstance (apellido, str):
            return "Error: apellido debe ser un string"
        if not isinstance(fecha_nacimiento, str):
            return "Error: fecha_nacimiento debe ser un string"
        if not isinstance (nacionalidad, str):
            return "Error: nacionalidad debe ser un string"
        self.nombre = nombre
        self.apellido = apellido
        self.fecha_nacimiento = fecha_nacimiento
        self.nacionalidad = nacionalidad
        
    """
    descripción: Muestra por consola la información del objeto.
    #E: ninguna
    #S: muestra la información básica de una persona
    #R: debe mostrar un string
    Objetivo: Permitir la visualización rápida del estado y valores actuales de la instancia.
    """
    def mostrar_datos(self):
        print(f"{self.nombre} {self.apellido} ({self.nacionalidad})")

