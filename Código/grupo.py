from partido import Partido
from seleccion import Seleccion

class Grupo:
    """
    descripción: Inicializa los atributos principales de la clase.
    #E: nombre_grupo
    #S: inicializa atributos de la clase Grupo
    #R: nombre_grupo debe ser un string
    Objetivo: Establecer el estado inicial del objeto para su correcto funcionamiento en el sistema.
    """
    def __init__(self, nombre_grupo):
        if not isinstance(nombre_grupo, str):
            return "Error: nombre_grupo debe ser un string"  
        self.nombre_grupo = nombre_grupo
        self.equipos = []
        self.partidos = []

    """
    descripción: Añade una selección a un grupo específico.
    #E: seleccion
    #S: agrega una selección al grupo
    #R: seleccion debe ser de la clase Seleccion en cada lista de equipos solo pueden haber 4 equipos.
    Objetivo: Formar los grupos que competirán en la primera fase del mundial.
    """
    def agregar_equipo(self, seleccion):
        if not isinstance(seleccion, Seleccion):
            return "Error: seleccion debe ser un objeto de la clase Seleccion"
            
        if len(self.equipos) < 4:
            self.equipos = self.equipos + [seleccion]
            return True
        return False

    """
    descripción: Genera y simula los enfrentamientos del grupo.
    #E: Ninguna
    #S: simula los partidos entre los equipos de una misma lista
    #R: Deben haber equipos
    Objetivo: Determinar los resultados y puntos de la fase de grupos.
    """
    def jugar_partidos(self):
        equipo1 = self.equipos[0]
        equipo2 = self.equipos[1]
        equipo3 = self.equipos[2]
        equipo4 = self.equipos[3]

        partido1 = Partido(1, equipo1, equipo2, "Grupos", "Fecha Simulada")
        partido1.simular()
        self.partidos = self.partidos + [partido1]

        partido2 = Partido(2, equipo3, equipo4, "Grupos", "Fecha Simulada")
        partido2.simular()
        self.partidos = self.partidos + [partido2]
        
        partido3 = Partido(3, equipo1, equipo3, "Grupos", "Fecha Simulada")
        partido3.simular()
        self.partidos = self.partidos + [partido3]
        
        partido4 = Partido(4, equipo2, equipo4, "Grupos", "Fecha Simulada")
        partido4.simular()
        self.partidos = self.partidos + [partido4]
        
        partido5 = Partido(5, equipo1, equipo4, "Grupos", "Fecha Simulada")
        partido5.simular()
        self.partidos = self.partidos + [partido5]
        
        partido6 = Partido(6, equipo2, equipo3, "Grupos", "Fecha Simulada")
        partido6.simular()
        self.partidos = self.partidos + [partido6]

    """
    descripción: Ordena a los equipos del grupo según sus puntos.
    #E: Ninguna
    #S: rrdena equipos por puntos y diferencia de goles.
    #R: Ninguna
    Objetivo: Definir las posiciones finales para saber quién clasifica.
    """
    def calcular_tabla(self):
        largo = len(self.equipos)
        for i in range(largo):
            for j in range(0, largo - i - 1):
                e1 = self.equipos[j]
                e2 = self.equipos[j + 1]
                dif1 = e1.total_goles_favor - e1.total_goles_contra
                dif2 = e2.total_goles_favor - e2.total_goles_contra
                cambiar = False
                if e1.puntos < e2.puntos:
                    cambiar = True
                elif e1.puntos == e2.puntos:
                    if dif1 < dif2:
                        cambiar = True
                    elif dif1 == dif2:
                        if e1.total_goles_favor < e2.total_goles_favor:
                            cambiar = True      
                if cambiar:
                    temp = self.equipos[j]
                    self.equipos[j] = self.equipos[j + 1]
                    self.equipos[j + 1] = temp

    """
    descripción: Calcula y retorna los equipos que superaron la fase.
    #E: Ninguna
    #S: retorna los 2 mejores equipos
    #R: deben haberse jugado los partidos
    Objetivo: Determinar qué selecciones avanzan a la siguiente etapa del torneo.
    """
    def obtener_clasificados(self):
        return self.equipos[:2] if len(self.equipos) >= 2 else self.equipos

    """
    descripción: Imprime la tabla de posiciones del grupo.
    #E: Ninguna
    #S: retorna la tabla de posiciones
    #R: Ninguna
    Objetivo: Proveer una representación visual de la clasificación del grupo.
    """
    def mostrar_tabla(self):
        self.calcular_tabla()
        resultado = f"--- {self.nombre_grupo} ---\n"
        resultado += f"{'Pos':<3} | {'Selección':<15} | {'Pts':<3} | {'PJ':<2} | {'PG':<2} | {'PE':<2} | {'PP':<2} | {'GF':<2} | {'GC':<2} | {'DG':<3} | {'TA':<2} | {'TR':<2}\n"
        resultado += "-" * 85 + "\n"
        for i in range(len(self.equipos)):
            eq = self.equipos[i]
            dg = eq.total_goles_favor - eq.total_goles_contra
            resultado += f"{i+1:<3} | {eq.pais.nombre[:15]:<15} | {eq.puntos:<3} | {eq.partidos_jugados:<2} | {eq.partidos_ganados:<2} | {eq.partidos_empatados:<2} | {eq.partidos_perdidos:<2} | {eq.total_goles_favor:<2} | {eq.total_goles_contra:<2} | {dg:<3} | {eq.total_tarjetas_amarillas:<2} | {eq.total_tarjetas_rojas:<2}\n"
        return resultado

