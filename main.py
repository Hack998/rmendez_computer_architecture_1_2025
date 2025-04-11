import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import numpy as np

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

        self.other_image = None
        self.tk_other_image = None

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

        # Marco para el botón de conteo
        self.frame_counter_button = tk.Frame(master)
        self.frame_counter_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.counter_button = tk.Button(self.frame_counter_button, text="Interpolacion Bilineal", command=self.start_counter)
        self.counter_button.pack()

        # Marco para visualizar otra imagen
        self.frame_other_image = tk.LabelFrame(master, text="Resultado (298x298)")
        self.frame_other_image.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.other_image_label = tk.Label(self.frame_other_image)
        self.other_image_label.pack()

    def load_image(self):
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
                    self.selected_quadrant_data = np.array(quadrant.convert('L'))
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

    def start_counter(self):
        if self.selected_quadrant is not None:
            self.save()
            # Subprocess
            self.read()
        else:
            tk.messagebox.showinfo("Información", "Por favor, selecciona un cuadrante primero.")

    def save(self):
        file_path = "cuadrante.img"
        n_filas, n_cols = self.selected_quadrant_data.shape
        subcuadros_guardados = 0
        try:
            with open(file_path, "wb") as f:  # Abrir en modo binario ("wb")
                for i in range(0, n_filas - 1):
                    for j in range(0, n_cols - 1):
                        subcuadro = self.selected_quadrant_data[i:i+2, j:j+2]
                        for fila in subcuadro:
                            for valor in fila:
                                byte_value = int(valor) & 0xFF
                                f.write(byte_value.to_bytes(1, 'big'))
                        subcuadros_guardados += 1
                print(f"Se han guardado {subcuadros_guardados} subcuadros")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al guardar el archivo: {e}")

    def hex_to_dec(hex_str):
        try:
            return int(hex_str, 16)
        except ValueError:
            return None

        

    def read(self):

        matriz = np.full((298, 298), "00", dtype='<U2')

        file_path = "r.img"
        try:
            with open(file_path, "rb")as f:
                contenido = f.read()
                hex_leido = [f"{byte:02x}" for byte in contenido]
        except:
            print("No se encontro")

        contador = 0

        for x_big in range (0, 1): # Esta 99
            for y_big in range(0, 99): # Esta 99
                for x in range(0, 4):
                    for y in range(0, 4):
                        matriz[x+x_big*3][y+y_big*3] = hex_leido[contador]
                        contador += 1
                contador = 0

        matriz[4][4] = "FF"
        #print(matriz[0:5, -10:])

        hex_to_dec_vectorized = np.vectorize(ImageQuadrantApp.hex_to_dec)
        matriz_decimal = hex_to_dec_vectorized(matriz)

        matriz_uint8 = matriz_decimal.astype(np.uint8)
        new_image = Image.fromarray(matriz_uint8)

        self.other_image = new_image
        self.tk_other_image = ImageTk.PhotoImage(self.other_image)
        self.other_image_label.config(image=self.tk_other_image)
        self.other_image_label.image = self.tk_other_image

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageQuadrantApp(root)
    root.mainloop()