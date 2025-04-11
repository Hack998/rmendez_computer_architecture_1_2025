import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import subprocess
import os

class ImageQuadrantApp:
    def __init__(self, master):
        self.master = master
        master.title("Interpolador Bilineal para escalar cuadrante")

        self.original_image_path = None
        self.original_image = None
        self.tk_original_image = None
        self.selected_quadrant = None
        self.selected_quadrant_data = None

        self.selected_quadrant_image = None
        self.tk_selected_quadrant_image = None

        self.result_image = None
        self.tk_result_image = None

        # Marco para cargar y visualizar la imagen original
        self.frame_original = tk.LabelFrame(master, text="Imagen Original (400x400)")
        self.frame_original.grid(row=0, column=0, padx=10, pady=10)

        self.load_button = tk.Button(self.frame_original, text="Cargar Imagen", command=self.load_image)
        self.load_button.pack(pady=5)

        self.original_image_label = tk.Label(self.frame_original)
        self.original_image_label.pack()

        # Marco para seleccionar el cuadrante
        self.frame_quadrant = tk.LabelFrame(master, text="Seleccionar Cuadrante")
        self.frame_quadrant.grid(row=0, column=1, padx=10, pady=10)

        self.quadrant_label = tk.Label(self.frame_quadrant, text="Cuadrante (1-16):")
        self.quadrant_label.pack(pady=5)

        self.quadrant_entry = tk.Entry(self.frame_quadrant)
        self.quadrant_entry.pack(pady=5)

        self.select_button = tk.Button(self.frame_quadrant, text="Seleccionar", command=self.display_quadrant)
        self.select_button.pack(pady=5)

        self.selected_quadrant_label = tk.Label(self.frame_quadrant, text="Cuadrante Seleccionado (100x100):")
        self.selected_quadrant_label.pack(pady=5)
        self.quadrant_image_label = tk.Label(self.frame_quadrant)
        self.quadrant_image_label.pack()

        # Marco para el botón de interpolacion
        self.frame_interpolation_button = tk.Frame(master)
        self.frame_interpolation_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.interpolation_button = tk.Button(self.frame_interpolation_button, text="Interpolacion Bilineal", command=self.start_interpolation)
        self.interpolation_button.pack()

        # Marco para visualizar la imagen resultante
        self.frame_result_image = tk.LabelFrame(master, text="Resultado (298x298)")
        self.frame_result_image.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.result_image_label = tk.Label(self.frame_result_image)
        self.result_image_label.pack()

    def load_image(self):
        """
        Funcion para cargar la imagen original y dibujarla en la interfaz
        """
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg")])
        if file_path:
            try:
                self.original_image = Image.open(file_path).resize((400, 400))
                self.tk_original_image = ImageTk.PhotoImage(self.original_image)
                self.original_image_label.config(image=self.tk_original_image)
                self.original_image_label.image = self.tk_original_image 
                self.original_image_path = file_path
            except Exception as e:
                tk.messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

    def display_quadrant(self):
        """
        Calcula cual es el cuadrante elegido y lo dibuja
        """
        if self.original_image:
            try:
                quadrant_number = int(self.quadrant_entry.get())
                if 1 <= quadrant_number <= 16:
                    self.selected_quadrant = quadrant_number
                    width, height = self.original_image.size
                    quadrant_size = width // 4

                    row = (quadrant_number - 1) // 4
                    col = (quadrant_number - 1) % 4

                    left = col * quadrant_size
                    top = row * quadrant_size
                    right = (col + 1) * quadrant_size
                    bottom = (row + 1) * quadrant_size

                    quadrant = self.original_image.crop((left, top, right, bottom)).resize((100, 100))
                    self.selected_quadrant_data = np.array(quadrant.convert('L')) # La informacion que se guarda es solo al escala de grices
                    self.selected_quadrant_image = ImageTk.PhotoImage(quadrant)
                    self.quadrant_image_label.config(image=self.selected_quadrant_image)
                    self.quadrant_image_label.image = self.selected_quadrant_image
                else:
                    self.selected_quadrant = None
                    tk.messagebox.showerror("Error", "El número de cuadrante debe estar entre 1 y 16.")
            except ValueError:
                self.selected_quadrant = None
                tk.messagebox.showerror("Error", "Por favor, introduce un número entero para el cuadrante.")
        else:
            self.selected_quadrant = None
            tk.messagebox.showinfo("Información", "Por favor, carga una imagen primero.")

    def start_interpolation(self):
        """
        Inicia toda la logica de la interpolacion bilineal
        """
        if self.selected_quadrant is not None:
            self.save()
            self.execute_assembly()
            self.read()
        else:
            tk.messagebox.showinfo("Información", "Por favor, selecciona un cuadrante primero.")

    def save(self):
        """
        Funcion encargada de guardar toda la informacion del cuadrante elegido
        """
        file_path = "cuadrante.img"
        n_filas, n_cols = self.selected_quadrant_data.shape
        try:
            with open(file_path, "wb") as f:
                for i in range(0, n_filas - 1):
                    for j in range(0, n_cols - 1):
                        subcuadro = self.selected_quadrant_data[i:i+2, j:j+2]
                        for fila in subcuadro:
                            for valor in fila:
                                # Lo pasa a Hexadecimal
                                byte_value = int(valor) & 0xFF
                                f.write(byte_value.to_bytes(1, 'big'))
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al guardar el archivo: {e}")

    def execute_assembly(self):
        """
        Ejecuta el codigo de ensamblador
        """
        ruta_ejecutable = os.path.join(".", "interpolation")
        try:
            subprocess.run([ruta_ejecutable])
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo ejecutable en la ruta: {ruta_ejecutable}")
        except Exception as e:
            print(f"Ocurrió un error al ejecutar '{ruta_ejecutable}': {e}")

    def hex_to_dec(hex_str):
        """
        Funcion para cambiar la matriz {hex_str} de hexadecimal a decimal

        Args:
            hex_str: Matriz hexadecimal.

        Returns:
            Matriz decimal
        """
        try:
            return int(hex_str, 16)
        except ValueError:
            return None

    def read(self):
        """
        Lee la salida del ensamblador y dibuja la imagen
        """
        # Es necesario el dtype='<U2' para que la matriz tengo el espacio guardar los 2 bytes que se leen por pixel
        matriz = np.full((298, 298), "00", dtype='<U2')
        file_path = "r.img"
        try:
            with open(file_path, "rb")as f:
                contenido = f.read()
                hex_leido = [f"{byte:02x}" for byte in contenido]
        except:
            print("No se encontro la salida del ensamblador")

        # Reconstruye la imagen
        contador = 0
        for x_big in range (0, 99):
            for y_big in range(0, 99):
                for x in range(0, 4):
                    for y in range(0, 4):
                        matriz[x+x_big*3][y+y_big*3] = hex_leido[contador]
                        contador += 1

        # Vectoriza la funcion hex_to_dec para que funcione en matrices
        hex_to_dec_vectorized = np.vectorize(ImageQuadrantApp.hex_to_dec)
        matriz_decimal = hex_to_dec_vectorized(matriz)

        matriz_uint8 = matriz_decimal.astype(np.uint8)
        new_image = Image.fromarray(matriz_uint8)
        new_image.save("Resultado.jpg")

        self.result_image = new_image
        self.tk_result_image = ImageTk.PhotoImage(self.result_image)
        self.result_image_label.config(image=self.tk_result_image)
        self.result_image_label.image = self.tk_result_image

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageQuadrantApp(root)
    root.mainloop()