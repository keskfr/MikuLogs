# 📝 Monitor de Logs con Generación Automática y Respuestas
Este proyecto es una aplicación que monitoriza un archivo de log y muestra las líneas que contienen palabras clave definidas en un diccionario, junto con respuestas asociadas. Está construido con Flask para el backend y una interfaz web básica con HTML, CSS y JavaScript.

Incluye una funcionalidad para generar logs automáticamente. Esta característica es para demostración y ayuda a visualizar cómo el monitor procesa y responde a las entradas del log.

# 🛠 Características Principales
🔍 Monitoreo de Archivos de Log: Lee y presenta el contenido de un archivo de log (app.log por defecto).

📚 Diccionario Configurable: Utiliza un archivo de texto (diccionario.txt) para establecer palabras clave y sus respuestas correspondientes (clave|valor).

🚨 Identificación de Palabras Clave: Busca coincidencias exactas de palabras clave dentro de las líneas del log.

💬 Respuestas Asociadas: Muestra las respuestas del diccionario junto a las líneas de log donde se encontraron las palabras clave.

🤖 Generación de Logs (Demostración): Incluye una función para crear nuevas líneas de log de forma periódica.

✅ Soporte UTF-8: Compatible con caracteres especiales y emojis.

🔄 Actualización Web: La interfaz web solicita nuevos datos de log al servidor a intervalos regulares.

🧹 Limpieza de Logs: Dispone de un endpoint para vaciar el archivo de log.

✨ Diseño Sencillo: Presenta una interfaz web clara y funcional.

# ⚙️ Configuración
diccionario.txt: Define las palabras clave y sus respuestas. Formato: palabra_clave|Mensaje de respuesta. Las líneas que empiezan con # son ignoradas.

app.log: Archivo de log a monitorizar. app.py lo crea con contenido de ejemplo si no existe.

static/banner.png: Coloca tu imagen de banner aquí y asegura que el nombre en index.html coincida.

# ▶️ Uso
Instala Python 3.6+ y Flask (pip install Flask).

Ejecuta python app.py.

Abre http://127.0.0.1:5000/ en tu navegador.

La interfaz mostrará las líneas del log que contengan palabras clave del diccionario, junto con sus respuestas asociadas.

# 📚 Dependencias
Python 3.6+

Flask

Librerías estándar de Python: os, re, threading, time, random

untos para Integrar Logs Reales
Para usar logs de tu sistema o aplicación en lugar de la generación de demostración, modifica app.py en los puntos indicados por comentarios (### PUNTO DE MODIFICACIÓN PARA LOGS REALES ###). Principalmente, deberás:

Ajustar la variable LOG_FILE para que apunte a tu archivo de log real.

Modificar la función leer_logs() si tu fuente de logs no es un archivo de texto simple.

Comentar o eliminar la función generar_log_aleatorio() y la tarea log_generation_task.

Considerar si la función clear_logs() es aplicable o necesaria para tu fuente de logs real.

# 🚀 Posibles Mejoras
Integración con diversas fuentes de logs (syslog, bases de datos, etc.).

Control de la generación de logs de demostración desde la interfaz.

Funcionalidades de filtrado y búsqueda más avanzadas.

Almacenamiento del diccionario en una base de datos.

Optimización para manejar archivos de log de gran tamaño.
