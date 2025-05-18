# 📝 Monitor de Logs con Generación Automática y Respuestas
Este proyecto es un monitor de logs simple implementado con Flask (backend) y HTML/CSS/JavaScript (frontend). Permite visualizar el contenido de un archivo de log (app.log) y, basándose en un diccionario de palabras clave (diccionario.txt), asociar y mostrar respuestas predefinidas cuando se detectan esas palabras clave.

Además, la aplicación genera automáticamente líneas de log en segundo plano, simulando la actividad de un sistema real. Esta generación automática es únicamente para fines de demostración y para facilitar la visualización de cómo el monitor procesa los logs y muestra las respuestas.

# 🛠 Características clave
🔍 Monitoreo de Archivos de Log: Lee y muestra el contenido de un archivo de log especificado (app.log por defecto).

📚 Diccionario Personalizable: Utiliza un archivo de texto simple (diccionario.txt) para definir palabras clave y las respuestas asociadas (clave|valor).

🚨 Detección Inteligente: Busca palabras clave completas dentro de las líneas del log.

💬 Respuestas Contextuales: Muestra las respuestas definidas en el diccionario junto a las líneas de log donde se encontraron las palabras clave.

🤖 Generación Automática de Logs (Demostración): La aplicación genera nuevas líneas de log periódicamente.

✅ Soporte para UTF-8: Permite el uso de caracteres especiales y emojis.

🔄 Actualización Periódica: El frontend solicita nuevos logs al backend a intervalos regulares.

🧹 Limpieza de Logs: Endpoint API para vaciar el archivo de log.

✨ Interfaz Minimalista: Diseño limpio y sencillo para una fácil visualización.

# 📂 Estructura del Proyecto
tu_proyecto/
├── app.py              Script principal de la aplicación Flask (backend y generación de logs)
├── app.log             Archivo de log que será monitoreado y escrito
├── diccionario.txt     Archivo con palabras clave y respuestas
├── static/             Archivos estáticos (CSS, JS, Imágenes)
│   ├── styles.css      Estilos para la interfaz (minimalista azul)
│   ├── app.js          Lógica del frontend (carga y muestra logs)
│   └── banner.png      Imagen para el banner (reemplaza con tu imagen)
└── templates/          Archivos HTML renderizados por Flask
    └── index.html      Página principal del monitor


# ⚙️ Configuración
diccionario.txt: Edita este archivo para definir tus palabras clave y las respuestas asociadas. Cada línea debe tener el formato palabra_clave|Mensaje de respuesta. Las líneas que comienzan con # son ignoradas.

app.log: Este es el archivo que la aplicación monitoreará y en el que escribirá logs generados automáticamente (para demostración). El script app.py lo creará si no existe.

static/banner.png: Coloca la imagen que deseas usar como banner en la carpeta static/ y asegúrate de que el nombre del archivo coincida con el especificado en templates/index.html.

# ▶️ Uso
Asegúrate de tener Python 3.6+ y Flask instalados (pip install Flask).

Ejecuta el script principal: python app.py

Abre tu navegador y ve a http://127.0.0.1:5000/.

Verás la interfaz del monitor de logs, que se actualizará automáticamente con los logs generados. Las líneas que contengan palabras clave del diccionario mostrarán las respuestas asociadas.

# 📚 Dependencias
Python 3.6+

Flask

Bibliotecas estándar de Python: os, re, threading, time, random

#🚀 Potenciales Mejoras
Integración con Logs Reales: Modificar el código para leer logs de fuentes reales (archivos de sistema, bases de datos, etc.).

Control de la generación automática de logs desde la interfaz web.

Opciones de filtrado y búsqueda en la visualización de logs.

Persistencia de la configuración del diccionario a través de una base de datos.

Manejo de logs más grandes de manera eficiente.
