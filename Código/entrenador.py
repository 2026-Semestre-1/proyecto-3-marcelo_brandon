from persona import Persona

class Entrenador(Persona):
    """
    descripción: Inicializa los atributos principales de la clase.
    #E: nombre, apellido, fecha_nacimiento, nacionalidad, licencia, experiencia_anios, sistema_juego
    #S: Inicializa la clase Entrenador
    #R: licencia debe ser string la experiencia_anios debe ser un entero mayor o igual a 0 el sistema_juego debe ser un string
    Objetivo: Establecer el estado inicial del objeto para su correcto funcionamiento en el sistema.
    """
    def __init__(self, nombre, apellido, fecha_nacimiento, nacionalidad, licencia, experiencia_anios, sistema_juego):
        if not isinstance(licencia, str):
            return "Error: licencia debe ser un string"
        if not isinstance(experiencia_anios, int) or experiencia_anios < 0:
            return "Error: experiencia_anios debe ser un entero mayor o igual a 0"
        if not isinstance(sistema_juego, str):
            return "Error: sistema_juego debe ser un string"
        Persona.__init__(self, nombre, apellido, fecha_nacimiento, nacionalidad)
        self.licencia = licencia
        self.experiencia_anios = experiencia_anios
        self.sistema_juego = sistema_juego

    """
    descripción: Muestra por consola la información del objeto.
    #E: Ninguna
    #S: imprime la información de un entrenador
    #R: debe mostrar un string
    Objetivo: Permitir la visualización rápida del estado y valores actuales de la instancia.
    """
    def mostrar_datos(self):
        print(f"Entrenador: {self.nombre} {self.apellido} ({self.nacionalidad}) | Licencia: {self.licencia} | Años de experiencia: {self.experiencia_anios} años | Sistema de juego: {self.sistema_juego}")

    """
    descripción: Actualiza los atributos específicos de la instancia.
    #E: licencia, experiencia_anios, sistema_juego
    #S: Actualiza los datos del entrenador
    #R: licencia debe ser string experiencia_anios debe ser un entero mayor o igual a 0 sistema_juego debe ser un string
    Objetivo: Permitir la modificación dinámica de los datos del objeto en tiempo de ejecución.
    """
    def actualizar_datos(self, licencia, experiencia_anios, sistema_juego):
        if not isinstance(licencia, str):
            return "Error: licencia debe ser un string"
        if not isinstance(experiencia_anios, int) or experiencia_anios < 0:
            return "Error: experiencia_anios debe ser un entero mayor o igual a 0"
        if not isinstance(sistema_juego, str):
            return"Error: sistema_juego debe ser un string"   
        self.licencia = licencia
        self.experiencia_anios = experiencia_anios
        self.sistema_juego = sistema_juego

