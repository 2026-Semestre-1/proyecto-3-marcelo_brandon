import random
from grupo import Grupo
from fase import Fase
from pais import Pais
from seleccion import Seleccion

class Mundial:
    """
    descripción: Inicializa los atributos principales de la clase.
    #E: nombre, anio
    #S: inicializa los atributos de la clase Mundial
    #R: nombre debe ser un string anio debe ser un entero
    Objetivo: Establecer el estado inicial del objeto para su correcto funcionamiento en el sistema.
    """
    def __init__(self, nombre, anio):
        if not isinstance(nombre, str):
            return "Error: nombre debe ser un string"
        if not isinstance(anio, int):
            return "Error: anio debe ser un entero"
        self.nombre = nombre
        self.anio = anio
        self.paises = []
        self.selecciones = []
        self.grupos = []
        self.fases = []
        self.campeon = None
    """
    descripción: Valida y guarda un nuevo país ingresado.
    #E: pais
    #S: agrega un país al mundial
    #R: pais debe ser de la clase Pais
    Objetivo: Procesar la entrada del formulario y almacenar la nación en memoria.
    """
    def registrar_pais(self, pais):
        if not isinstance(pais, Pais):
            return "Error: pais debe ser de la clase Pais"
        self.paises = self.paises + [pais]
    """
    descripción: Procesa el formulario y añade una selección.
    #E: seleccion
    #S: agrega una selección al torneo
    #R: seleccion debe ser de la clase Seleccion
    Objetivo: Validar y registrar un equipo nacional en el sistema.
    """
    def registrar_seleccion(self, seleccion):
        if not isinstance(seleccion, Seleccion):
            return "Error: seleccion debe ser de la clase Seleccion"
        self.selecciones = self.selecciones + [seleccion]
    """
    descripción: Arma las estructuras de grupo a partir de las selecciones.
    #E: cantidad_grupos
    #S: organiza selecciones en grupos
    #R: cantidad_grupos debe ser un entero mayor o igual a 2
    Objetivo: Agrupar a los equipos aleatoriamente para iniciar el torneo.
    """
    def crear_grupos(self, cantidad_grupos):
        if not isinstance(cantidad_grupos, int) or cantidad_grupos < 2:
            return "Error: cantidad_grupos debe ser un entero mayor o igual a 2"   
        self.grupos = []
        nombres_grupos = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        for i in range(cantidad_grupos):
            nombre_oficial = "Grupo " + nombres_grupos[i]
            nuevo_grupo = Grupo(nombre_oficial)
            self.grupos = self.grupos + [nuevo_grupo]
        selecciones_mezcladas = self.selecciones.copy()
        random.shuffle(selecciones_mezcladas)
        posicion = 0
        for equipo in selecciones_mezcladas:
            grupo_actual = self.grupos[posicion]
            if len(grupo_actual.equipos) < 4:
                grupo_actual.agregar_equipo(equipo)
            posicion = posicion + 1
            if posicion == cantidad_grupos:
                posicion = 0
    """
    descripción: Orquesta la simulación iterativa de cada grupo.
    #E: ninguna
    #S: juega y calcula las tablas
    #R: n inguna
    Objetivo: Obtener la lista inicial de 16 equipos clasificados.
    """
    def jugar_fase_grupos(self):
        for grupo in self.grupos:
            grupo.jugar_partidos()
            grupo.calcular_tabla()

    """
    descripción: Crea las llaves de emparejamiento directo.
    #E: nombre_fase, clasificados
    #S: crea enfrentamientos de fase
    #R: nombre_fase debe ser un string clasificados debe ser una lista
    Objetivo: Enfrentar a las selecciones sobrevivientes según las reglas del torneo.
    """
    def armar_fase_eliminatoria(self, nombre_fase, clasificados):
        if not isinstance(nombre_fase, str):
            return "Error: nombre_fase debe ser un string"
        if not isinstance(clasificados, list):
            return "Error: clasificados debe ser una lista" 
        fase = Fase(nombre_fase)
        cantidad = len(clasificados)
        mitad = cantidad // 2
        for i in range(mitad):
            equipo_1 = clasificados[i]
            posicion_rival = (cantidad - 1) - i
            equipo_2 = clasificados[posicion_rival]
            fase.registrar_juego(equipo_1, equipo_2)
        self.fases = self.fases + [fase]
        return fase

    """
    descripción: Ejecuta una ronda a muerte súbita.
    #E: fase
    #S: ejecuta jugar_fase y retorna los equipos clasificados
    #R: fase debe ser de la clase Fase
    Objetivo: Reducir a la mitad la cantidad de selecciones en la competencia.
    """
    def jugar_fase_eliminatoria(self, fase):
        if not isinstance(fase, Fase):
            return "Error: fase debe ser un objeto de la clase Fase"  
        fase.jugar_fase()
        return fase.obtener_clasificados()

    """
    descripción: Ejecuta todas las fases eliminatorias hasta la final.
    #E: ninguna
    #S: ejecuta el flujo completo desde grupos hasta final
    #R: ninguna
    Objetivo: Descubrir al ganador definitivo del campeonato mundial.
    """
    def determinar_campeon(self):
        self.jugar_fase_grupos()
        clasificados = []
        for grupo in self.grupos:
            clasificados = clasificados + grupo.obtener_clasificados() 
        while len(clasificados) > 1:
            largo = len(clasificados)
            if largo >= 32:
                nombre = "Dieciseisavos de Final"
            elif largo >= 16:
                nombre = "Octavos de Final"
            elif largo >= 8:
                nombre = "Cuartos de Final"
            elif largo >= 4:
                nombre = "Semifinales"
            else:
                nombre = "Final"
                
            fase = self.armar_fase_eliminatoria(nombre, clasificados)
            clasificados = self.jugar_fase_eliminatoria(fase)
        self.campeon = clasificados[0]
    """
    descripción: Genera el ranking ordenado de todas las selecciones.
    #E: ninguna
    #S: muestra la tabla general
    #R: Ninguna
    Objetivo: Otorgar la clasificación del primer al último lugar del torneo.
    """
    def mostrar_tabla_general(self):
        resultado = ""
        for grupo in self.grupos:
            resultado += grupo.mostrar_tabla() + "\n"
        return resultado
    """
    descripción: Calcula todas las métricas globales del mundial.
    #E: ninguna
    #S: genera archivo de estadísticas
    #R: ninguna
    Objetivo: Recopilar goleadores, porteros y equipos más goleadores para exportar.
    """
    def generar_reporte(self):
        from archivos import Archivos
        gestor = Archivos(".")
        gestor.guardar_paises(self.paises)
        gestor.guardar_selecciones(self.selecciones)
        gestor.guardar_jugadores(self.selecciones)
        gestor.guardar_rankings(self.selecciones)
        todos_los_partidos = []
        for grupo in self.grupos:
            todos_los_partidos = todos_los_partidos + grupo.partidos
        for fase in self.fases:
            todos_los_partidos = todos_los_partidos + fase.partidos
        gestor.guardar_partidos(todos_los_partidos)
        return "Reportes .txt generados exitosamente en la carpeta 'datos'"


