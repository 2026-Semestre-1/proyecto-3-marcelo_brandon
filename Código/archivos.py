import os
from pais import Pais
from seleccion import Seleccion
from entrenador import Entrenador
from futbolista import Futbolista
from partido import Partido

class Archivos:
    """
    descripción: Inicializa los atributos principales de la clase.
    #E: ruta_base
    #S: inicializa el gestor de archivos
    #R: ruta_base debe ser un string
    Objetivo: Establecer el estado inicial del objeto para su correcto funcionamiento en el sistema.
    """
    def __init__(self, ruta_base):
        if not isinstance(ruta_base, str):
            return "Error: ruta_base debe ser un string"
            
        self.ruta_datos = os.path.join(ruta_base, "datos")
        if not os.path.exists(self.ruta_datos):
            os.makedirs(self.ruta_datos)   

    """
    descripción: Divide una cadena de texto utilizando un separador.
    #E: linea, separador
    #S: Retorna una lista con las palabras separadas
    #R: linea y separador deben ser strings
    Objetivo: Obtener los elementos individuales a partir de una línea de texto procesada.
    """
    def separar_linea(self, linea, separador):
        largo = len(linea)
        if largo > 0:
            ultima_letra = linea[largo - 1]
            if ultima_letra == '\n':
                linea = linea[0 : largo - 1]
        partes = []
        palabra_actual = ""
        for letra in linea:
            if letra == separador:
                partes = partes + [palabra_actual]
                palabra_actual = ""
            else:
                palabra_actual = palabra_actual + letra
        partes = partes + [palabra_actual]
        
        return partes

    """
    descripción: Obtiene la ruta absoluta para acceder a un archivo de datos.
    #E: archivo
    #S: retorna la ruta completa del archivo.
    #R: archivo debe ser un string
    Objetivo: Asegurar que la lectura y escritura de archivos ocurra en el directorio correcto.
    """
    def conseguir_ruta(self, archivo):
        if not isinstance(archivo, str):
            return "Error: archivo debe ser un string"
        return os.path.join(self.ruta_datos, archivo)

    """
    descripción: Guarda la lista de países en el archivo correspondiente.
    #E: paises
    #S: guarda la lista de países en un txt
    #R: paises debe ser una lista
    Objetivo: Persistir la información de los países registrados de forma permanente.
    """
    def guardar_paises(self, paises):
        if not isinstance(paises, list):
            return "Error: paises debe ser una lista"
        try:
            with open(self.conseguir_ruta("paises.txt"), "w", encoding="utf-8") as f:
                for p in paises:
                    f.write(f"{p.codigo_fifa},{p.nombre},{p.continente},{p.ranking_fifa}\n")
        except Exception as e:
            print(f"Error guardando paises: {e}")

    """
    descripción: Lee los datos de países desde el disco al sistema.
    #E: ninguna
    #S: lee el txt y retorna una lista de países
    #R: ninguna
    Objetivo: Poblar el sistema con los datos de países previamente guardados.
    """
    def cargar_paises(self):
        paises = []
        ruta = self.conseguir_ruta("paises.txt")
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    for linea in f:
                        partes = self.separar_linea(linea, ",")
                        if len(partes) == 4:
                            p = Pais(partes[0], partes[1], partes[2], int(partes[3]))
                            paises = paises + [p]
            except Exception as e:
                print(f"Error cargando paises: {e}")
        return paises

    """
    descripción: Guarda la lista de selecciones en el archivo de texto.
    #E: selecciones
    #S: guarda la lista de selecciones en un txt
    #R: selecciones debe ser una lista
    Objetivo: Persistir la información y configuraciones de las selecciones de forma permanente.
    """
    def guardar_selecciones(self, selecciones):
        if not isinstance(selecciones, list):
            return "Error: selecciones debe ser una lista"
        try:
            with open(self.conseguir_ruta("selecciones.txt"), "w", encoding="utf-8") as f:
                for seleccion in selecciones:
                    entrenador_data = "None"
                    if seleccion.entrenador:
                        e = seleccion.entrenador
                        entrenador_data = f"{e.nombre}|{e.apellido}|{e.fecha_nacimiento}|{e.nacionalidad}|{e.licencia}|{e.experiencia_anios}|{e.sistema_juego}"
                    f.write(f"{seleccion.codigo_equipo},{seleccion.pais.codigo_fifa},{entrenador_data},{seleccion.fuerza_equipo}\n")
        except Exception as e:
            print(f"Error guardando selecciones: {e}")

    """
    descripción: Lee los datos de selecciones desde el almacenamiento.
    #E: paises
    #S: lee el txt y retorna una lista de selecciones
    #R: paises debe ser una lista
    Objetivo: Cargar las selecciones existentes para ser usadas en el torneo.
    """
    def cargar_selecciones(self, paises):
        if not isinstance(paises, list):
            return "Error: paises debe ser una lista"   
        selecciones = []
        ruta = self.conseguir_ruta("selecciones.txt")
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    for linea in f:
                        partes = self.separar_linea(linea, ",")
                        if len(partes) == 4:
                            cod_equipo = partes[0]
                            cod_pais = partes[1]
                            ent_data = partes[2]
                            pais_encontrado = None
                            for p in paises:
                                if p.codigo_fifa == cod_pais:
                                    pais_encontrado = p
                                    break
                            if pais_encontrado:
                                s = Seleccion(cod_equipo, pais_encontrado)
                                if ent_data != "None":
                                    ep = self.separar_linea(ent_data, "|")
                                    if len(ep) == 7:
                                        ent = Entrenador(ep[0], ep[1], ep[2], ep[3], ep[4], int(ep[5]), ep[6])
                                        s.asignar_entrenador(ent)
                                selecciones = selecciones + [s]
            except Exception as e:
                print(f"Error cargando selecciones: {e}")
        return selecciones

    """
    descripción: Guarda el listado total de jugadores en el disco.
    #E: selecciones
    #S: guarda la lista de jugadores en un txt
    #R: selecciones debe ser una lista
    Objetivo: Evitar la pérdida de datos de los futbolistas y sus estadísticas.
    """
    def guardar_jugadores(self, selecciones):
        if not isinstance(selecciones, list):
            return "Error: selecciones debe ser una lista"
            
        try:
            with open(self.conseguir_ruta("jugadores.txt"), "w", encoding="utf-8") as f:
                for s in selecciones:
                    for j in s.jugadores:
                        f.write(f"{s.codigo_equipo},{j.nombre},{j.apellido},{j.fecha_nacimiento},{j.nacionalidad},{j.dorsal},{j.posicion},{j.puntaje_individual},{j.goles},{j.asistencias},{j.total_tarjetas_amarillas},{j.total_tarjetas_rojas}\n")
        except Exception as e:
            print(f"Error al guardar a los jugadores: {e}")
    """
    descripción: Carga la información de los jugadores al programa.
    #E: selecciones
    #S: lee el txt y carga los jugadores a las selecciones correspondientes
    #R: selecciones debe ser una lista
    Objetivo: Restaurar las plantillas de los equipos al reiniciar la aplicación.
    """
    def cargar_jugadores(self, selecciones):
        if not isinstance(selecciones, list):
            return "Error: selecciones debe ser una lista"
        ruta = self.conseguir_ruta("jugadores.txt")
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    for linea in f:
                        partes = self.separar_linea(linea, ",")
                        if len(partes) == 12:
                            cod_equipo = partes[0]
                            seleccion_encontrada = None
                            for sel in selecciones:
                                if sel.codigo_equipo == cod_equipo:
                                    seleccion_encontrada = sel
                                    break
                            if seleccion_encontrada:
                                j = Futbolista(partes[1], partes[2], partes[3], partes[4], int(partes[5]), partes[6], int(partes[7]))
                                j.goles = int(partes[8])
                                j.asistencias = int(partes[9])
                                j.total_tarjetas_amarillas = int(partes[10])
                                j.total_tarjetas_rojas = int(partes[11])
                                seleccion_encontrada.agregar_jugador(j)
            except Exception as e:
                print(f"Error cargando jugadores: {e}")
    """
    descripción: Exporta las estadísticas y rankings a un archivo de texto.
    #E: selecciones
    #S: guarda los rankings en archivos txt
    #R: selecciones debe ser una lista
    Objetivo: Generar un reporte persistente con los resultados del torneo.
    """
    def guardar_rankings(self, selecciones):
        if not isinstance(selecciones, list):
            return "Error: selecciones debe ser una lista"  
        try:
            todos_jugadores = []
            for s in selecciones:
                for j in s.jugadores:
                    if j.goles > 0:
                        todos_jugadores = todos_jugadores + [(j, s)]
            largo_jugadores = len(todos_jugadores)
            for i in range(largo_jugadores):
                for j in range(0, largo_jugadores - i - 1):
                    goles_actual = todos_jugadores[j][0].goles
                    goles_siguiente = todos_jugadores[j + 1][0].goles
                    if goles_actual < goles_siguiente:
                        temp = todos_jugadores[j]
                        todos_jugadores[j] = todos_jugadores[j + 1]
                        todos_jugadores[j + 1] = temp
            with open(self.conseguir_ruta("ranking_goleadores.txt"), "w", encoding="utf-8") as f:
                f.write(f"{'Nombre':<25} | {'Seleccion':<15} | {'Goles':<5}\n")
                for tupla in todos_jugadores:
                    jugador = tupla[0]
                    selec = tupla[1]
                    f.write(f"{jugador.nombre + ' ' + jugador.apellido:<25} | {selec.pais.nombre:<15} | {jugador.goles:<5}\n")     
            sels = selecciones.copy()
            largo_sels = len(sels)
            for i in range(largo_sels):
                for j in range(0, largo_sels - i - 1):
                    s1 = sels[j]
                    s2 = sels[j + 1]
                    dif1 = s1.total_goles_favor - s1.total_goles_contra
                    dif2 = s2.total_goles_favor - s2.total_goles_contra
                    cambiar = False
                    if s1.puntos < s2.puntos:
                        cambiar = True
                    elif s1.puntos == s2.puntos:
                        if dif1 < dif2:
                            cambiar = True    
                    if cambiar:
                        temp = sels[j]
                        sels[j] = sels[j + 1]
                        sels[j + 1] = temp
            with open(self.conseguir_ruta("ranking_selecciones.txt"), "w", encoding="utf-8") as f:
                f.write(f"{'Pais':<16} | {'Pts':<3} | {'PJ':<2} | {'PG':<2} | {'PE':<2} | {'PP':<2} | {'GF':<2} | {'GC':<2} | {'DG':<3} | {'TA':<2} | {'TR':<2}\n")
                for s in sels:
                    dg = s.total_goles_favor - s.total_goles_contra
                    f.write(f"{s.pais.nombre:<16} | {s.puntos:<3} | {s.partidos_jugados:<2} | {s.partidos_ganados:<2} | {s.partidos_empatados:<2} | {s.partidos_perdidos:<2} | {s.total_goles_favor:<2} | {s.total_goles_contra:<2} | {dg:<3} | {s.total_tarjetas_amarillas:<2} | {s.total_tarjetas_rojas:<2}\n")
                    
            max_goles = -1
            sel_max_goles = None
            max_tarjetas = -1
            sel_max_tarjetas = None
            for s in sels:
                if s.total_goles_favor > max_goles:
                    max_goles = s.total_goles_favor
                    sel_max_goles = s
                tarjetas = s.total_tarjetas_amarillas + s.total_tarjetas_rojas
                if tarjetas > max_tarjetas:
                    max_tarjetas = tarjetas
                    sel_max_tarjetas = s
            with open(self.conseguir_ruta("records.txt"), "w", encoding="utf-8") as f:
                f.write(f"{'Categoria':<25} | {'Seleccion':<16} | {'Cantidad':<8}\n")
                if sel_max_goles:
                    f.write(f"{'Mas Goles Anotados':<25} | {sel_max_goles.pais.nombre:<16} | {max_goles:<8}\n")
                if sel_max_tarjetas:
                    f.write(f"{'Mas Tarjetas':<25} | {sel_max_tarjetas.pais.nombre:<16} | {max_tarjetas:<8}\n")
        except Exception as e:
            print(f"Error guardando rankings: {e}")
    """
    descripción: Escribe el historial de partidos simulados en el disco.
    #E: partidos
    #S: guarda la lista de partidos en un txt
    #R: partidos debe ser una lista
    Objetivo: Conservar la bitácora completa de los enfrentamientos para futuras referencias.
    """
    def guardar_partidos(self, partidos):
        if not isinstance(partidos, list):
            return "Error: partidos debe ser una lista"
        try:
            with open(self.conseguir_ruta("partidos.txt"), "w", encoding="utf-8") as f:
                f.write(f"{'Fase':<12} | {'Equipo 1':<15} | {'Goles 1':<7} | {'Equipo 2':<15} | {'Goles 2':<7} | {'Penales 1':<9} | {'Penales 2':<9}\n")
                for p in partidos:
                    f.write(f"{p.fase:<12} | {p.equipo_1.pais.nombre:<15} | {p.goles_equipo1:<7} | {p.equipo_2.pais.nombre:<15} | {p.goles_equipo2:<7} | {p.penales_equipo1:<9} | {p.penales_equipo2:<9}\n")
        except Exception as e:
            print(f"Error guardando partidos: {e}")

