import os
import socket

def obtener_nombre_equipo():
    try:
        nombre_equipo = socket.gethostname()
        return nombre_equipo
    except Exception as e:
        print("Error al obtener el nombre del equipo:", e)
        return None

def buscar_reemplazar(ruta, palabra_buscar, palabra_reemplazar):
    script_actual = os.path.abspath(__file__)
    for carpeta_actual, _, archivos in os.walk(ruta):
        for archivo in archivos:
            ruta_completa = os.path.join(carpeta_actual, archivo)
            if os.path.abspath(ruta_completa) != script_actual:  # Evitar reemplazar en el propio script
                if ruta_completa.upper().endswith(('.CONFIG', '.PY')):
                    try:
                        with open(ruta_completa, 'r') as f:
                            contenido = f.read()
                        if palabra_buscar in contenido:
                            contenido_modificado = contenido.replace(palabra_buscar, palabra_reemplazar)
                            with open(ruta_completa, 'w') as f:
                                f.write(contenido_modificado)
                            print(f"Se reemplazó '{palabra_buscar}' por '{palabra_reemplazar}' en {ruta_completa}")
                    except Exception as e:
                        #print(f"Error al procesar {ruta_completa}: {e}")
                        pass

# Ruta de la carpeta a buscar
ruta_carpeta = 'C:\\BuenosAires\\'

# Palabra a buscar y reemplazar (PC del profe en el laboratorio es AOAWSB03LC1100, el Notebook del profe es z80\\SQLEXPRESS)
palabra_buscar = 'AOAWSB03LC1100'
palabra_reemplazar = obtener_nombre_equipo()
buscar_reemplazar(ruta_carpeta, palabra_buscar, palabra_reemplazar)
