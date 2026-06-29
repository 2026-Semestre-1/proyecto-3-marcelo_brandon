import tkinter as tk
from tkinter import messagebox
import os

# Imports de las clases
from pais import Pais
from seleccion import Seleccion
from futbolista import Futbolista
from entrenador import Entrenador
from archivos import Archivos
from mundial import Mundial

RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_FONDO = os.path.join(RUTA_BASE, "fondo_inicio.png")

# =========================================================================
# VENTANA PRINCIPAL
# =========================================================================
"""
nombre: VentanaPrincipal
#E: Ninguna
#S: Crea la ventana principal de la aplicación
#R: Debe heredar de tk.Tk para funcionar como ventana
Objetivo: VentanaPrincipal
"""
class VentanaPrincipal(tk.Tk):
    
    """
    descripción: Inicializa los atributos principales de la clase.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def __init__(self):
        super().__init__()
        
        self.title("FIFA WORLD CUP 2026")
        self.state('zoomed')  
        
        # --- PALETA DE COLORES ---
        self.color_fondo = "#C5CCDB"     
        self.color_menu = "#111827"         
        self.color_menu_borde = "#374151"     
        self.color_boton_activo = "#111E6C"   
        self.color_boton_hover = "#111E6C"    
        self.color_boton_normal = "#1E293B"    
        self.color_dorado = "#FACC15"          
        self.color_texto_claro = "#FFFFFF"     
        self.color_texto_oscuro = "#0F172A"    
        self.color_texto_gris = "#64748B"      
        self.color_verde = "#16A34A"       
        
        self.configure(bg=self.color_fondo)
        
        self.hay_cambios = False 
        self.pantalla_actual = None
        
        # Instancia de Archivos y listas de objetos
        self.archivos = Archivos(RUTA_BASE)
        self.paises = self.archivos.cargar_paises()
        self.selecciones = self.archivos.cargar_selecciones(self.paises)
        self.archivos.cargar_jugadores(self.selecciones)
        self.jugadores = [] 
        self.entrenadores = []

        for sel in self.selecciones:
            if sel.entrenador is not None:
                self.entrenadores = self.entrenadores + [sel.entrenador]
            
            for jug in sel.jugadores:
                self.jugadores = self.jugadores + [jug]
                
        # Inicializar el Mundial global
        self.mi_mundial = Mundial("Mundial 2026", 2026)
        # Asignarle las selecciones cargadas
        self.mi_mundial.selecciones = self.selecciones
               
        self.mostrar_bienvenida()

    # =========================================================================
    # PANTALLA BIENVENIDA
    # =========================================================================
    """
    descripción: Despliega la pantalla inicial del sistema.
    #E: Ninguna
    #S: Muestra la pantalla inicial con el fondo y los botones de comenzar y salir
    #R: Las imágenes deben existir en la carpeta de imagenes
    Objetivo: Dar la bienvenida al usuario y presentar el menú principal.
    """
    def mostrar_bienvenida(self):
        if self.pantalla_actual:
            self.pantalla_actual.destroy()
            
        self.pantalla_actual = tk.Frame(self, bg=self.color_menu)
        self.pantalla_actual.pack(fill=tk.BOTH, expand=True)
        
        self.fondo_inicio = tk.PhotoImage(file=RUTA_FONDO)
        label_fondo = tk.Label(self.pantalla_actual, image=self.fondo_inicio)
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        
        tk.Button(self.pantalla_actual, text="COMENZAR", 
                  font=("Segoe UI", 16, "bold"), bg=self.color_boton_activo, 
                  fg=self.color_texto_claro, relief=tk.FLAT, cursor="hand2", 
                  padx=70, pady=16, command=self.mostrar_menu).place(relx=0.40, rely=0.73, anchor="center")
        
        tk.Button(self.pantalla_actual, text="SALIR", 
                  font=("Segoe UI", 16, "bold"), bg=self.color_dorado, 
                  fg=self.color_texto_oscuro, relief=tk.FLAT, cursor="hand2", 
                  padx=70, pady=16, command=self.confirmar_salir).place(relx=0.60, rely=0.73, anchor="center")

    # =========================================================================
    # MENÚ PRINCIPAL
    # =========================================================================
    """
    descripción: Construye el panel de navegación lateral.
    #E: Ninguna
    #S: Muestra el menú lateral y el área de contenido principal
    #R: Ninguna
    Objetivo: Permitir al usuario acceder a las diferentes secciones del sistema.
    """
    def mostrar_menu(self):
        if self.pantalla_actual:
            self.pantalla_actual.destroy()
            
        contenedor = tk.Frame(self, bg=self.color_fondo)
        contenedor.pack(fill=tk.BOTH, expand=True)
        self.pantalla_actual = contenedor
        
        menu = tk.Frame(contenedor, bg=self.color_menu, width=260)
        self.menu_lateral = menu
        menu.pack(side=tk.LEFT, fill=tk.Y)
        menu.pack_propagate(False)
        
        ruta_logo = os.path.join(RUTA_BASE, "logomenu.png")
        self.logo_menu = tk.PhotoImage(file=ruta_logo)
        self.logo_menu = self.logo_menu.subsample(7, 7)
        tk.Label(menu, image=self.logo_menu, bg=self.color_menu).pack(pady=(25, 0))
        
        tk.Frame(menu, bg=self.color_dorado, height=2).pack(fill=tk.X, padx=20, pady=(10, 0))
        
        self.crear_boton_menu(menu, "Países", self.cargar_paises)
        self.crear_boton_menu(menu, "Selecciones", self.cargar_selecciones)

        tk.Frame(menu, bg=self.color_dorado, height=2).pack(fill=tk.X, padx=20, pady=(0, 0))
        
        self.crear_boton_menu(menu, "Entrenadores", self.cargar_entrenadores)
        self.crear_boton_menu(menu, "Jugadores", self.cargar_jugadores)

        tk.Frame(menu, bg=self.color_dorado, height=2).pack(fill=tk.X, padx=20, pady=(0, 0))
        
        self.crear_boton_menu(menu, "Configurar Mundial", self.cargar_configurar)
        self.crear_boton_menu(menu, "Simular Mundial", self.cargar_simular)

        tk.Frame(menu, bg=self.color_dorado, height=2).pack(fill=tk.X, padx=20, pady=(0, 0))
        
        self.crear_boton_menu(menu, "Estadísticas", self.cargar_estadisticas)
        
        tk.Frame(menu, bg=self.color_menu, height=20).pack(fill=tk.X)
        
        tk.Button(menu, text="Volver al Inicio", font=("Segoe UI", 14, "bold"), 
                  bg=self.color_boton_normal, fg=self.color_texto_claro, 
                  relief=tk.FLAT, cursor="hand2", pady=10,
                  command=self.volver_inicio).pack(fill=tk.X, pady=0, padx=0)

        self.area_contenido = tk.Frame(contenedor, bg=self.color_fondo)
        self.area_contenido.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.cargar_paises()

    """
    descripción: Genera un botón estándar para la barra lateral.
    #E: self, padre, texto, comando
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def crear_boton_menu(self, padre, texto, comando):
        boton = tk.Button(padre, text=texto, font=("Segoe UI", 13), 
                          bg=self.color_menu, fg=self.color_texto_claro, 
                          activebackground=self.color_boton_activo, 
                          activeforeground=self.color_texto_claro, 
                          relief=tk.FLAT, anchor="w", padx=30, pady=15, 
                          cursor="hand2", command=comando)
        boton.pack(fill=tk.X, pady=2, padx=10)
        boton.bind("<Enter>", lambda e: boton.configure(bg=self.color_boton_hover, font=("Segoe UI", 13, "bold")))
        boton.bind("<Leave>", lambda e: boton.configure(bg=self.color_menu, font=("Segoe UI", 13)))

    """
    descripción: Borra los elementos (widgets) de un contenedor.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def limpiar_contenido(self):
        for widget in self.area_contenido.winfo_children():
            widget.destroy()

    """
    descripción: Dibuja el título principal de una vista.
    #E: self, titulo, descripcion
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def crear_encabezado(self, titulo, descripcion):
        tk.Label(self.area_contenido, text=titulo, font=("Segoe UI", 30, "bold"),
                 bg=self.color_fondo, fg=self.color_texto_oscuro).pack(pady=(40, 0))
        tk.Label(self.area_contenido, text=descripcion, font=("Segoe UI", 13),
                 bg=self.color_fondo, fg=self.color_texto_gris).pack(pady=(0, 20))

    """
    descripción: Marca que han habido ediciones no guardadas.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def marcar_cambios(self):
        self.hay_cambios = True

    # =========================================================================
    # PANTALLA: PAÍSES
    # =========================================================================
    """
    descripción: Lee los datos de países desde el disco al sistema.
    #E: Ninguna
    #S: Muestra la pantalla de gestión de países
    #R: Pregunta si hay cambios sin guardar
    Objetivo: Poblar el sistema con los datos de países previamente guardados.
    """
    def cargar_paises(self):
        if self.hay_cambios:
            if not messagebox.askyesno("Atención", "Hay cambios sin guardar. ¿Desea salir?"):
                return
        self.hay_cambios = False
        self.limpiar_contenido()
        self.crear_encabezado("Gestión de Países", "Registrar y administrar los países participantes.")
        
        contenedor = tk.Frame(self.area_contenido, bg=self.color_fondo)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        frame_tabs = tk.Frame(contenedor, bg=self.color_fondo)
        frame_tabs.pack(pady=(0, 5))
        
        self.btn_tab_registro_pais = tk.Button(frame_tabs, text="Registrar País", font=("Segoe UI", 12, "bold"),
                                               bg=self.color_boton_activo, fg=self.color_texto_claro,
                                               relief=tk.FLAT, padx=25, pady=8, cursor="hand2",
                                               command=self.mostrar_registro_pais)
        self.btn_tab_registro_pais.grid(row=0, column=0, padx=5)
        
        self.btn_tab_lista_pais = tk.Button(frame_tabs, text="Lista de Países", font=("Segoe UI", 12),
                                            bg="#E2E8F0", fg=self.color_texto_oscuro,
                                            relief=tk.FLAT, padx=25, pady=8, cursor="hand2",
                                            command=self.mostrar_lista_paises)
        self.btn_tab_lista_pais.grid(row=0, column=1, padx=5)

        self.btn_tab_lista_pais.bind("<Enter>", lambda e: self.btn_tab_lista_pais.config(bg="#CBD5E1"))
        self.btn_tab_lista_pais.bind("<Leave>", lambda e: self.btn_tab_lista_pais.config(bg="#E2E8F0"))
        
        tk.Frame(contenedor, bg="#D1D5DB", height=2).pack(fill=tk.X, pady=(0, 15))
        
        self.frame_contenido_paises = tk.Frame(contenedor, bg=self.color_fondo)
        self.frame_contenido_paises.pack(fill=tk.BOTH, expand=True)
        
        self.mostrar_registro_pais()

    """
    descripción: Despliega el formulario para añadir países.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def mostrar_registro_pais(self):
        for w in self.frame_contenido_paises.winfo_children():
            w.destroy()
            
        self.btn_tab_registro_pais.configure(bg=self.color_boton_activo, fg=self.color_texto_claro, font=("Segoe UI", 12, "bold"))
        self.btn_tab_lista_pais.configure(bg="#E2E8F0", fg=self.color_texto_oscuro, font=("Segoe UI", 12))

        frame_form = tk.Frame(self.frame_contenido_paises, bg=self.color_texto_claro, relief=tk.SOLID, bd=1)
        frame_form.pack(fill=tk.X, padx=100, pady=50)

        tk.Label(frame_form, text="Registrar nuevo país", font=("Segoe UI", 16, "bold"), 
                 bg=self.color_texto_claro, fg=self.color_texto_oscuro).grid(row=0, column=0, columnspan=4, sticky="w", padx=30, pady=(20, 15))
        
        tk.Label(frame_form, text="Código FIFA:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=1, column=0, padx=(30, 10), pady=8, sticky="w")
        self.entry_codigo_pais = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_codigo_pais.grid(row=1, column=1, padx=10, pady=8, sticky="ew")
        self.entry_codigo_pais.bind("<KeyRelease>", lambda e: self.marcar_cambios())
        
        tk.Label(frame_form, text="Nombre:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=1, column=2, padx=(20, 10), pady=8, sticky="w")
        self.entry_nombre_pais = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_nombre_pais.grid(row=1, column=3, padx=(10, 30), pady=8, sticky="ew")
        self.entry_nombre_pais.bind("<KeyRelease>", lambda e: self.marcar_cambios())
        
        tk.Label(frame_form, text="Continente:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=2, column=0, padx=(30, 10), pady=8, sticky="w")
        self.combo_continente = tk.StringVar(value="América")
        menu_continente = tk.OptionMenu(frame_form, self.combo_continente, "América", "Europa", "Asia", "África", "Oceanía")
        menu_continente.config(font=("Segoe UI", 11), width=18, relief=tk.SOLID, borderwidth=1, bg=self.color_texto_claro)
        menu_continente.grid(row=2, column=1, padx=10, pady=8, sticky="ew")
        self.combo_continente.trace_add("write", lambda *args: self.marcar_cambios())
        
        tk.Label(frame_form, text="Ranking FIFA:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=2, column=2, padx=(20, 10), pady=8, sticky="w")
        self.entry_ranking_pais = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_ranking_pais.grid(row=2, column=3, padx=(10, 30), pady=8, sticky="ew")
        self.entry_ranking_pais.bind("<KeyRelease>", lambda e: self.marcar_cambios())

        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)
        
        frame_boton = tk.Frame(frame_form, bg=self.color_texto_claro)
        frame_boton.grid(row=3, column=0, columnspan=4, pady=(25, 30))
        
        tk.Button(frame_boton, text="Guardar país", font=("Segoe UI", 12, "bold"), 
                  bg=self.color_boton_activo, fg=self.color_texto_claro, relief=tk.FLAT, cursor="hand2",
                  padx=40, pady=8, command=self.registrar_pais).pack()

    """
    descripción: Añade barras de desplazamiento a un contenedor.
    #E: contenedor_padre
    #S: retorna un frame interno con scroll
    #R: contenedor debe ser un frame de tkinter
    Objetivo: Permitir la navegación visual cuando hay demasiados elementos en una lista.
    """
    def crear_frame_scrollable(self, contenedor_padre):
        frame_exterior = tk.Frame(contenedor_padre, bg=self.color_texto_claro, relief=tk.SOLID, bd=1)
        frame_exterior.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        canvas = tk.Canvas(frame_exterior, bg=self.color_texto_claro, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(frame_exterior, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        frame_interior = tk.Frame(canvas, bg=self.color_texto_claro)
        window_id = canvas.create_window((0, 0), window=frame_interior, anchor="nw")
        """
        descripción: Captura el giro de la rueda del ratón.
        #E: event
        #S: actualiza el scroll
        #R: ninguna
        Objetivo: mover canvas
        """
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        frame_interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))
        return frame_interior

    """
    descripción: Renderiza la tabla con los países registrados.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def mostrar_lista_paises(self):
        for w in self.frame_contenido_paises.winfo_children():
            w.destroy()
            
        self.btn_tab_lista_pais.configure(bg=self.color_boton_activo, fg=self.color_texto_claro, font=("Segoe UI", 12, "bold"))
        self.btn_tab_registro_pais.configure(bg="#E2E8F0", fg=self.color_texto_oscuro, font=("Segoe UI", 12))
        
        self.btn_tab_registro_pais.bind("<Enter>", lambda e: self.btn_tab_registro_pais.config(bg="#CBD5E1"))
        self.btn_tab_registro_pais.bind("<Leave>", lambda e: self.btn_tab_registro_pais.config(bg="#E2E8F0"))
        
        frame_superior = tk.Frame(self.frame_contenido_paises, bg=self.color_fondo)
        frame_superior.pack(fill=tk.X, pady=(0, 15))

        cantidad = len(self.paises)
        tk.Label(frame_superior, text="Países registrados (%d)" % cantidad, font=("Segoe UI", 20, "bold"), 
                 bg=self.color_fondo, fg=self.color_texto_oscuro).pack(anchor="w", padx=20)

        frame_tabla = self.crear_frame_scrollable(self.frame_contenido_paises)
        
        encabezados = ["Código", "Nombre", "Continente", "Ranking", "Editar", "Eliminar"]
        columna = 0
        for texto in encabezados:
            tk.Label(frame_tabla, text=texto, font=("Segoe UI", 11, "bold"), 
                     bg="#F1F5F9", fg=self.color_texto_oscuro, anchor="w",
                     padx=15, pady=12, relief=tk.SOLID, bd=1).grid(row=0, column=columna, sticky="ew")
            columna += 1
            
        for i in range(4):
            frame_tabla.columnconfigure(i, weight=1)
            
        if cantidad == 0:
            tk.Label(frame_tabla, text="No hay países registrados.", 
                     font=("Segoe UI", 12), bg=self.color_texto_claro, fg=self.color_texto_gris, justify="center").grid(row=1, column=0, columnspan=6, pady=60)
        else:
            fila = 1
            for pais in self.paises:
                tk.Label(frame_tabla, text=pais.codigo_fifa, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=0, sticky="ew")
                tk.Label(frame_tabla, text=pais.nombre, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=1, sticky="ew")
                tk.Label(frame_tabla, text=pais.continente, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=2, sticky="ew")
                tk.Label(frame_tabla, text=str(pais.ranking_fifa), font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=3, sticky="ew")
                
                btn_editar = tk.Button(frame_tabla, text="Editar", font=("Segoe UI", 10), bg="#FBBF24", relief=tk.FLAT, cursor="hand2",
                                       command=lambda p=pais: self.editar_pais(p))
                btn_editar.grid(row=fila, column=4, padx=5, pady=5)
                
                btn_eliminar = tk.Button(frame_tabla, text="Eliminar", font=("Segoe UI", 10), bg="#DC2626", fg="white", relief=tk.FLAT, cursor="hand2",
                                         command=lambda p=pais: self.eliminar_pais(p))
                btn_eliminar.grid(row=fila, column=5, padx=5, pady=5)
                
                fila += 1

    """
    descripción: Valida y guarda un nuevo país ingresado.
    #E: Datos de los Entry
    #S: Guarda el país en la lista y en el archivo
    #R: Valida usando el constructor de la clase Pais
    Objetivo: Procesar la entrada del formulario y almacenar la nación en memoria.
    """
    def registrar_pais(self):
        codigo = self.entry_codigo_pais.get().strip().upper()
        nombre = self.entry_nombre_pais.get().strip()
        continente = self.combo_continente.get()
        ranking_str = self.entry_ranking_pais.get().strip()
        
        if not self.EsEntero(ranking_str):
            messagebox.showwarning("Atención", "El ranking debe ser un número válido.")
            return
        
        ranking = int(ranking_str)
        
        nuevo_pais = Pais(codigo, nombre, continente, ranking)
        if isinstance(nuevo_pais, str):
            messagebox.showerror("Error", nuevo_pais)
            return
        
        for p in self.paises:
            if p.codigo_fifa == codigo:
                messagebox.showwarning("Atención", "Ya existe un país con el código " + codigo + ".")
                return
            if p.ranking_fifa == ranking:
                messagebox.showwarning("Atención", "El ranking " + str(ranking) + " ya está ocupado por " + p.nombre + ".")
                return
        
        self.paises = self.paises + [nuevo_pais]
        self.archivos.guardar_paises(self.paises)
        
        messagebox.showinfo("Éxito", "El país " + nombre + " ha sido registrado correctamente.")
        self.hay_cambios = False
        self.mostrar_lista_paises()

    """
    descripción: Permite modificar los datos de un país.
    #E: self, pais
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def editar_pais(self, pais):
        self.mostrar_registro_pais()
        self.entry_codigo_pais.delete(0, tk.END)
        self.entry_codigo_pais.insert(0, pais.codigo_fifa)
        self.entry_nombre_pais.delete(0, tk.END)
        self.entry_nombre_pais.insert(0, pais.nombre)
        self.combo_continente.set(pais.continente)
        self.entry_ranking_pais.delete(0, tk.END)
        self.entry_ranking_pais.insert(0, str(pais.ranking_fifa))
        self.eliminar_pais_silencioso(pais)
        
    """
    descripción: Borra un país de memoria sin pedir confirmación.
    #E: self, pais
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def eliminar_pais_silencioso(self, pais):
        nuevos_paises = []
        for p in self.paises:
            if p.codigo_fifa != pais.codigo_fifa:
                nuevos_paises = nuevos_paises + [p]
        self.paises = nuevos_paises

    """
    descripción: Solicita confirmación y borra un país seleccionado.
    #E: self, pais
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def eliminar_pais(self, pais):
        if messagebox.askyesno("Confirmar", "¿Desea eliminar el país " + pais.nombre + "?"):
            nuevos_paises = []
            for p in self.paises:
                if p.codigo_fifa != pais.codigo_fifa:
                    nuevos_paises = nuevos_paises + [p]
            self.paises = nuevos_paises
            self.archivos.guardar_paises(self.paises)
            self.mostrar_lista_paises()

    # =========================================================================
    # PANTALLA: SELECCIONES (NUEVA E INTEGRADA)
    # =========================================================================
    """
    descripción: Lee los datos de selecciones desde el almacenamiento.
    #E: Ninguna
    #S: Muestra la pantalla de gestión de selecciones
    #R: Pregunta si hay cambios sin guardar
    Objetivo: Cargar las selecciones existentes para ser usadas en el torneo.
    """
    def cargar_selecciones(self):
        if self.hay_cambios:
            if not messagebox.askyesno("Atención", "Hay cambios sin guardar. ¿Desea salir?"):
                return
        self.hay_cambios = False
        self.limpiar_contenido()
        self.crear_encabezado("Gestión de Selecciones", "Crear selecciones nacionales asociadas a un país.")
        
        contenedor = tk.Frame(self.area_contenido, bg=self.color_fondo)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        frame_tabs = tk.Frame(contenedor, bg=self.color_fondo)
        frame_tabs.pack(pady=(0, 5))
        
        self.btn_tab_registro_sel = tk.Button(frame_tabs, text="Registrar Selección", font=("Segoe UI", 12, "bold"),
                                              bg=self.color_boton_activo, fg=self.color_texto_claro,
                                              relief=tk.FLAT, padx=25, pady=8, cursor="hand2",
                                              command=self.mostrar_registro_seleccion)
        self.btn_tab_registro_sel.grid(row=0, column=0, padx=5)
        
        self.btn_tab_lista_sel = tk.Button(frame_tabs, text="Lista de Selecciones", font=("Segoe UI", 12),
                                           bg="#E2E8F0", fg=self.color_texto_oscuro,
                                           relief=tk.FLAT, padx=25, pady=8, cursor="hand2",
                                           command=self.mostrar_lista_selecciones)
        self.btn_tab_lista_sel.grid(row=0, column=1, padx=5)

        self.btn_tab_lista_sel.bind("<Enter>", lambda e: self.btn_tab_lista_sel.config(bg="#CBD5E1"))
        self.btn_tab_lista_sel.bind("<Leave>", lambda e: self.btn_tab_lista_sel.config(bg="#E2E8F0"))
        
        tk.Frame(contenedor, bg="#D1D5DB", height=2).pack(fill=tk.X, pady=(0, 15))
        
        self.frame_contenido_selecciones = tk.Frame(contenedor, bg=self.color_fondo)
        self.frame_contenido_selecciones.pack(fill=tk.BOTH, expand=True)
        
        self.mostrar_registro_seleccion()

    """
    descripción: Despliega el formulario de selecciones.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def mostrar_registro_seleccion(self):
        for w in self.frame_contenido_selecciones.winfo_children():
            w.destroy()
            
        self.btn_tab_registro_sel.configure(bg=self.color_boton_activo, fg=self.color_texto_claro, font=("Segoe UI", 12, "bold"))
        self.btn_tab_lista_sel.configure(bg="#E2E8F0", fg=self.color_texto_oscuro, font=("Segoe UI", 12))

        frame_form = tk.Frame(self.frame_contenido_selecciones, bg=self.color_texto_claro, relief=tk.SOLID, bd=1)
        frame_form.pack(fill=tk.X, padx=100, pady=50)

        tk.Label(frame_form, text="Registrar nueva selección", font=("Segoe UI", 16, "bold"), 
                 bg=self.color_texto_claro, fg=self.color_texto_oscuro).grid(row=0, column=0, columnspan=4, sticky="w", padx=30, pady=(20, 15))
        
        tk.Label(frame_form, text="Código Selección:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=1, column=0, padx=(30, 10), pady=8, sticky="w")
        self.entry_codigo_seleccion = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_codigo_seleccion.grid(row=1, column=1, padx=10, pady=8, sticky="ew")
        self.entry_codigo_seleccion.bind("<KeyRelease>", lambda e: self.marcar_cambios())
        
        tk.Label(frame_form, text="País asociado:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=1, column=2, padx=(20, 10), pady=8, sticky="w")
        
        # Cargar países para el OptionMenu
        opciones_paises = []
        for p in self.paises:
            opciones_paises = opciones_paises + [p.codigo_fifa]
            
        if len(opciones_paises) == 0:
            opciones_paises = ["No hay países registrados"]
            
        self.combo_pais_seleccion = tk.StringVar(value=opciones_paises[0])
        menu_pais = tk.OptionMenu(frame_form, self.combo_pais_seleccion, *opciones_paises)
        menu_pais.config(font=("Segoe UI", 11), width=18, relief=tk.SOLID, borderwidth=1, bg=self.color_texto_claro)
        menu_pais.grid(row=1, column=3, padx=(10, 30), pady=8, sticky="ew")
        self.combo_pais_seleccion.trace_add("write", lambda *args: self.marcar_cambios())

        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)
        
        frame_boton = tk.Frame(frame_form, bg=self.color_texto_claro)
        frame_boton.grid(row=2, column=0, columnspan=4, pady=(25, 30))
        
        tk.Button(frame_boton, text="Guardar selección", font=("Segoe UI", 12, "bold"), 
                  bg=self.color_boton_activo, fg=self.color_texto_claro, relief=tk.FLAT, cursor="hand2",
                  padx=40, pady=8, command=self.registrar_seleccion).pack()

    """
    descripción: Renderiza la tabla de selecciones registradas.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def mostrar_lista_selecciones(self):
        for w in self.frame_contenido_selecciones.winfo_children():
            w.destroy()
            
        self.btn_tab_lista_sel.configure(bg=self.color_boton_activo, fg=self.color_texto_claro, font=("Segoe UI", 12, "bold"))
        self.btn_tab_registro_sel.configure(bg="#E2E8F0", fg=self.color_texto_oscuro, font=("Segoe UI", 12))
        
        self.btn_tab_registro_sel.bind("<Enter>", lambda e: self.btn_tab_registro_sel.config(bg="#CBD5E1"))
        self.btn_tab_registro_sel.bind("<Leave>", lambda e: self.btn_tab_registro_sel.config(bg="#E2E8F0"))
        
        frame_superior = tk.Frame(self.frame_contenido_selecciones, bg=self.color_fondo)
        frame_superior.pack(fill=tk.X, pady=(0, 15))

        cantidad = len(self.selecciones)
        tk.Label(frame_superior, text="Selecciones registradas (%d)" % cantidad, font=("Segoe UI", 20, "bold"), 
                 bg=self.color_fondo, fg=self.color_texto_oscuro).pack(anchor="w", padx=20)

        frame_tabla = self.crear_frame_scrollable(self.frame_contenido_selecciones)
        
        encabezados = ["Código", "País", "Entrenador", "Jugadores", "Editar", "Eliminar"]
        columna = 0
        for texto in encabezados:
            tk.Label(frame_tabla, text=texto, font=("Segoe UI", 11, "bold"), 
                     bg="#F1F5F9", fg=self.color_texto_oscuro, anchor="w",
                     padx=15, pady=12, relief=tk.SOLID, bd=1).grid(row=0, column=columna, sticky="ew")
            columna += 1
            
        for i in range(4):
            frame_tabla.columnconfigure(i, weight=1)
            
        if cantidad == 0:
            tk.Label(frame_tabla, text="No hay selecciones registradas.", 
                     font=("Segoe UI", 12), bg=self.color_texto_claro, fg=self.color_texto_gris, justify="center").grid(row=1, column=0, columnspan=6, pady=60)
        else:
            fila = 1
            for sel in self.selecciones:
                tk.Label(frame_tabla, text=sel.codigo_equipo, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=0, sticky="ew")
                tk.Label(frame_tabla, text=sel.pais.nombre, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=1, sticky="ew")
                
                ent_texto = "Sin asignar"
                if sel.entrenador:
                    ent_texto = sel.entrenador.nombre + " " + sel.entrenador.apellido
                tk.Label(frame_tabla, text=ent_texto, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=2, sticky="ew")
                
                # AQUI ESTA EL CAMBIO: de 23 a 20
                tk.Label(frame_tabla, text="%d / 20" % len(sel.jugadores), font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=3, sticky="ew")
                
                btn_editar = tk.Button(frame_tabla, text="Editar", font=("Segoe UI", 10), bg="#FBBF24", relief=tk.FLAT, cursor="hand2",
                                       command=lambda s=sel: self.editar_seleccion(s))
                btn_editar.grid(row=fila, column=4, padx=5, pady=5)
                
                btn_eliminar = tk.Button(frame_tabla, text="Eliminar", font=("Segoe UI", 10), bg="#DC2626", fg="white", relief=tk.FLAT, cursor="hand2",
                                         command=lambda s=sel: self.eliminar_seleccion(s))
                btn_eliminar.grid(row=fila, column=5, padx=5, pady=5)
                
                fila += 1
    """
    descripción: Procesa el formulario y añade una selección.
    #E: Datos de los Entry y Combo
    #S: Guarda la selección en la lista y en el archivo
    #R: Valida usando el constructor de la clase Seleccion
    Objetivo: Validar y registrar un equipo nacional en el sistema.
    """
    def registrar_seleccion(self):
        codigo = self.entry_codigo_seleccion.get().strip().upper()
        pais_cod = self.combo_pais_seleccion.get()
        
        if codigo == "":
            messagebox.showwarning("Atención", "El código de la selección es obligatorio.")
            return
            
        if pais_cod == "No hay países registrados":
            messagebox.showwarning("Atención", "Debe registrar un país primero.")
            return
            
        # Buscar el objeto Pais
        pais_obj = None
        for p in self.paises:
            if p.codigo_fifa == pais_cod:
                pais_obj = p
                break
                
        if not pais_obj:
            messagebox.showerror("Error", "No se encontró el país seleccionado.")
            return
            
        nueva_sel = Seleccion(codigo, pais_obj)
        if isinstance(nueva_sel, str):
            messagebox.showerror("Error", nueva_sel)
            return
            
        for s in self.selecciones:
            if s.codigo_equipo == codigo:
                messagebox.showwarning("Atención", "Ya existe una selección con el código " + codigo + ".")
                return
                
        # Mantener los jugadores y entrenador si estábamos editando
        if hasattr(self, 'sel_temp_jugadores') and self.sel_temp_jugadores is not None:
            nueva_sel.jugadores = self.sel_temp_jugadores
            nueva_sel.entrenador = self.sel_temp_entrenador
            self.sel_temp_jugadores = None
            self.sel_temp_entrenador = None
                
        self.selecciones = self.selecciones + [nueva_sel]
        self.archivos.guardar_selecciones(self.selecciones)
        
        messagebox.showinfo("Éxito", "La selección " + codigo + " ha sido registrada correctamente.")
        self.hay_cambios = False
        self.mostrar_lista_selecciones()

    """
    descripción: Modifica la configuración de una selección.
    #E: self, sel
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def editar_seleccion(self, sel):
        self.mostrar_registro_seleccion()
        self.entry_codigo_seleccion.delete(0, tk.END)
        self.entry_codigo_seleccion.insert(0, sel.codigo_equipo)
        self.combo_pais_seleccion.set(sel.pais.codigo_fifa)
        
        self.sel_temp_jugadores = sel.jugadores
        self.sel_temp_entrenador = sel.entrenador
        
        nuevas_sels = []
        for s in self.selecciones:
            if s.codigo_equipo != sel.codigo_equipo:
                nuevas_sels = nuevas_sels + [s]
        self.selecciones = nuevas_sels

    """
    descripción: Solicita confirmación y borra un equipo.
    #E: self, sel
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def eliminar_seleccion(self, sel):
        if messagebox.askyesno("Confirmar", "¿Desea eliminar la selección " + sel.codigo_equipo + "?"):
            nuevas_sels = []
            for s in self.selecciones:
                if s.codigo_equipo != sel.codigo_equipo:
                    nuevas_sels = nuevas_sels + [s]
            self.selecciones = nuevas_sels
            self.archivos.guardar_selecciones(self.selecciones)
            self.mostrar_lista_selecciones()

    # =========================================================================
    # PANTALLA: JUGADORES (ACTUALIZADO CON SELECCIONES REALES)
    # =========================================================================
    """
    descripción: Carga la información de los jugadores al programa.
    #E: Ninguna
    #S: Muestra la pantalla de gestión de jugadores
    #R: Pregunta si hay cambios sin guardar
    Objetivo: Restaurar las plantillas de los equipos al reiniciar la aplicación.
    """
    def cargar_jugadores(self):
        if self.hay_cambios:
            if not messagebox.askyesno("Atención", "Hay cambios sin guardar. ¿Desea salir?"):
                return
        self.hay_cambios = False
        self.limpiar_contenido()
        self.crear_encabezado("Gestión de Jugadores", "Registrar futbolistas.")
        
        contenedor = tk.Frame(self.area_contenido, bg=self.color_fondo)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        frame_tabs = tk.Frame(contenedor, bg=self.color_fondo)
        frame_tabs.pack(pady=(0, 5))
        
        self.btn_tab_registro = tk.Button(frame_tabs, text="Registrar Jugador", font=("Segoe UI", 12, "bold"),
                                          bg=self.color_boton_activo, fg=self.color_texto_claro,
                                          relief=tk.FLAT, padx=25, pady=8, cursor="hand2",
                                          command=self.mostrar_registro_jugador)
        self.btn_tab_registro.grid(row=0, column=0, padx=5)
        
        self.btn_tab_lista = tk.Button(frame_tabs, text="Lista de Jugadores", font=("Segoe UI", 12),
                                       bg="#E2E8F0", fg=self.color_texto_oscuro,
                                       relief=tk.FLAT, padx=25, pady=8, cursor="hand2",
                                       command=self.mostrar_lista_jugadores)
        self.btn_tab_lista.grid(row=0, column=1, padx=5)

        self.btn_tab_lista.bind("<Enter>", lambda e: self.btn_tab_lista.config(bg="#CBD5E1"))
        self.btn_tab_lista.bind("<Leave>", lambda e: self.btn_tab_lista.config(bg="#E2E8F0"))
        
        tk.Frame(contenedor, bg="#D1D5DB", height=2).pack(fill=tk.X, pady=(0, 15))
        
        self.frame_contenido_jugadores = tk.Frame(contenedor, bg=self.color_fondo)
        self.frame_contenido_jugadores.pack(fill=tk.BOTH, expand=True)
        
        self.mostrar_registro_jugador()

    """
    descripción: Muestra el formulario para inscribir futbolistas.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def mostrar_registro_jugador(self):
        for w in self.frame_contenido_jugadores.winfo_children():
            w.destroy()
            
        self.btn_tab_registro.configure(bg=self.color_boton_activo, fg=self.color_texto_claro, font=("Segoe UI", 12, "bold"))
        self.btn_tab_lista.configure(bg="#E2E8F0", fg=self.color_texto_oscuro, font=("Segoe UI", 12))

        frame_form = tk.Frame(self.frame_contenido_jugadores, bg=self.color_texto_claro, relief=tk.SOLID, bd=1)
        frame_form.pack(fill=tk.X, padx=100, pady=50)

        tk.Label(frame_form, text="Registrar nuevo jugador", font=("Segoe UI", 16, "bold"), 
                 bg=self.color_texto_claro, fg=self.color_texto_oscuro).grid(row=0, column=0, columnspan=4, sticky="w", padx=30, pady=(20, 15))
        
        tk.Label(frame_form, text="Nombre:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=1, column=0, padx=(30, 10), pady=8, sticky="w")
        self.entry_nombre_jugador = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_nombre_jugador.grid(row=1, column=1, padx=10, pady=8, sticky="ew")
        self.entry_nombre_jugador.bind("<KeyRelease>", lambda e: self.marcar_cambios())
        
        tk.Label(frame_form, text="Apellido:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=1, column=2, padx=(20, 10), pady=8, sticky="w")
        self.entry_apellido_jugador = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_apellido_jugador.grid(row=1, column=3, padx=(10, 30), pady=8, sticky="ew")
        self.entry_apellido_jugador.bind("<KeyRelease>", lambda e: self.marcar_cambios())
        
        tk.Label(frame_form, text="Fecha Nac.:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=2, column=0, padx=(30, 10), pady=8, sticky="w")
        self.entry_fecha_jugador = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_fecha_jugador.grid(row=2, column=1, padx=10, pady=8, sticky="ew")
        self.entry_fecha_jugador.bind("<KeyRelease>", lambda e: self.marcar_cambios())
        
        tk.Label(frame_form, text="Nacionalidad:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=2, column=2, padx=(20, 10), pady=8, sticky="w")
        self.entry_nacionalidad_jugador = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_nacionalidad_jugador.grid(row=2, column=3, padx=(10, 30), pady=8, sticky="ew")
        self.entry_nacionalidad_jugador.bind("<KeyRelease>", lambda e: self.marcar_cambios())

        tk.Label(frame_form, text="Posición:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=3, column=0, padx=(30, 10), pady=8, sticky="w")
        self.combo_posicion = tk.StringVar(value="Delantero")
        menu_posicion = tk.OptionMenu(frame_form, self.combo_posicion, "Portero", "Defensa", "Mediocampista", "Delantero")
        menu_posicion.config(font=("Segoe UI", 11), width=18, relief=tk.SOLID, borderwidth=1, bg=self.color_texto_claro)
        menu_posicion.grid(row=3, column=1, padx=10, pady=8, sticky="ew")
        self.combo_posicion.trace_add("write", lambda *args: self.marcar_cambios())
        
        tk.Label(frame_form, text="Selección:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=3, column=2, padx=(20, 10), pady=8, sticky="w")
        
        # Cargar selecciones reales
        opciones_sel = []
        for s in self.selecciones:
            opciones_sel = opciones_sel + [s.codigo_equipo]
        if len(opciones_sel) == 0:
            opciones_sel = ["No hay selecciones registradas"]
            
        self.combo_seleccion_jug = tk.StringVar(value=opciones_sel[0])
        menu_seleccion = tk.OptionMenu(frame_form, self.combo_seleccion_jug, *opciones_sel)
        menu_seleccion.config(font=("Segoe UI", 11), width=18, relief=tk.SOLID, borderwidth=1, bg=self.color_texto_claro)
        menu_seleccion.grid(row=3, column=3, padx=(10, 30), pady=8, sticky="ew")
        self.combo_seleccion_jug.trace_add("write", lambda *args: self.marcar_cambios())
        
        tk.Label(frame_form, text="Dorsal:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=4, column=0, padx=(30, 10), pady=8, sticky="w")
        self.entry_dorsal = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_dorsal.grid(row=4, column=1, padx=10, pady=8, sticky="ew")
        self.entry_dorsal.bind("<KeyRelease>", lambda e: self.marcar_cambios())
        
        tk.Label(frame_form, text="Puntaje:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=4, column=2, padx=(20, 10), pady=8, sticky="w")
        self.entry_puntaje = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_puntaje.grid(row=4, column=3, padx=(10, 30), pady=8, sticky="ew")
        self.entry_puntaje.bind("<KeyRelease>", lambda e: self.marcar_cambios())

        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)
        
        frame_boton = tk.Frame(frame_form, bg=self.color_texto_claro)
        frame_boton.grid(row=5, column=0, columnspan=4, pady=(25, 30))
        
        tk.Button(frame_boton, text="Guardar jugador", font=("Segoe UI", 12, "bold"), 
                  bg=self.color_boton_activo, fg=self.color_texto_claro, relief=tk.FLAT, cursor="hand2",
                  padx=40, pady=8, command=self.registrar_jugador).pack()

    """
    descripción: Dibuja la lista completa de futbolistas.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def mostrar_lista_jugadores(self):
        for w in self.frame_contenido_jugadores.winfo_children():
            w.destroy()
            
        self.btn_tab_lista.configure(bg=self.color_boton_activo, fg=self.color_texto_claro, font=("Segoe UI", 12, "bold"))
        self.btn_tab_registro.configure(bg="#E2E8F0", fg=self.color_texto_oscuro, font=("Segoe UI", 12))
        
        self.btn_tab_registro.bind("<Enter>", lambda e: self.btn_tab_registro.config(bg="#CBD5E1"))
        self.btn_tab_registro.bind("<Leave>", lambda e: self.btn_tab_registro.config(bg="#E2E8F0"))
        
        frame_superior = tk.Frame(self.frame_contenido_jugadores, bg=self.color_fondo)
        frame_superior.pack(fill=tk.X, pady=(0, 15))

        tk.Label(frame_superior, text="Lista de Jugadores (%d)" % len(self.jugadores), font=("Segoe UI", 20, "bold"), 
                 bg=self.color_fondo, fg=self.color_texto_oscuro).pack(anchor="w", padx=20)

        frame_tabla = self.crear_frame_scrollable(self.frame_contenido_jugadores)
        
        encabezados = ["Nombre", "Apellido", "País", "Posición", "Dorsal", "Puntaje", "Editar", "Eliminar"]
        columna = 0
        for texto in encabezados:
            tk.Label(frame_tabla, text=texto, font=("Segoe UI", 11, "bold"), 
                     bg="#F1F5F9", fg=self.color_texto_oscuro, anchor="w",
                     padx=15, pady=12, relief=tk.SOLID, bd=1).grid(row=0, column=columna, sticky="ew")
            columna += 1
            
        for i in range(8):
            frame_tabla.columnconfigure(i, weight=1)
            
        if len(self.jugadores) == 0:
            tk.Label(frame_tabla, text="No hay jugadores registrados.", 
                     font=("Segoe UI", 12), bg=self.color_texto_claro, fg=self.color_texto_gris, justify="center").grid(row=1, column=0, columnspan=8, pady=60)
        else:
            fila = 1
            for jugador in self.jugadores:
                tk.Label(frame_tabla, text=jugador.nombre, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=0, sticky="ew")
                tk.Label(frame_tabla, text=jugador.apellido, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=1, sticky="ew")
                tk.Label(frame_tabla, text=jugador.nacionalidad, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=2, sticky="ew")
                tk.Label(frame_tabla, text=jugador.posicion, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=3, sticky="ew")
                tk.Label(frame_tabla, text=str(jugador.dorsal), font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=4, sticky="ew")
                tk.Label(frame_tabla, text=str(jugador.puntaje_individual), font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=5, sticky="ew")
                
                btn_editar = tk.Button(frame_tabla, text="Editar", font=("Segoe UI", 10), bg="#FBBF24", relief=tk.FLAT, cursor="hand2",
                                       command=lambda j=jugador: self.editar_jugador(j))
                btn_editar.grid(row=fila, column=6, padx=5, pady=5)
                
                btn_eliminar = tk.Button(frame_tabla, text="Eliminar", font=("Segoe UI", 10), bg="#DC2626", fg="white", relief=tk.FLAT, cursor="hand2",
                                         command=lambda j=jugador: self.eliminar_jugador(j))
                btn_eliminar.grid(row=fila, column=7, padx=5, pady=5)
                fila += 1

    """
    descripción: Valida y guarda los datos de un nuevo jugador.
    #E: Datos de los Entry
    #S: Guarda el jugador
    #R: Valida usando el constructor de Futbolista
    Objetivo: Integrar un futbolista a la plantilla de una selección específica.
    """
    def registrar_jugador(self):
        nombre = self.entry_nombre_jugador.get().strip()
        apellido = self.entry_apellido_jugador.get().strip()
        fecha = self.entry_fecha_jugador.get().strip()
        
        if len(fecha) >= 4:
            anio_str = fecha[-4:]
            if self.EsEntero(anio_str):
                anio = int(anio_str)
                if anio <= 1982:
                    messagebox.showwarning("Atención", "El jugador es demasiado mayor para jugar un mundial (44+ años).")
                    return
                if anio >= 2011:
                    messagebox.showwarning("Atención", "El jugador es demasiado joven para jugar un mundial (menor de 15 años).")
                    return
                    
        nacionalidad = self.entry_nacionalidad_jugador.get().strip()
        posicion = self.combo_posicion.get()
        dorsal_str = self.entry_dorsal.get().strip()
        puntaje_str = self.entry_puntaje.get().strip()
        
        if not self.EsEntero(dorsal_str) or not self.EsEntero(puntaje_str):
            messagebox.showwarning("Atención", "Dorsal y Puntaje deben ser números válidos.")
            return
        
        dorsal = int(dorsal_str)
        puntaje = int(puntaje_str)
        
        if dorsal == 1 and posicion != "Portero":
            messagebox.showwarning("Atención", "El dorsal 1 está reservado exclusivamente para los Porteros.")
            return
            
        seleccion_cod = self.combo_seleccion_jug.get()
        if seleccion_cod != "No hay selecciones registradas":
            for sel in self.selecciones:
                if sel.codigo_equipo == seleccion_cod:
                    for j in sel.jugadores:
                        if j.dorsal == dorsal:
                            messagebox.showwarning("Atención", "El dorsal " + str(dorsal) + " ya está ocupado por " + j.nombre + " en esta selección.")
                            return
        
        nuevo_jugador = Futbolista(nombre, apellido, fecha, nacionalidad, dorsal, posicion, puntaje)
        if isinstance(nuevo_jugador, str):
            messagebox.showerror("Error", nuevo_jugador)
            return
        
        if seleccion_cod != "No hay selecciones registradas":
            for sel in self.selecciones:
                if sel.codigo_equipo == seleccion_cod:
                    resultado = sel.agregar_jugador(nuevo_jugador)
                    if not resultado: 
                        messagebox.showwarning("Atención", "La selección ya tiene el máximo de 20 jugadores.")
                    break
        
        self.jugadores = self.jugadores + [nuevo_jugador]
        
        messagebox.showinfo("Éxito", "Jugador " + nombre + " registrado correctamente.")
        self.hay_cambios = False
        self.mostrar_lista_jugadores()
        
        self.archivos.guardar_jugadores(self.selecciones)
        
    """
    descripción: Permite alterar la información de un jugador.
    #E: self, jugador
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def editar_jugador(self, jugador):
        self.mostrar_registro_jugador()
        self.entry_nombre_jugador.delete(0, tk.END)
        self.entry_nombre_jugador.insert(0, jugador.nombre)
        self.entry_apellido_jugador.delete(0, tk.END)
        self.entry_apellido_jugador.insert(0, jugador.apellido)
        self.entry_fecha_jugador.delete(0, tk.END)
        self.entry_fecha_jugador.insert(0, jugador.fecha_nacimiento)
        self.entry_nacionalidad_jugador.delete(0, tk.END)
        self.entry_nacionalidad_jugador.insert(0, jugador.nacionalidad)
        self.combo_posicion.set(jugador.posicion)
        self.entry_dorsal.delete(0, tk.END)
        self.entry_dorsal.insert(0, str(jugador.dorsal))
        self.entry_puntaje.delete(0, tk.END)
        self.entry_puntaje.insert(0, str(jugador.puntaje_individual))
        
        for sel in self.selecciones:
            if jugador in sel.jugadores:
                self.combo_seleccion_jug.set(sel.codigo_equipo)
                break
                
        self.eliminar_jugador_silencioso(jugador)

    """
    descripción: Borra internamente un jugador de memoria.
    #E: self, jugador
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def eliminar_jugador_silencioso(self, jugador):
        nuevos_jugadores = []
        for j in self.jugadores:
            if j.nombre != jugador.nombre or j.apellido != jugador.apellido:
                nuevos_jugadores = nuevos_jugadores + [j]
        self.jugadores = nuevos_jugadores
        
        for sel in self.selecciones:
            nuevos_sel = []
            encontrado = False
            for j in sel.jugadores:
                if j.nombre == jugador.nombre and j.apellido == jugador.apellido:
                    encontrado = True
                else:
                    nuevos_sel = nuevos_sel + [j]
            if encontrado:
                sel.jugadores = nuevos_sel

    """
    descripción: Saca a un jugador de la plantilla.
    #E: self, jugador
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def eliminar_jugador(self, jugador):
        if messagebox.askyesno("Confirmar", "¿Desea eliminar al jugador " + jugador.nombre + "?"):
            self.eliminar_jugador_silencioso(jugador)
            self.mostrar_lista_jugadores()
            self.archivos.guardar_jugadores(self.selecciones)

    # =========================================================================
    # PANTALLA: ENTRENADORES (ACTUALIZADO CON SELECCIONES REALES)
    # =========================================================================
    """
    descripción: Abre la vista principal de la sección entrenadores.
    #E: Ninguna
    #S: Muestra la pantalla de gestión de entrenadores
    #R: Pregunta si hay cambios sin guardar
    Objetivo: Gestionar a los directores técnicos desde la interfaz.
    """
    def cargar_entrenadores(self):
        if self.hay_cambios:
            if not messagebox.askyesno("Atención", "Hay cambios sin guardar. ¿Desea salir?"):
                return
        self.hay_cambios = False
        self.limpiar_contenido()
        self.crear_encabezado("Gestión de Entrenadores", "Registrar entrenadores.")
        
        contenedor = tk.Frame(self.area_contenido, bg=self.color_fondo)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        frame_tabs = tk.Frame(contenedor, bg=self.color_fondo)
        frame_tabs.pack(pady=(0, 5))
        
        self.btn_tab_registro_ent = tk.Button(frame_tabs, text="Registrar Entrenador", font=("Segoe UI", 12, "bold"),
                                              bg=self.color_boton_activo, fg=self.color_texto_claro,
                                              relief=tk.FLAT, padx=25, pady=8, cursor="hand2",
                                              command=self.mostrar_registro_entrenador)
        self.btn_tab_registro_ent.grid(row=0, column=0, padx=5)
        
        self.btn_tab_lista_ent = tk.Button(frame_tabs, text="Lista de Entrenadores", font=("Segoe UI", 12),
                                           bg="#E2E8F0", fg=self.color_texto_oscuro,
                                           relief=tk.FLAT, padx=25, pady=8, cursor="hand2",
                                           command=self.mostrar_lista_entrenadores)
        self.btn_tab_lista_ent.grid(row=0, column=1, padx=5)

        self.btn_tab_lista_ent.bind("<Enter>", lambda e: self.btn_tab_lista_ent.config(bg="#CBD5E1"))
        self.btn_tab_lista_ent.bind("<Leave>", lambda e: self.btn_tab_lista_ent.config(bg="#E2E8F0"))
        
        tk.Frame(contenedor, bg="#D1D5DB", height=2).pack(fill=tk.X, pady=(0, 15))
        
        self.frame_contenido_entrenadores = tk.Frame(contenedor, bg=self.color_fondo)
        self.frame_contenido_entrenadores.pack(fill=tk.BOTH, expand=True)
        
        self.mostrar_registro_entrenador()

    """
    descripción: Despliega el formulario de entrenadores.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def mostrar_registro_entrenador(self):
        for w in self.frame_contenido_entrenadores.winfo_children():
            w.destroy()
            
        self.btn_tab_registro_ent.configure(bg=self.color_boton_activo, fg=self.color_texto_claro, font=("Segoe UI", 12, "bold"))
        self.btn_tab_lista_ent.configure(bg="#E2E8F0", fg=self.color_texto_oscuro, font=("Segoe UI", 12))

        frame_form = tk.Frame(self.frame_contenido_entrenadores, bg=self.color_texto_claro, relief=tk.SOLID, bd=1)
        frame_form.pack(fill=tk.X, padx=100, pady=50)

        tk.Label(frame_form, text="Registrar nuevo entrenador", font=("Segoe UI", 16, "bold"), 
                 bg=self.color_texto_claro, fg=self.color_texto_oscuro).grid(row=0, column=0, columnspan=4, sticky="w", padx=30, pady=(20, 15))
        
        tk.Label(frame_form, text="Nombre:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=1, column=0, padx=(30, 10), pady=8, sticky="w")
        self.entry_nombre_ent = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_nombre_ent.grid(row=1, column=1, padx=10, pady=8, sticky="ew")
        self.entry_nombre_ent.bind("<KeyRelease>", lambda e: self.marcar_cambios())
        
        tk.Label(frame_form, text="Apellido:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=1, column=2, padx=(20, 10), pady=8, sticky="w")
        self.entry_apellido_ent = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_apellido_ent.grid(row=1, column=3, padx=(10, 30), pady=8, sticky="ew")
        self.entry_apellido_ent.bind("<KeyRelease>", lambda e: self.marcar_cambios())
        
        tk.Label(frame_form, text="Fecha Nac.:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=2, column=0, padx=(30, 10), pady=8, sticky="w")
        self.entry_fecha_ent = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_fecha_ent.grid(row=2, column=1, padx=10, pady=8, sticky="ew")
        self.entry_fecha_ent.bind("<KeyRelease>", lambda e: self.marcar_cambios())
        
        tk.Label(frame_form, text="Nacionalidad:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=2, column=2, padx=(20, 10), pady=8, sticky="w")
        self.entry_nacionalidad_ent = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_nacionalidad_ent.grid(row=2, column=3, padx=(10, 30), pady=8, sticky="ew")
        self.entry_nacionalidad_ent.bind("<KeyRelease>", lambda e: self.marcar_cambios())

        tk.Label(frame_form, text="Selección:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=3, column=0, padx=(30, 10), pady=8, sticky="w")
        
        # Cargar selecciones reales
        opciones_sel = []
        for s in self.selecciones:
            opciones_sel = opciones_sel + [s.codigo_equipo]
        if len(opciones_sel) == 0:
            opciones_sel = ["No hay selecciones registradas"]
            
        self.combo_seleccion_ent = tk.StringVar(value=opciones_sel[0])
        menu_seleccion = tk.OptionMenu(frame_form, self.combo_seleccion_ent, *opciones_sel)
        menu_seleccion.config(font=("Segoe UI", 11), width=18, relief=tk.SOLID, borderwidth=1, bg=self.color_texto_claro)
        menu_seleccion.grid(row=3, column=1, padx=10, pady=8, sticky="ew")
        self.combo_seleccion_ent.trace_add("write", lambda *args: self.marcar_cambios())
        
        tk.Label(frame_form, text="Licencia:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=3, column=2, padx=(20, 10), pady=8, sticky="w")
        self.combo_licencia = tk.StringVar(value="Pro")
        menu_licencia = tk.OptionMenu(frame_form, self.combo_licencia, "Pro", "UEFA A", "UEFA B", "Nacional")
        menu_licencia.config(font=("Segoe UI", 11), width=18, relief=tk.SOLID, borderwidth=1, bg=self.color_texto_claro)
        menu_licencia.grid(row=3, column=3, padx=(10, 30), pady=8, sticky="ew")
        self.combo_licencia.trace_add("write", lambda *args: self.marcar_cambios())
        
        tk.Label(frame_form, text="Experiencia:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=4, column=0, padx=(30, 10), pady=8, sticky="w")
        self.entry_experiencia = tk.Entry(frame_form, font=("Segoe UI", 11), relief=tk.SOLID, borderwidth=1)
        self.entry_experiencia.grid(row=4, column=1, padx=10, pady=8, sticky="ew")
        self.entry_experiencia.bind("<KeyRelease>", lambda e: self.marcar_cambios())
        
        tk.Label(frame_form, text="Sistema:", font=("Segoe UI", 11), bg=self.color_texto_claro).grid(row=4, column=2, padx=(20, 10), pady=8, sticky="w")
        self.combo_sistema = tk.StringVar(value="4-3-3")
        menu_sistema = tk.OptionMenu(frame_form, self.combo_sistema, "4-3-3", "4-4-2", "3-5-2", "5-3-2")
        menu_sistema.config(font=("Segoe UI", 11), width=18, relief=tk.SOLID, borderwidth=1, bg=self.color_texto_claro)
        menu_sistema.grid(row=4, column=3, padx=(10, 30), pady=8, sticky="ew")

        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)
        
        frame_boton = tk.Frame(frame_form, bg=self.color_texto_claro)
        frame_boton.grid(row=5, column=0, columnspan=4, pady=(25, 30))
        
        tk.Button(frame_boton, text="Guardar entrenador", font=("Segoe UI", 12, "bold"), 
                  bg=self.color_boton_activo, fg=self.color_texto_claro, relief=tk.FLAT, cursor="hand2",
                  padx=40, pady=8, command=self.registrar_entrenador).pack()

    """
    descripción: Renderiza la tabla de directores técnicos.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def mostrar_lista_entrenadores(self):
        for w in self.frame_contenido_entrenadores.winfo_children():
            w.destroy()
            
        self.btn_tab_lista_ent.configure(bg=self.color_boton_activo, fg=self.color_texto_claro, font=("Segoe UI", 12, "bold"))
        self.btn_tab_registro_ent.configure(bg="#E2E8F0", fg=self.color_texto_oscuro, font=("Segoe UI", 12))
        
        self.btn_tab_registro_ent.bind("<Enter>", lambda e: self.btn_tab_registro_ent.config(bg="#CBD5E1"))
        self.btn_tab_registro_ent.bind("<Leave>", lambda e: self.btn_tab_registro_ent.config(bg="#E2E8F0"))
        
        frame_superior = tk.Frame(self.frame_contenido_entrenadores, bg=self.color_fondo)
        frame_superior.pack(fill=tk.X, pady=(0, 15))

        tk.Label(frame_superior, text="Lista de Entrenadores (%d)" % len(self.entrenadores), font=("Segoe UI", 20, "bold"), 
                 bg=self.color_fondo, fg=self.color_texto_oscuro).pack(anchor="w", padx=20)

        frame_tabla = self.crear_frame_scrollable(self.frame_contenido_entrenadores)
        
        encabezados = ["Nombre", "Apellido", "Licencia", "Experiencia", "Sistema", "Eliminar"]
        columna = 0
        for texto in encabezados:
            tk.Label(frame_tabla, text=texto, font=("Segoe UI", 11, "bold"), 
                     bg="#F1F5F9", fg=self.color_texto_oscuro, anchor="w",
                     padx=15, pady=12, relief=tk.SOLID, bd=1).grid(row=0, column=columna, sticky="ew")
            columna += 1
            
        for i in range(5):
            frame_tabla.columnconfigure(i, weight=1)
            
        if len(self.entrenadores) == 0:
            tk.Label(frame_tabla, text="No hay entrenadores registrados.", 
                     font=("Segoe UI", 12), bg=self.color_texto_claro, fg=self.color_texto_gris, justify="center").grid(row=1, column=0, columnspan=6, pady=60)
        else:
            fila = 1
            for ent in self.entrenadores:
                tk.Label(frame_tabla, text=ent.nombre, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=0, sticky="ew")
                tk.Label(frame_tabla, text=ent.apellido, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=1, sticky="ew")
                tk.Label(frame_tabla, text=ent.licencia, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=2, sticky="ew")
                tk.Label(frame_tabla, text=str(ent.experiencia_anios), font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=3, sticky="ew")
                tk.Label(frame_tabla, text=ent.sistema_juego, font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=4, sticky="ew")
                
                btn_eliminar = tk.Button(frame_tabla, text="Eliminar", font=("Segoe UI", 10), bg="#DC2626", fg="white", relief=tk.FLAT, cursor="hand2",
                                         command=lambda e=ent: self.eliminar_entrenador(e))
                btn_eliminar.grid(row=fila, column=5, padx=5, pady=5)
                fila += 1

    """
    descripción: Valida y guarda un entrenador nuevo.
    #E: Datos de los Entry
    #S: Guarda el entrenador
    #R: Valida usando el constructor de Entrenador
    Objetivo: Vincular a un director técnico con una selección nacional.
    """
    def registrar_entrenador(self):
        nombre = self.entry_nombre_ent.get().strip()
        apellido = self.entry_apellido_ent.get().strip()
        fecha = self.entry_fecha_ent.get().strip()
        
        if len(fecha) >= 4:
            anio_str = fecha[-4:]
            if self.EsEntero(anio_str):
                anio = int(anio_str)
                if anio > 1996:
                    messagebox.showwarning("Atención", "El entrenador es demasiado joven para dirigir (Mínimo 30 años).")
                    return
                    
        nacionalidad = self.entry_nacionalidad_ent.get().strip()
        licencia = self.combo_licencia.get()
        exp_str = self.entry_experiencia.get().strip()
        sistema = self.combo_sistema.get()
        
        if not self.EsEntero(exp_str):
            messagebox.showwarning("Atención", "La experiencia debe ser un número válido.")
            return
        
        experiencia = int(exp_str)
        
        seleccion_cod = self.combo_seleccion_ent.get()
        if seleccion_cod == "No hay selecciones registradas":
            messagebox.showwarning("Atención", "Debe registrar una selección primero.")
            return

        seleccion_obj = None
        for sel in self.selecciones:
            if sel.codigo_equipo == seleccion_cod:
                seleccion_obj = sel
                break

        if seleccion_obj.entrenador is not None:
            messagebox.showwarning("Atención", "La selección " + seleccion_cod + " ya tiene un entrenador asignado.")
            return
        
        nuevo_ent = Entrenador(nombre, apellido, fecha, nacionalidad, licencia, experiencia, sistema)
        if isinstance(nuevo_ent, str):
            messagebox.showerror("Error", nuevo_ent)
            return
        
        seleccion_obj.asignar_entrenador(nuevo_ent)
        
        self.entrenadores = self.entrenadores + [nuevo_ent]
        
        messagebox.showinfo("Éxito", "Entrenador " + nombre + " registrado correctamente.")
        self.hay_cambios = False
        self.mostrar_lista_entrenadores()
        
        self.archivos.guardar_selecciones(self.selecciones)

    """
    descripción: Despide y elimina a un entrenador del sistema.
    #E: self, ent
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def eliminar_entrenador(self, ent):
        if messagebox.askyesno("Confirmar", "¿Desea eliminar al entrenador " + ent.nombre + "?"):
            nuevos_ent = []
            for e in self.entrenadores:
                if e.nombre != ent.nombre or e.apellido != ent.apellido:
                    nuevos_ent = nuevos_ent + [e]
            self.entrenadores = nuevos_ent
            self.mostrar_lista_entrenadores()
            
            self.archivos.guardar_selecciones(self.selecciones)
    # =========================================================================
    # OTRAS PANTALLAS
    # =========================================================================
    """
    descripción: Despliega la ventana de configuración del torneo.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def cargar_configurar(self): 
        if self.hay_cambios:
            if not messagebox.askyesno("Atención", "Hay cambios sin guardar. ¿Desea salir?"): return
        self.hay_cambios = False
        self.limpiar_contenido()
        self.crear_encabezado("Configurar Mundial", "Divide las selecciones registradas en grupos aleatorios.")
        
        # Asegurarnos de usar las selecciones más actualizadas
        self.mi_mundial.selecciones = self.selecciones
        
        contenedor = tk.Frame(self.area_contenido, bg=self.color_fondo)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        tk.Label(contenedor, text="Cantidad de grupos deseada:", font=("Segoe UI", 14), bg=self.color_fondo, fg=self.color_texto_oscuro).pack(pady=(20, 10))
        self.entry_grupos = tk.Entry(contenedor, font=("Segoe UI", 14), justify="center", width=10)
        self.entry_grupos.pack(pady=10)
        self.entry_grupos.insert(0, "2") # Mínimo 2 por defecto
        
        tk.Button(contenedor, text="Crear Grupos", font=("Segoe UI", 14, "bold"), bg=self.color_boton_activo, fg=self.color_texto_claro, cursor="hand2", padx=20, pady=10, command=self.ejecutar_crear_grupos).pack(pady=20)
        
        self.texto_grupos = tk.Text(contenedor, font=("Consolas", 12), bg=self.color_texto_claro, fg=self.color_texto_oscuro, height=15, width=60, state=tk.DISABLED)
        self.texto_grupos.pack(pady=20)

    """
    descripción: Realiza el sorteo de selecciones a los grupos.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def ejecutar_crear_grupos(self):
        if len(self.selecciones) < 8:
            messagebox.showerror("Error", "No se puede crear grupo, selecciones insuficientes.")
            return
            
        cant_str = self.entry_grupos.get().strip()
        if not self.EsEntero(cant_str):
            messagebox.showwarning("Atención", "La cantidad debe ser un número entero.")
            return
            
        cantidad = int(cant_str)
        if cantidad < 2:
            messagebox.showwarning("Atención", "El mínimo de grupos es 2.")
            return
            
        resultado = self.mi_mundial.crear_grupos(cantidad)
        if isinstance(resultado, str):
            messagebox.showerror("Error", resultado)
            return
            
        for sel in self.selecciones:
            sel.total_goles_favor = 0
            sel.total_goles_contra = 0
            sel.total_tarjetas_amarillas = 0
            sel.total_tarjetas_rojas = 0
            sel.puntos = 0
            sel.partidos_jugados = 0
            sel.partidos_ganados = 0
            sel.partidos_empatados = 0
            sel.partidos_perdidos = 0
            for j in sel.jugadores:
                j.goles = 0
                j.asistencias = 0
                j.amarillas = 0
                j.rojas = 0
            
        texto = ""
        for i in range(len(self.mi_mundial.grupos)):
            grupo = self.mi_mundial.grupos[i]
            texto = texto + f"--- {grupo.nombre_grupo.upper()} ---\n"
            for eq in grupo.equipos:
                texto = texto + f"- {eq.pais.nombre}\n"
            texto = texto + "\n"
            
        self.texto_grupos.config(state=tk.NORMAL)
        self.texto_grupos.delete(1.0, tk.END)
        self.texto_grupos.insert(tk.END, texto)
        self.texto_grupos.config(state=tk.DISABLED)
        messagebox.showinfo("Éxito", "Los grupos han sido creados correctamente.")
        
    """
    descripción: Abre el panel de control de simulación.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def cargar_simular(self): 
        if self.hay_cambios:
            if not messagebox.askyesno("Atención", "Hay cambios sin guardar. ¿Desea salir?"): return
        self.hay_cambios = False
        self.limpiar_contenido()
        self.crear_encabezado("Simular Mundial", "Juega los partidos y descubre al campeón.")
        
        contenedor = tk.Frame(self.area_contenido, bg=self.color_fondo)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        frame_botones = tk.Frame(contenedor, bg=self.color_fondo)
        frame_botones.pack(pady=20)
        
        tk.Button(frame_botones, text="1. Simular Fase de Grupos", font=("Segoe UI", 12, "bold"), bg="#2563EB", fg="white", cursor="hand2", width=25, pady=10, command=self.simular_grupos).grid(row=0, column=0, padx=10)
        
        tk.Button(frame_botones, text="2. Jugar Eliminatorias", font=("Segoe UI", 12, "bold"), bg="#F59E0B", fg="white", cursor="hand2", width=25, pady=10, command=self.simular_eliminatorias).grid(row=0, column=1, padx=10)
        
        tk.Button(frame_botones, text="3. Exportar Reportes", font=("Segoe UI", 12, "bold"), bg="#10B981", fg="white", cursor="hand2", width=25, pady=10, command=self.exportar_reportes).grid(row=0, column=2, padx=10)
        
        frame_texto = tk.Frame(contenedor)
        frame_texto.pack(pady=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.texto_simulacion = tk.Text(frame_texto, font=("Consolas", 12), bg=self.color_texto_claro, fg=self.color_texto_oscuro, height=20, width=90, state=tk.DISABLED, yscrollcommand=scrollbar.set)
        self.texto_simulacion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.texto_simulacion.yview)

    """
    descripción: Ejecuta la primera fase del torneo de forma automática.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def simular_grupos(self):
        if len(self.mi_mundial.grupos) == 0:
            messagebox.showwarning("Atención", "Debe configurar los grupos primero.")
            return
            
        if len(self.mi_mundial.grupos[0].partidos) > 0:
            messagebox.showwarning("Atención", "La fase de grupos ya ha sido simulada. Si desea jugar de nuevo, vuelva a Crear Grupos.")
            return
            
        for grupo in self.mi_mundial.grupos:
            for equipo in grupo.equipos:
                if len(equipo.jugadores) < 1:
                    messagebox.showwarning("Atención", "La selección de " + equipo.pais.nombre + " no tiene jugadores. ¡Debe registrar al menos 1!")
                    return
            
        self.mi_mundial.jugar_fase_grupos()
        tabla = self.mi_mundial.mostrar_tabla_general()
        
        self.texto_simulacion.config(state=tk.NORMAL)
        self.texto_simulacion.delete(1.0, tk.END)
        self.texto_simulacion.insert(tk.END, tabla)
        self.texto_simulacion.config(state=tk.DISABLED)
        messagebox.showinfo("Éxito", "Fase de grupos jugada con éxito.")

    """
    descripción: Ejecuta los playoffs desde octavos hasta la final.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def simular_eliminatorias(self):
        if len(self.mi_mundial.grupos) == 0:
            messagebox.showwarning("Atención", "Debe jugar la fase de grupos primero.")
            return
            
        # Determinar campeón usa el while manual de fases
        self.mi_mundial.determinar_campeon()
        campeon = self.mi_mundial.campeon
        
        if campeon:
            mensaje = ""
            for fase in self.mi_mundial.fases:
                mensaje += fase.mostrar_juegos() + "\n"
                
            mensaje += f"**************************************************\n"
            mensaje += f"  ¡¡¡ EL CAMPEÓN DEL MUNDO ES {campeon.pais.nombre.upper()} !!!\n"
            mensaje += f"**************************************************\n\n"
            mensaje += f"Felicidades al equipo de {campeon.pais.nombre}.\n"
            
            self.texto_simulacion.config(state=tk.NORMAL)
            self.texto_simulacion.delete(1.0, tk.END)
            self.texto_simulacion.insert(tk.END, mensaje)
            self.texto_simulacion.config(state=tk.DISABLED)
            messagebox.showinfo("¡Tenemos Campeón!", f"¡{campeon.pais.nombre} ganó el mundial!")
        else:
            messagebox.showerror("Error", "No se pudo determinar al campeón.")

    """
    descripción: Genera los archivos .txt con los resultados finales.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def exportar_reportes(self):
        todos_los_partidos = []
        for grupo in self.mi_mundial.grupos:
            todos_los_partidos = todos_los_partidos + grupo.partidos
        for fase in self.mi_mundial.fases:
            todos_los_partidos = todos_los_partidos + fase.partidos
            
        if len(todos_los_partidos) == 0:
            messagebox.showwarning("Atención", "Debe jugar partidos antes de exportar.")
            return
            
        self.archivos.guardar_rankings(self.mi_mundial.selecciones)
        self.archivos.guardar_partidos(todos_los_partidos)
        messagebox.showinfo("Reportes", "Los archivos TXT se han guardado exitosamente en la carpeta 'datos'.")

    """
    descripción: Abre el panel visor de reportes del torneo.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def cargar_estadisticas(self): 
        if self.hay_cambios:
            if not messagebox.askyesno("Atención", "Hay cambios sin guardar. ¿Desea salir?"): return
        self.hay_cambios = False
        self.limpiar_contenido()
        self.crear_encabezado("Estadísticas", "Visualiza los resultados del torneo almacenados en los TXT.")
        
        contenedor = tk.Frame(self.area_contenido, bg=self.color_fondo)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        
        frame_botones = tk.Frame(contenedor, bg=self.color_fondo)
        frame_botones.pack(pady=10)
        
        tk.Button(frame_botones, text="Ver Ranking Goleadores", font=("Segoe UI", 11, "bold"), bg=self.color_menu, fg=self.color_texto_claro, cursor="hand2", padx=15, pady=8, command=self.ver_goleadores).grid(row=0, column=0, padx=10)
        tk.Button(frame_botones, text="Ver Ranking Selecciones", font=("Segoe UI", 11, "bold"), bg=self.color_menu, fg=self.color_texto_claro, cursor="hand2", padx=15, pady=8, command=self.ver_selecciones).grid(row=0, column=1, padx=10)
        tk.Button(frame_botones, text="Ver Récords", font=("Segoe UI", 11, "bold"), bg=self.color_menu, fg=self.color_texto_claro, cursor="hand2", padx=15, pady=8, command=self.ver_records).grid(row=0, column=2, padx=10)
        
        self.frame_tabla_estadisticas = tk.Frame(contenedor, bg=self.color_fondo)
        self.frame_tabla_estadisticas.pack(fill=tk.BOTH, expand=True, pady=20)

    """
    descripción: Renderiza el ranking de máximos anotadores.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def ver_goleadores(self):
        ruta = self.archivos.conseguir_ruta("ranking_goleadores.txt")
        self.mostrar_archivo_txt(ruta, "Aún no hay datos de goleadores (simule y exporte primero).")

    """
    descripción: Muestra la tabla general de todas las selecciones.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def ver_selecciones(self):
        ruta = self.archivos.conseguir_ruta("ranking_selecciones.txt")
        self.mostrar_archivo_txt(ruta, "Aún no hay datos de selecciones (simule y exporte primero).")

    """
    descripción: Muestra curiosidades y datos destacables del torneo.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def ver_records(self):
        ruta = self.archivos.conseguir_ruta("records.txt")
        self.mostrar_archivo_txt(ruta, "Aún no hay datos de récords (simule y exporte primero).")

    """
    descripción: Lee un reporte de disco y lo dibuja en una tabla.
    #E: self, ruta, mensaje_error
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def mostrar_archivo_txt(self, ruta, mensaje_error):
        for w in self.frame_tabla_estadisticas.winfo_children():
            w.destroy()
            
        if not os.path.exists(ruta):
            tk.Label(self.frame_tabla_estadisticas, text=mensaje_error, font=("Segoe UI", 12), bg=self.color_fondo, fg=self.color_texto_gris).pack(pady=60)
            return
            
        frame_tabla = tk.Frame(self.frame_tabla_estadisticas, bg=self.color_texto_claro, relief=tk.SOLID, bd=1)
        frame_tabla.pack(fill=tk.BOTH, expand=True)
        
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                # Leer líneas
                lineas = []
                for linea in f:
                    # limpiar el salto de linea al final si lo hay
                    if linea[-1] == '\n':
                        lineas = lineas + [linea[:-1]]
                    else:
                        lineas = lineas + [linea]
                    
            if len(lineas) == 0:
                tk.Label(frame_tabla, text="No hay datos en el archivo.", font=("Segoe UI", 12), bg=self.color_texto_claro).pack(pady=20)
                return
                
            # Procesar el encabezado
            encabezado = self.archivos.separar_linea(lineas[0], "|")
            columna = 0
            for texto in encabezado:
                tk.Label(frame_tabla, text=texto.strip(), font=("Segoe UI", 11, "bold"), 
                         bg="#F1F5F9", fg=self.color_texto_oscuro, anchor="w",
                         padx=15, pady=12, relief=tk.SOLID, bd=1).grid(row=0, column=columna, sticky="ew")
                frame_tabla.columnconfigure(columna, weight=1)
                columna += 1
                
            # Procesar datos
            fila = 1
            for i in range(1, len(lineas)):
                datos = self.archivos.separar_linea(lineas[i], "|")
                columna = 0
                for dato in datos:
                    tk.Label(frame_tabla, text=dato.strip(), font=("Segoe UI", 11), bg=self.color_texto_claro, anchor="w", padx=15, pady=10).grid(row=fila, column=columna, sticky="ew")
                    columna += 1
                fila += 1
                
        except Exception as e:
            tk.Label(self.frame_tabla_estadisticas, text="Error al leer el archivo.", font=("Segoe UI", 12), fg="red").pack(pady=20)

    """
    descripción: Regresa al panel de bienvenida principal.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def volver_inicio(self):
        if self.hay_cambios:
            if not messagebox.askyesno("Atención", "Hay cambios sin guardar. ¿Desea volver al inicio?"):
                return
        self.hay_cambios = False
        self.mostrar_bienvenida()

    """
    descripción: Pregunta al usuario si desea guardar antes de salir.
    #E: self
    #S: Actualiza la interfaz o retorna valores.
    #R: Ninguna
    Objetivo: Ejecutar la funcionalidad de la interfaz.
    """
    def confirmar_salir(self):
        if messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir del sistema?"):
            self.destroy()

    # =========================================================================
    # FUNCIONES PARA VALIDAR
    # =========================================================================
    """
    descripción: Verifica si un string representa un número entero.
    #E: texto (el string a revisar)
    #S: True si es número, False si no
    #R: El texto debe ser un string
    Objetivo: Validar que las entradas numéricas del formulario sean correctas.
    """
    def EsEntero(self, texto):
        if not isinstance(texto, str):
            return False
        digitos = "0123456789"
        if texto == "":
            return False
        for caracter in texto:
            if caracter not in digitos:
                return False
        return True

# =========================================================================
# EJECUCIÓN
# =========================================================================
if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()

