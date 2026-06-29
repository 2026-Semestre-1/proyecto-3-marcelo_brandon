from pais import Pais
from futbolista import Futbolista
from entrenador import Entrenador

class Seleccion:
    """
    descripción: Inicializa los atributos principales de la clase.
    #E: codigo_equipo, pais
    #S: inicializa a la seleccion
    #R: codigo_equipo debe ser un string
    Objetivo: Establecer el estado inicial del objeto para su correcto funcionamiento en el sistema.
    """
    def __init__(self, codigo_equipo, pais):
        if not isinstance(codigo_equipo, str):
            return "Error: codigo_equipo debe ser un string"
        
        if not isinstance(pais, Pais):
            return "Error: pais debe ser una instancia de la clase Pais"
            
        self.codigo_equipo = codigo_equipo
        self.pais = pais
        self.entrenador = None
        self.jugadores = []
        
        self.total_goles_favor = 0
        self.total_goles_contra = 0
        self.total_tarjetas_amarillas = 0
        self.total_tarjetas_rojas = 0
        self.fuerza_equipo = 0
        
        self.puntos = 0
        self.partidos_jugados = 0
        self.partidos_ganados = 0
        self.partidos_empatados = 0
        self.partidos_perdidos = 0
        
    """
    descripción: Muestra por consola la información del objeto.
    #E: Ninguna
    #S: muestra la información de la selección, entrenador y plantilla.
    #R: debe mostrar un string
    Objetivo: Permitir la visualización rápida del estado y valores actuales de la instancia.
    """
    def mostrar_datos(self):
        print(f"Selección: {self.pais.nombre} ({self.codigo_equipo}) | Fuerza: {self.fuerza_equipo:.2f} | Jugadores: {len(self.jugadores)}")
        if self.entrenador:
            self.entrenador.mostrar_datos()
        else:
            print("Entrenador: Sin entrenador asignado")

    """
    descripción: Vincula un futbolista a la lista de la selección.
    #E: futbolista
    #S: agrega un futbolista a la lista de la selección.
    #R: el maximo de jugadores debe ser 23
    Objetivo: Completar la plantilla oficial de 26 jugadores para el torneo.
    """
    def agregar_jugador(self, futbolista):
        if not isinstance(futbolista, Futbolista):
            return "Error: futbolista debe ser una instancia de la clase Futbolista"
            
        if len(self.jugadores) < 23:
            self.jugadores = self.jugadores + [futbolista]
            self.calcular_fuerza_equipo()
            return True
        return False

    """
    descripción: Saca a un jugador de la plantilla.
    #E: dorsal
    #S: elimina un futbolista segun el dorsal
    #R: dorsal debe ser un entero
    Objetivo: Permitir sustituciones o descartes antes de iniciar la copa.
    """
    def eliminar_jugador(self, dorsal):
        if not isinstance(dorsal, int):
            return "Error: dorsal debe ser un entero"
        encontrado = False
        nueva_lista = []
        for jugador in self.jugadores:
            if jugador.dorsal == dorsal:
                encontrado = True
            else:
                nueva_lista = nueva_lista + [jugador]
        if encontrado:
            self.jugadores = nueva_lista
            self.calcular_fuerza_equipo()
            return True
        return False

    """
    descripción: Coloca a un estratega a cargo de la selección.
    #E: entrenador
    #S: asigna o remplaza al entrenador de un equipo
    #R: Ninguna
    Objetivo: Cumplir el requerimiento de que cada equipo tenga un DT oficial.
    """
    def asignar_entrenador(self, entrenador):
        if not isinstance(entrenador, Entrenador):
            return "Error: entrenador debe ser una instancia de la clase Entrenador"
            
        self.entrenador = entrenador
        self.calcular_fuerza_equipo()

    """
    descripción: Actualiza puntos, goles y partidos de la selección.
    #E: goles_favor, goles_contra, tarjetas_am, tarjetas_roj
    #S: actualiza los totales del equipo tras un partido.
    #R: todos los atributos deben ser enteros mayores o iguales a cero
    Objetivo: Acumular estadísticas vitales tras finalizar cada encuentro.
    """
    def registrar_resultado(self, goles_favor, goles_contra, tarjetas_am, tarjetas_roj, es_grupo=True):
        if not isinstance(goles_favor, int) or goles_favor < 0:
            return "Error: goles_favor inválido"
        if not isinstance(goles_contra, int) or goles_contra < 0:
            return "Error: goles_contra inválido"
        if not isinstance(tarjetas_am, int) or tarjetas_am < 0:
            return "Error: tarjetas_am inválido"
        if not isinstance(tarjetas_roj, int) or tarjetas_roj < 0:
            return "Error: tarjetas_roj inválido"
        
        self.total_goles_favor += goles_favor
        self.total_goles_contra += goles_contra
        self.total_tarjetas_amarillas += tarjetas_am
        self.total_tarjetas_rojas += tarjetas_roj
        self.partidos_jugados += 1
        
        if goles_favor > goles_contra:
            self.partidos_ganados += 1
            if es_grupo:
                self.puntos += 3
        elif goles_favor == goles_contra:
            self.partidos_empatados += 1
            if es_grupo:
                self.puntos += 1
        else:
            self.partidos_perdidos += 1

    """
    descripción: Promedia el puntaje de los 11 mejores jugadores.
    #E: Ninguna
    #S: calcula y actualiza el atributo fuerza_equipo.
    #R: deben haber jugadores registrados
    Objetivo: Obtener una calificación global que influirá en la probabilidad de ganar.
    """
    def calcular_fuerza_equipo(self):
        if len(self.jugadores) == 0:
            self.fuerza_equipo = 0
            return

        """
        descripción: Retorna el puntaje individual de un futbolista.
        #E: jugador
        #S: retorna el puntaje del jugador
        #R: jugador debe ser instancia de Futbolista
        Objetivo: Servir como llave de ordenamiento para encontrar a los mejores 11.
        """
        def obtener_puntaje(jugador):
            return jugador.puntaje_individual
        
        jugadores_ordenados = sorted(self.jugadores, key=obtener_puntaje, reverse=True)
        top_11 = jugadores_ordenados[:11]
        
        suma_puntajes = sum(jugador.puntaje_individual for jugador in top_11)
        promedio_jugadores = suma_puntajes / len(top_11)
        
        factor_entrenador = 0
        if self.entrenador != None:
            factor_entrenador = min(self.entrenador.experiencia_anios * 4, 100)
            
        factor_ranking = 100 - self.pais.ranking_fifa
        if factor_ranking < 0: 
            factor_ranking = 0
        
        self.fuerza_equipo = (promedio_jugadores * 0.6) + (factor_entrenador * 0.25) + (factor_ranking * 0.15)


