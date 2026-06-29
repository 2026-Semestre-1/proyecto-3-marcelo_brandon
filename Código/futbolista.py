from persona import Persona

class Futbolista(Persona):
    """
    descripción: Inicializa los atributos principales de la clase.
    #E: nombre, apellido, fecha_nacimiento, nacionalidad, dorsal, posicion, puntaje_individual
    #S: Instancia de Futbolista
    #R: puntaje_individual debe ser un entero entre 1 y 100 dorsal debe ser un entero entre 1 y 99 posicion debe ser un string
    Objetivo: Establecer el estado inicial del objeto para su correcto funcionamiento en el sistema.
    """
    def __init__(self, nombre, apellido, fecha_nacimiento, nacionalidad, dorsal, posicion, puntaje_individual):
        if not isinstance(dorsal, int) or dorsal < 1 or dorsal > 99:
            return "Error: dorsal debe ser un entero entre 1 y 99"
        if not isinstance(posicion, str):
            return "Error: posicion debe ser un string"
        if not isinstance(puntaje_individual, int) or puntaje_individual < 1 or puntaje_individual > 100:
            return "Error: puntaje_individual debe ser un entero entre 1 y 100"
        Persona.__init__(self, nombre, apellido, fecha_nacimiento, nacionalidad)
        self.dorsal = dorsal
        self.posicion = posicion
        self.total_tarjetas_amarillas = 0
        self.total_tarjetas_rojas = 0
        self.goles = 0
        self.asistencias = 0
        self.puntaje_individual = puntaje_individual

    """
    descripción: Muestra por consola la información del objeto.
    #E: ninguna
    #S: sobrescribe el método de Persona para incluir los atributos del futbolista
    #R: debe mostrar un string
    Objetivo: Permitir la visualización rápida del estado y valores actuales de la instancia.
    """
    def mostrar_datos(self):
        base = Persona.mostrar_datos(self)
        print(f"#{self.dorsal} {base} - {self.posicion} (Puntaje: {self.puntaje_individual}) | Goles: {self.goles}")
        
    """
    descripción: Actualiza los atributos específicos de la instancia.
    #E: dorsal, posicion, puntaje_individual
    #S: modifica los atributos básicos del jugador.
    #R: dorsal debe ser un entero entre 1 y 99 posicion debe ser un string puntaje_individual debe ser un entero entre 1 y 100
    Objetivo: Permitir la modificación dinámica de los datos del objeto en tiempo de ejecución.
    """
    def actualizar_datos(self, dorsal, posicion, puntaje_individual):
        if not isinstance(dorsal, int) or dorsal < 1 or dorsal > 99:
            return "Error: dorsal debe ser un entero entre 1 y 99"
        if not isinstance(posicion, str):
            return "Error: posicion debe ser un string"
        if not isinstance(puntaje_individual, int) or puntaje_individual < 1 or puntaje_individual > 100:
            return "Error: puntaje_individual debe ser un entero entre 1 y 100"
            
        self.dorsal = dorsal
        self.posicion = posicion
        self.puntaje_individual = puntaje_individual

    """
    descripción: Aumenta el contador de goles del jugador.
    #E: ninguna
    #S: aumenta en 1 el contador de goles
    #R: ninguna
    Objetivo: Llevar la estadística individual de anotaciones actualizada.
    """
    def registrar_gol(self):
        self.goles += 1

    """
    descripción: Aumenta el contador de asistencias del jugador.
    #E: Ninguna
    #S: aumenta en 1 el contador de asistencias.
    #R: ninguna
    Objetivo: Llevar la estadística individual de pases a gol.
    """
    def registrar_asistencia(self):
        self.asistencias += 1

    """
    descripción: Registra una tarjeta amarilla o roja recibida.
    #E: tipo
    #S: aumenta en 1 el contador de tarjetas amarillas o rojas.
    #R: tipo debe ser válido ("amarilla" o "roja")
    Objetivo: Mantener el historial disciplinario del futbolista durante el torneo.
    """
    def registrar_tarjeta(self, tipo):
        if not isinstance(tipo, str):
            return "Error: tipo debe ser un string"
            
        if tipo.lower() == "amarilla":
            self.total_tarjetas_amarillas += 1
        elif tipo.lower() == "roja":
            self.total_tarjetas_rojas += 1
        else:
            return "Error: tipo de tarjeta inválido"


