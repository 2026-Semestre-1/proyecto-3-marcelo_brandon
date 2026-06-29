class Pais:
    """
    descripción: Inicializa los atributos principales de la clase.
    #E: codigo_fifa, nombre, continente, ranking_fifa
    #S: inicializa la clase Pais con sus atributos
    #R: el atributo ranking_fifa debe ser mayor a 0 codigo_fifa debe ser un string nombre debe ser string continente debe ser string ranking_fifa debe ser un entero
    Objetivo: Establecer el estado inicial del objeto para su correcto funcionamiento en el sistema.
    """
    def __init__(self, codigo_fifa, nombre, continente, ranking_fifa):
        if not isinstance(codigo_fifa, str):
            return "Error: codigo_fifa debe ser un string"
        if not isinstance(nombre, str):
            return "Error: nombre debe ser un string"
        if not isinstance(continente, str):
            return "Error: continente debe ser un string"
        if not isinstance(ranking_fifa, int):
            return "Error: ranking_fifa debe ser un entero."
        if ranking_fifa <= 0:
            return "Error: ranking_fifa debe ser mayor a 0"

        self.codigo_fifa = codigo_fifa
        self.nombre = nombre
        self.continente = continente
        self.ranking_fifa = ranking_fifa

    """
    descripción: Muestra por consola la información del objeto.
    #E: Ninguna
    #S: retorna la información del país
    #R: debe mostrar un string
    Objetivo: Permitir la visualización rápida del estado y valores actuales de la instancia.
    """
    def mostrar_datos(self):
        print(f"[{self.codigo_fifa}] {self.nombre} - {self.continente} (Ranking: {self.ranking_fifa})")

    """
    descripción: Actualiza los atributos específicos de la instancia.
    #E: nombre, continente, ranking_fifa
    #S: Modifica los atributos del país.
    #R: el atributo ranking_fifa debe ser un entero mayor a 0 nombre debe ser un string continente debe ser un string
    Objetivo: Permitir la modificación dinámica de los datos del objeto en tiempo de ejecución.
    """
    def actualizar_datos(self, nombre, continente, ranking_fifa):
        if not isinstance(nombre, str):
            return "Error: nombre debe ser un string" 
        if not isinstance(continente, str):
            return "Error: continente debe ser un string"
        if not isinstance(ranking_fifa, int) or ranking_fifa <= 0:
            return "Error: ranking_fifa debe ser un entero mayor a 0"
            
            
        self.nombre = nombre
        self.continente = continente
        self.ranking_fifa = ranking_fifa

