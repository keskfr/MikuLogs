from flask import Flask, jsonify, render_template, request
import os
import re
import threading
import time
import random

app = Flask(__name__)

LOG_FILE = "app.log"
DICCIONARIO_FILE = "diccionario.txt"
# Intervalo para generar nuevos logs en segundos
LOG_GENERATION_INTERVAL = 5

def cargar_diccionario():
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
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip()]
    except Exception as e:
        print(f"Error leyendo logs: {e}")
        return []

def generar_log_aleatorio():
    """Genera una línea de log aleatoria, incluyendo a veces palabras del diccionario."""
    diccionario = cargar_diccionario() # Carga el diccionario para usar sus claves
    claves = list(diccionario.keys())

    palabras_comunes = ["proceso", "sistema", "usuario", "tarea", "archivo", "red", "base de datos", "servicio"]
    tipos_mensaje = ["INFO", "DEBUG", "WARN", "ERROR"]

    mensaje_parts = []

    # Incluir una palabra del diccionario aleatoriamente
    if claves and random.random() < 0.5: # 50% de probabilidad de incluir una palabra clave
        clave_aleatoria = random.choice(claves)
        mensaje_parts.append(clave_aleatoria)

    # Añadir algunas palabras comunes aleatorias
    num_palabras_comunes = random.randint(1, 3)
    mensaje_parts.extend(random.sample(palabras_comunes, min(num_palabras_comunes, len(palabras_comunes))))

    # Añadir un tipo de mensaje aleatorio
    tipo = random.choice(tipos_mensaje)
    mensaje_parts.insert(0, f"[{tipo}]") # Añade el tipo al principio

    # Mezclar las partes y unirlas en una línea
    random.shuffle(mensaje_parts)
    log_linea = " ".join(mensaje_parts) + "."

    # Escribir la línea en el archivo de log
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_linea + "\n")
        print(f"Log generado: {log_linea}") # Opcional: imprimir en consola del servidor
    except Exception as e:
        print(f"Error escribiendo en el archivo de log: {e}")


def log_generation_task():
    """Tarea en segundo plano para generar logs periódicamente."""
    while True:
        generar_log_aleatorio()
        time.sleep(LOG_GENERATION_INTERVAL)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/logs')
def api_logs():
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

    logs = leer_logs()
    diccionario = cargar_diccionario()

    logs_nuevos = logs[offset:] if offset < len(logs) else []

    resultado = []
    for line in logs_nuevos:
        line_lower = line.lower()
        claves_encontradas = []
        mensajes_asociados = []
        for key, msg in diccionario.items():
            if re.search(r'\b' + re.escape(key) + r'\b', line_lower):
                claves_encontradas.append(key)
                mensajes_asociados.append(msg)

        resultado.append({
            "texto": line,
            "tags": claves_encontradas,
            "mensajes": mensajes_asociados
        })

    return jsonify({
        "logs": resultado,
        "total_lines": len(logs)
    })

@app.route('/api/logs/clear', methods=['POST'])
def clear_logs():
    try:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.truncate(0)
        return jsonify({"status": "ok", "message": "Logs limpiados exitosamente"})
    except Exception as e:
        print(f"Error limpiando logs: {e}")
        return jsonify({"status": "error", "message": f"Error limpiando logs: {e}"}), 500

if __name__ == '__main__':
    # Crea los archivos de log y diccionario si no existen con contenido de ejemplo
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', encoding='utf-8') as f_log:
            f_log.write("Inicio del sistema.\n")

    if not os.path.exists(DICCIONARIO_FILE):
        with open(DICCIONARIO_FILE, 'w', encoding='utf-8') as f_dict:
            f_dict.write("# Este es un comentario, será ignorado\n")
            f_dict.write("error|Se ha detectado un error crítico. Revisar inmediatamente.\n")
            f_dict.write("advertencia|Hay una advertencia en el sistema.\n")
            f_dict.write("ejemplo|Este es un mensaje de ejemplo del diccionario.\n")
            f_dict.write("sistema|Mensaje relacionado con el sistema.\n")
            f_dict.write("proceso|Información sobre un proceso en ejecución.\n")


    # Inicia el hilo en segundo plano para la generación automática de logs
    log_thread = threading.Thread(target=log_generation_task, daemon=True)
    log_thread.start()

    # Ejecuta la aplicación Flask
    app.run(debug=True)