from flask import Flask, jsonify, render_template, request
import os
import re
import threading
import time
import random

app = Flask(__name__)

# Define los nombres de los archivos de log y diccionario
# ### PUNTO DE MODIFICACIÓN PARA LOGS REALES ###
# Si usas logs reales, esta variable DEBE apuntar a la ruta completa o relativa
# del archivo de log que deseas monitorear en tu sistema.
LOG_FILE = "app.log"
DICCIONARIO_FILE = "diccionario.txt"

# Intervalo para generar nuevos logs en segundos (solo para demostración)
# ### PUNTO DE MODIFICACIÓN PARA LOGS REALES ###
# Este intervalo y la tarea de generación automática (log_generation_task)
# deben eliminarse o deshabilitarse si estás usando logs reales.
LOG_GENERATION_INTERVAL = 5

def cargar_diccionario():
    """
    Carga el diccionario desde el archivo DICCIONARIO_FILE.
    El formato esperado es: clave|valor por línea.
    Las líneas que comienzan con # son ignoradas.
    """
    dic = {}
    try:
        with open(DICCIONARIO_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|', 1)
                    if len(parts) == 2:
                        key = parts[0].strip().lower()
                        val = parts[1].strip()
                        dic[key] = val
    except FileNotFoundError:
        print(f"Advertencia: El archivo de diccionario '{DICCIONARIO_FILE}' no fue encontrado.")
    except Exception as e:
        print(f"Error cargando diccionario: {e}")
    return dic

def leer_logs():
    """
    Lee las líneas del archivo de log especificado por LOG_FILE.
    Retorna una lista de strings, donde cada string es una línea del log.
    Retorna una lista vacía si el archivo no existe o hay un error de lectura.

    ### PUNTO DE MODIFICACIÓN PARA LOGS REALES ###
    Si tu fuente de logs no es un archivo de texto simple (ej: logs de sistema
    gestionados por syslog, journald, una base de datos centralizada, etc.),
    DEBERÁS modificar esta función completamente para interactuar con esa
    fuente de logs y obtener las líneas más recientes. La forma de hacerlo
    dependerá de la fuente específica.
    """
    if not os.path.exists(LOG_FILE):
        return []
    try:
        # Abre el archivo de log en modo lectura. 'r' para leer, 'a+' para leer y añadir.
        # Si el archivo puede ser escrito por otra aplicación, 'a+' podría ser útil.
        # Asegúrate de tener permisos de lectura sobre el archivo de log real.
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # Filtra líneas vacías y elimina espacios al inicio/fin
        return [line.strip() for line in lines if line.strip()]
    except Exception as e:
        print(f"Error leyendo logs: {e}")
        return []

def generar_log_aleatorio():
    """
    Genera una línea de log aleatoria y la escribe en LOG_FILE.
    Esta función es solo para demostración.

    ### PUNTO DE MODIFICACIÓN PARA LOGS REALES ###
    Esta función DEBE eliminarse o deshabilitarse si estás usando logs reales.
    No querrás que tu aplicación de monitoreo escriba logs de demostración
    en tu archivo de log real.
    """
    diccionario = cargar_diccionario()
    claves = list(diccionario.keys())

    palabras_comunes = ["proceso", "sistema", "usuario", "tarea", "archivo", "red", "base de datos", "servicio"]
    tipos_mensaje = ["INFO", "DEBUG", "WARN", "ERROR"]

    mensaje_parts = []

    if claves and random.random() < 0.5:
        clave_aleatoria = random.choice(claves)
        mensaje_parts.append(clave_aleatoria)

    num_palabras_comunes = random.randint(1, 3)
    mensaje_parts.extend(random.sample(palabras_comunes, min(num_palabras_comunes, len(palabras_comunes))))

    tipo = random.choice(tipos_mensaje)
    mensaje_parts.insert(0, f"[{tipo}]")

    random.shuffle(mensaje_parts)
    log_linea = " ".join(mensaje_parts) + "."

    try:
        # Abre el archivo de log en modo añadir ('a') para no sobrescribir logs existentes
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_linea + "\n")
        # print(f"Log generado: {log_linea}") # Opcional: imprimir en consola del servidor
    except Exception as e:
        print(f"Error escribiendo en el archivo de log: {e}")


def log_generation_task():
    """
    Tarea en segundo plano para generar logs periódicamente.
    Esta tarea es solo para demostración.

    ### PUNTO DE MODIFICACIÓN PARA LOGS REALES ###
    Esta tarea DEBE eliminarse o deshabilitarse si estás usando logs reales.
    La generación de logs reales es responsabilidad del sistema o aplicación
    que estás monitoreando, no de esta aplicación de monitoreo.
    """
    while True:
        generar_log_aleatorio()
        time.sleep(LOG_GENERATION_INTERVAL)

@app.route('/')
def index():
    """
    Renderiza la página principal (index.html).
    Este archivo debe estar en la carpeta 'templates'.
    """
    return render_template('index.html')

@app.route('/api/logs')
def api_logs():
    """
    Endpoint API para obtener los logs.
    Acepta un parámetro 'offset' para paginación.
    Busca palabras clave del diccionario en los logs y asocia las respuestas.

    ### PUNTO DE MODIFICACIÓN PARA LOGS REALES ###
    La lógica de procesamiento de logs y búsqueda de palabras clave
    dentro de esta función es generalmente aplicable a logs reales.
    La parte que interactúa con `leer_logs()` es la que se adapta
    a la fuente de logs. Si `leer_logs()` ya te da las líneas correctas,
    esta función no necesitaría grandes cambios.
    """
    offset_str = request.args.get('offset', default='0')
    try:
        offset = int(offset_str)
        if offset < 0:
            offset = 0
    except ValueError:
        offset = 0
    except Exception as e:
        print(f"Error procesando el offset: {e}")
        offset = 0

    logs = leer_logs() # Llama a la función que lee los logs (modificable para logs reales)
    diccionario = cargar_diccionario()

    # Obtiene los logs a partir del offset especificado
    logs_nuevos = logs[offset:] if offset < len(logs) else []

    resultado = []
    # Itera sobre cada línea de log nueva para procesarla
    for line in logs_nuevos:
        line_lower = line.lower()
        claves_encontradas = []
        mensajes_asociados = []

        # Itera sobre cada par clave-valor del diccionario para buscar coincidencias
        for key, msg in diccionario.items():
            if re.search(r'\b' + re.escape(key) + r'\b', line_lower):
                claves_encontradas.append(key)
                mensajes_asociados.append(msg)

        # ### CAMBIO AÑADIDO: FILTRAR LOGS SIN PALABRAS CLAVE ###
        # Solo añade la entrada al resultado si se encontraron palabras clave en la línea
        if claves_encontradas:
            resultado.append({
                "texto": line,
                "tags": claves_encontradas,
                "mensajes": mensajes_asociados
            })

    # Retorna el resultado como un objeto JSON, incluyendo el total de líneas de log
    # Nota: total_lines sigue reflejando el total del archivo, no solo los filtrados
    return jsonify({
        "logs": resultado,
        "total_lines": len(logs)
    })

@app.route('/api/logs/clear', methods=['POST'])
def clear_logs():
    """
    Endpoint API para limpiar (vaciar) el archivo de logs.
    Solo accesible mediante el método POST.

    ### PUNTO DE MODIFICACIÓN PARA LOGS REALES ###
    Si lees logs de una fuente que no es un archivo simple (ej: syslog, journald),
    esta función podría no ser relevante o necesitar una implementación diferente
    para "limpiar" o archivar logs en esa fuente. Si solo lees un archivo,
    esta función puede seguir siendo útil para resetearlo.
    """
    try:
        # Abre el archivo en modo escritura ('w') para vaciarlo
        # Asegúrate de tener permisos de escritura sobre el archivo de log real si lo limpias.
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.truncate(0)
        return jsonify({"status": "ok", "message": "Logs limpiados exitosamente"})
    except Exception as e:
        print(f"Error limpiando logs: {e}")
        return jsonify({"status": "error", "message": f"Error limpiando logs: {e}"}), 500

if __name__ == '__main__':
    # Este bloque se ejecuta solo si el script se corre directamente

    # Crea el archivo de log si no existe con contenido de ejemplo
    # ### PUNTO DE MODIFICACIÓN PARA LOGS REALES ###
    # Si usas logs reales, es posible que no necesites crear este archivo aquí,
    # ya que tu sistema o aplicación ya lo gestionará. Puedes comentar o eliminar
    # este bloque `if not os.path.exists(LOG_FILE):`.
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', encoding='utf-8') as f_log:
            f_log.write("Inicio del sistema.\n")

    # Crea el archivo del diccionario si no existe con contenido de ejemplo
    # Este archivo es necesario para el funcionamiento del monitor, independientemente
    # de si usas logs de demostración o reales.
    if not os.path.exists(DICCIONARIO_FILE):
        with open(DICCIONARIO_FILE, 'w', encoding='utf-8') as f_dict:
            f_dict.write("# Este es un comentario, será ignorado\n")
            f_dict.write("error|Se ha detectado un error crítico. Revisar inmediatamente.\n")
            f_dict.write("advertencia|Hay una advertencia en el sistema.\n")
            f_dict.write("ejemplo|Este es un mensaje de ejemplo del diccionario.\n")
            f_dict.write("sistema|Mensaje relacionado con el sistema.\n")
            f_dict.write("proceso|Información sobre un proceso en ejecución.\n")


    # Inicia el hilo en segundo plano para la generación automática de logs (solo para demostración)
    # ### PUNTO DE MODIFICACIÓN PARA LOGS REALES ###
    # COMENTA o ELIMINA completamente estas dos líneas si no quieres generar logs de demostración.
    # Si tu fuente de logs real es un archivo, la función `leer_logs` ya lo leerá.
    log_thread = threading.Thread(target=log_generation_task, daemon=True)
    log_thread.start()

    # Ejecuta la aplicación Flask
    # debug=True es útil durante el desarrollo, pero considera desactivarlo en producción.
    app.run(debug=True)
