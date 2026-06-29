from partido import Partido
from seleccion import Seleccion

class Fase:
    """
    descripción: Inicializa los atributos principales de la clase.
    #E: nombre_fase
    #S: inicializa los atributos de la clase Fase
    #R: nombre_fase debe ser un string
    Objetivo: Establecer el estado inicial del objeto para su correcto funcionamiento en el sistema.
    """
    def __init__(self, nombre_fase):
        if not isinstance(nombre_fase, str):
            return "Error: nombre_fase debe ser un string"
        self.nombre_fase = nombre_fase
        self.partidos = []
        self.clasificados = []
    """
    descripción: Añade un partido a la fase actual.
    #E: equipo1, equipo2
    #S: crea partido y lo agrega a la fase
    #R: equipo1 y equipo2 deben ser de la clase Seleccion
    Objetivo: Mantener el control de los enfrentamientos que conforman una fase.
    """
    def registrar_juego(self, equipo1, equipo2):
        if not isinstance(equipo1, Seleccion) or not isinstance(equipo2, Seleccion):
            return "Error: Los equipos deben ser instancias de Seleccion" 
        partido = Partido(len(self.partidos)+1, equipo1, equipo2, self.nombre_fase, "Fecha Fase")
        self.partidos = self.partidos + [partido]

    """
    descripción: Simula todos los partidos programados en la fase.
    #E: Ninguna
    #S: simula partidos
    #R: Ninguna
    Objetivo: Avanzar el torneo determinando los resultados de un conjunto de partidos.
    """
    def jugar_fase(self):
        self.clasificados = []
        for partido in self.partidos:
            partido.simular()
            ganador = partido.generar_ganador()
            if ganador:
                self.clasificados = self.clasificados + [ganador]
    """
    descripción: Imprime en pantalla los partidos de la fase.
    #E: ninguna
    #S: Muestra resultados de la fase como string.
    #R: ninguna
    Objetivo: Facilitar la visualización del calendario y resultados de la etapa.
    """
    def mostrar_juegos(self):
        resultado = f"--- {self.nombre_fase} ---\n"
        for partido in self.partidos:
            resultado += partido.mostrar_resultado() + "\n"
        return resultado
    """
    descripción: Calcula y retorna los equipos que superaron la fase.
    #E: ninguna
    #S: retorna lista de los ganadores
    #R: ninguna
    Objetivo: Determinar qué selecciones avanzan a la siguiente etapa del torneo.
    """
    def obtener_clasificados(self):
        return self.clasificados

