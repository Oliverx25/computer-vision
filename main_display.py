import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
from pathlib import Path
import threading

class MainDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Visión por Computadora")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')

        # Configurar el estilo
        self.setup_styles()

        # Configurar la interfaz
        self.setup_interface()

        # Diccionario para mantener referencias a las ventanas de programas
        self.program_windows = {}

    def setup_styles(self):
        """Configurar estilos personalizados para la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configurar colores
        style.configure('Main.TFrame', background='#2c3e50')
        style.configure('Title.TLabel',
                       background='#2c3e50',
                       foreground='#1cf0f0',
                       font=('Arial', 24, 'bold'))
        style.configure('Subtitle.TLabel',
                       background='#2c3e50',
                       foreground='#1aaaaa',
                       font=('Arial', 12))

    def setup_interface(self):
        """Configurar la interfaz principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, style='Main.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título principal
        title_label = ttk.Label(main_frame,
                               text="Sistema de Visión por Computadora",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 10))


        # Frame para los botones
        buttons_frame = ttk.Frame(main_frame, style='Main.TFrame')
        buttons_frame.pack(expand=True)

        # Configurar los botones
        self.create_program_buttons(buttons_frame)

    def create_program_buttons(self, parent):
        """Crear los botones para cada programa"""
        programs = [
            {
                'name': 'Círculo y Línea',
                'description': 'Generador de formas geométricas con algoritmos de Bresenham y Midle Point Circle',
                'command': lambda: self.open_program('circulo_linea', Path("General/1-circulo-y-linea/main.py")),
                'color': '#e74c3c'
            },
            {
                'name': 'Filtros de Color',
                'description': 'Procesamiento de imágenes BMP con filtros de color',
                'command': lambda: self.open_program('filtros_color', Path("General/2-modos-color/filtros_color.py")),
                'color': '#3498db'
            },
            {
                'name': 'Reconocedor de Números',
                'description': 'Sistema de reconocimiento de dígitos en imágenes',
                'command': lambda: self.open_program('reconocedor_numeros', Path("General/3-reconocedor-numeros/reconocedor_numeros.py")),
                'color': '#2ecc71'
            },
            {
                'name': 'Reconocedor con Perceptron',
                'description': 'Reconocedor de dígitos con Perceptron',
                'command': lambda: self.open_program('reconocedor_perceptron', Path("General/3-reconocedor-perceptron/reconocedor_numeros_perc.py")),
                'color': '#f39c12'
            }
        ]

        # Crear grid de botones (2x2)
        for i, program in enumerate(programs):
            row = i // 2
            col = i % 2

            # Frame para cada botón
            button_frame = tk.Frame(parent, bg='#34495e', relief='raised', bd=2)
            button_frame.grid(row=row, column=col, padx=16, pady=16, sticky='nsew')
            button_frame.grid_propagate(False)
            button_frame.configure(width=320, height=120)

            # Botón principal (solo nombre, bien centrado y con buen contraste)
            button = tk.Button(
                button_frame,
                text=program['name'],
                command=program['command'],
                bg=program['color'],
                fg='black',
                font=('Arial', 16, 'bold'),
                relief='flat',
                cursor='hand2',
                padx=10, pady=10,
                activebackground=self.darker_color(program['color']),
                activeforeground='black',
                bd=0
            )
            button.pack(fill=tk.X, padx=16, pady=(16, 4))

            # Descripción debajo del botón
            desc_label = tk.Label(
                button_frame,
                text=program['description'],
                bg='#34495e',
                fg='#ecf0f1',
                font=('Arial', 11),
                wraplength=280,
                justify='center'
            )
            desc_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Configurar grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)

    def lighter_color(self, hex_color):
        r, g, b = self.hex_to_rgb(hex_color)
        return f'#{min(255, r+30):02x}{min(255, g+30):02x}{min(255, b+30):02x}'

    def darker_color(self, hex_color):
        r, g, b = self.hex_to_rgb(hex_color)
        return f'#{max(0, r-40):02x}{max(0, g-40):02x}{max(0, b-40):02x}'

    def hex_to_rgb(self, hex_color):
        """Convertir color hexadecimal a RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def open_program(self, key, program_path):
        # Si el programa es el generador de imágenes (en desarrollo)
        if program_path is None:
            self.open_generador_imagenes()
            return
        # Si el proceso existe, verificar si sigue activo
        process = self.program_windows.get(key)
        if process is not None:
            if process.poll() is None:
                # messagebox.showinfo("Información", f"El programa ya está abierto")
                return
            else:
                # El proceso terminó, eliminar referencia
                del self.program_windows[key]
        # Ejecutar el programa
        try:
            proc = subprocess.Popen([sys.executable, str(program_path)])
            self.program_windows[key] = proc
            # Lanzar un hilo para monitorear el proceso y limpiar referencia al cerrarse
            threading.Thread(target=self.monitor_process, args=(key, proc), daemon=True).start()
            # messagebox.showinfo("Éxito", f"Programa iniciado correctamente")
        except Exception as e:
            # messagebox.showerror("Error", f"Error al ejecutar el programa: {str(e)}")
            pass

    def monitor_process(self, key, proc):
        proc.wait()
        if key in self.program_windows and self.program_windows[key] == proc:
            del self.program_windows[key]

    def find_reconocedor_numeros(self):
        program_dir = Path("General/3-reconocedor-numeros")
        if program_dir.exists():
            python_files = list(program_dir.glob("*.py"))
            if python_files:
                return python_files[0]
        return None

    def open_generador_imagenes(self):
        """Abrir el programa Generador de Imágenes"""
        # messagebox.showinfo("Información", "El programa Generador de Imágenes está en desarrollo")
        pass

    def run(self):
        """Ejecutar la aplicación principal"""
        # Centrar la ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        # Iniciar el loop principal
        self.root.mainloop()

if __name__ == "__main__":
    app = MainDisplay()
    app.run()
