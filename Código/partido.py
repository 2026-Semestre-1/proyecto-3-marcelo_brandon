import random
from seleccion import Seleccion

class Partido:
    """
    descripción: Inicializa los atributos principales de la clase.
    #E: id_partido, equipo_1, equipo_2, fase, fecha
    #S: Instancia
    #R: id_partido debe ser un entero equipo_1 y equipo_2 deben ser herencias de la clase Seleccion fase debe ser un string fecha debe ser un string
    Objetivo: Inicializar un partido.
    """
    def __init__(self, id_partido, equipo_1, equipo_2, fase, fecha):
        if not isinstance(id_partido, int):
            return "Error: id_partido debe ser un entero"
        if not isinstance(equipo_1, Seleccion) or not isinstance(equipo_2, Seleccion):
            return "Error: equipo_1 y equipo_2 deben ser herencias de la clase Seleccion"
        if not isinstance(fase, str):
            return "Error: fase debe ser un string"
        if not isinstance(fecha, str):
            return "Error: fecha debe ser un string"
        self.id_partido = id_partido
        self.equipo_1 = equipo_1
        self.equipo_2 = equipo_2
        self.fase = fase
        self.fecha = fecha
        self.goles_equipo1 = 0
        self.goles_equipo2 = 0
        self.penales_equipo1 = 0
        self.penales_equipo2 = 0
        self.jugado = False
        
    """
    descripción: Lógica principal de un encuentro de 90 minutos.
    #E: Ninguna
    #S: realiza una simulación y asigna goles.
    #R: los equipos debe estar definidos
    Objetivo: Decidir al azar, pero balanceado, los goles y estadísticas de un partido.
    """
    def simular(self):
        fuerza1 = self.equipo_1.fuerza_equipo
        fuerza2 = self.equipo_2.fuerza_equipo
        diferencia = abs(fuerza1 - fuerza2)
        
        if diferencia > 30:
            if fuerza1 > fuerza2:
                self.goles_equipo1 = random.randint(2, 7)
                self.goles_equipo2 = random.randint(0, 3)
            else:
                self.goles_equipo1 = random.randint(0, 3)
                self.goles_equipo2 = random.randint(2, 7)
        elif diferencia > 15:
            if fuerza1 > fuerza2:
                self.goles_equipo1 = random.randint(1, 5)
                self.goles_equipo2 = random.randint(0, 4)
            else:
                self.goles_equipo1 = random.randint(0, 4)
                self.goles_equipo2 = random.randint(1, 5)
        else:
            self.goles_equipo1 = random.randint(0, 4)
            self.goles_equipo2 = random.randint(0, 4)
            
        if self.fase != "Grupos" and self.goles_equipo1 == self.goles_equipo2:
            self.penales_equipo1 = random.randint(2, 5)
            self.penales_equipo2 = random.randint(2, 5)
            while self.penales_equipo1 == self.penales_equipo2:
                self.penales_equipo1 = random.randint(2, 5)
                self.penales_equipo2 = random.randint(2, 5)
                
        if self.goles_equipo1 > 0:
            self._repartir_goles(self.equipo_1, self.goles_equipo1)
        if self.goles_equipo2 > 0:
            self._repartir_goles(self.equipo_2, self.goles_equipo2)
        
        es_grupo = (self.fase == "Grupos")
        self.equipo_1.registrar_resultado(self.goles_equipo1, self.goles_equipo2, random.randint(0, 3), random.randint(0, 1), es_grupo=es_grupo)
        self.equipo_2.registrar_resultado(self.goles_equipo2, self.goles_equipo1, random.randint(0, 3), random.randint(0, 1), es_grupo=es_grupo)
        
        self.jugado = True
        
    """
    descripción: Asigna goles generados a futbolistas específicos.
    #E: equipo, cant_goles
    #S: asigna goles a los jugadores del equipo
    #R: equipo debe ser una herencia de la clase Seleccion cant_goles debe ser un entero mayor a 0
    Objetivo: Dar autoría individual a los tantos marcados por la selección.
    """
    def _repartir_goles(self, equipo, cant_goles):
        if not isinstance(equipo, Seleccion):
            return "Error: equipo debe ser una herencia de la clase Seleccion"
        if not isinstance(cant_goles, int) or cant_goles <= 0:
            return "Error: cant_goles debe ser un entero mayor a 0"
            
        if cant_goles > 0 and len(equipo.jugadores) > 0:
            for _ in range(cant_goles):
                jugador = random.choice(equipo.jugadores)
                jugador.registrar_gol()
               
    """
    descripción: Analiza el marcador para definir al vencedor.
    #E: ninguna
    #S: retorna la selección ganadora o si es empate
    #R: solo se genera despues de simular
    Objetivo: Saber qué equipo se lleva los 3 puntos o avanza de ronda.
    """
    def generar_ganador(self):
        if self.goles_equipo1 > self.goles_equipo2:
            return self.equipo_1
        elif self.goles_equipo2 > self.goles_equipo1:
            return self.equipo_2
        else:
            if self.fase != "Grupos":
                if self.penales_equipo1 > self.penales_equipo2:
                    return self.equipo_1
                else:
                    return self.equipo_2
            return None
            
    """
    descripción: Formatea el resultado (ej. 2 - 1) como string.
    #E: Ninguna
    #S: muestra el resultado
    #R: Ninguna
    Objetivo: Brindar una representación visual clásica de un marcador de fútbol.
    """
    def mostrar_resultado(self):
        resultado = f"{self.equipo_1.pais.nombre} {self.goles_equipo1} - {self.goles_equipo2} {self.equipo_2.pais.nombre}"
        if self.fase != "Grupos" and self.goles_equipo1 == self.goles_equipo2:
            resultado += f" (Penales: {self.penales_equipo1}-{self.penales_equipo2})"
        return resultado

