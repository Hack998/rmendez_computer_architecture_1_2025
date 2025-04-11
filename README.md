Interpolador bilineal para escalar imagen 400x400 pixeles
=========================================================

##  Obteniendo el codigo fuente

	$ git clone https://github.com/Hack998/rmendez_computer_architecture_1_2025.git

##  Pre-requisitos

Se necesitan varios paquetes para construir el programa. Tomar en consideración que el programa fue desarrollado y probado en Ubuntu 22.04 (LTS)

En Ubuntu,

	$ sudo apt-get install python3 python3-pip nasm

Una vez descargado todo, es necesario descargar unos paquetes de Python

	$ pip3 install numpy pillow

### Uso de los paquetes

- Python3, Se usa para manejar la interfaz
- Python3-pip, Se usa para descargar los paquetes necesarios de Python
- Numpy, Se usa para el manejo de las matrices internas
- Pillow, Se usa para el manejo de imágenes
- nasm, Se usa para compilar el ensamblador

### Extra

	$ sudo apt-get install gdb

Este paquete se usa para debuggear el código de ensamblador


##  Uso

- Se carga una imagen de 400x400 pixeles, esta puede ser a color o no
- Se escribe en el campo de texto el cuadrante que se desea aplicar la interpolación bilineal, tiene que ser entre 1 y 16
- Click en el botón de seleccionar, para poder visualizar el cuadrante elegido
- Click en el botón de Interpolación bilineal, para iniciar el proceso
