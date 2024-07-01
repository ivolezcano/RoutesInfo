import tkinter as tk
from tkinter import filedialog
import pandas as pd
from chardet.universaldetector import UniversalDetector
import pyperclip
from PIL import Image, ImageTk

# Asocia a los vendedores con su número mayorista
asociaciones_vendedores = {
    39: [39, 88], # Vendedor 39
    57: [57, 58, 100, 41], # Vendedor 57
    65: [65, 89], # Vendedor 65
    56: [56, 26], # Vendedor 56
    36: [36, 27], # Vendedor 36
    71: [71, 29], # Vendedor 71
}

# Inicializa una lista para almacenar los DataFrames
dataframes = []

entrada = None  # Define la variable entrada en un ámbito más global

def detect_encoding(file_path):
    detector = UniversalDetector()
    with open(file_path, 'rb') as file:
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        return detector.result['encoding']

def buscar_vendedor(event=None):
    global entrada, resultado  # Usa la variable entrada y resultado definidas en el ámbito global
    if not dataframes:
        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, "Primero, cargue archivos CSV antes de buscar vendedores.")
        return
    vendedores_a_buscar = entrada.get().strip().split(',')
    vendedores_a_buscar = [int(num.strip()) for num in vendedores_a_buscar]
    
    if 'salir' in vendedores_a_buscar:
        ventana.destroy()
    else:
        resultado.delete(1.0, tk.END)  # Limpia el área de resultados
        for vendedor in vendedores_a_buscar:
            if vendedor in asociaciones_vendedores:
                vendedores_asociados = asociaciones_vendedores[vendedor]
                for vendedor_asociado in vendedores_asociados:
                    for df in dataframes:
                        filtered_df = df[df['cod_ven'] == vendedor_asociado]
                        if not filtered_df.empty:
                            for index, row in filtered_df.iterrows():
                                num_vendedor = row['cod_ven']
                                direccion = row['cli_dir']
                                # Convierte el total String a flotante para redondear.
                                totalString = row['total']
                                totalString = totalString.replace(",", ".")
                                total = float(totalString)
                                totalR = round(total, 2)
                                #
                                resultado.insert(tk.END, f'Vend: {num_vendedor}, Dir: {direccion} ${totalR}\n')
                    if resultado.get(1.0, tk.END) == "":
                        resultado.insert(tk.END, f"No se encontraron registros para el vendedor con número {vendedor_asociado}")
            else:
                for df in dataframes:
                    filtered_df = df[df['cod_ven'] == vendedor]
                    if not filtered_df.empty:
                        for index, row in filtered_df.iterrows():
                            num_vendedor = row['cod_ven']
                            direccion = row['cli_dir']
                            # Convierte el total String a flotante para redondear.
                            totalString = row['total']
                            totalString = totalString.replace(",", ".")
                            total = float(totalString)
                            totalR = round(total, 2)
                            #
                            resultado.insert(tk.END, f'Vend: {num_vendedor}, Dir: {direccion} ${totalR}\n')
                if resultado.get(1.0, tk.END) == "":
                    resultado.insert(tk.END, f"No se encontraron registros para el vendedor con número {vendedor}")

def ordenar_y_listar_vendedores():
    global entrada, resultado  # Usa la variable entrada y resultado definidas en el ámbito global

    def copiar_resultado():
        resultado_text = resultado.get(1.0, tk.END)
        pyperclip.copy(resultado_text)  # Copia el resultado al portapapeles

    def seleccionar_archivos():
        archivos = filedialog.askopenfilenames(filetypes=[("Archivos CSV", "*.csv")])
        for archivo in archivos:
            # Cambia el delimitador a ';' al leer el archivo CSV
            encoding = detect_encoding(archivo)
            df = pd.read_csv(archivo, sep=';', encoding=encoding)
            dataframes.append(df)
        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, f"✔️ {len(dataframes)} archivo(s) cargado(s) exitosamente. ✔️\n")
        resultado.insert(tk.END, "Ingrese el número de vendedor que desea buscar (o 'salir' para volver al menú principal) ")

    ventana = tk.Tk()
    ventana.title("Ordenar y Listar Vendedores")

    # Crear un Frame para centrar los elementos
    frame = tk.Frame(ventana)
    frame.pack(expand=True, fill=tk.BOTH)

    # Abre y redimensiona el logotipo
    logo_image = Image.open("logo.png")  # Reemplaza "logo.png" con la ruta de tu imagen
    logo_image.thumbnail((100, 100))  # Ajusta el tamaño del logotipo
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(frame, image=logo_photo)
    logo_label.pack()

    cargar_archivos_button = tk.Button(frame, text="Cargar Archivos", command=seleccionar_archivos)
    cargar_archivos_button.pack(pady=10)

    entrada = tk.Entry(frame)
    entrada.pack()

    buscar_button = tk.Button(frame, text="Buscar", command=buscar_vendedor)
    buscar_button.pack(pady=10)

    copiar_button = tk.Button(frame, text="Copiar al Portapapeles", command=copiar_resultado)
    copiar_button.pack(pady=10)

    # Asocia la función 'buscar_vendedor' al evento 'Enter' en la entrada (Entry)
    entrada.bind('<Return>', buscar_vendedor)

    resultado = tk.Text(frame, height=10, width=40)
    resultado.pack()

    ventana.mainloop()

ordenar_y_listar_vendedores()