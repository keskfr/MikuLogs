let totalLinesLoaded = 0;


async function loadLogs() {
    try {

        const response = await fetch(`/api/logs?offset=${totalLinesLoaded}`);


        if (!response.ok) {

            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        const logsContainer = document.getElementById('logs-container');
        const loadedLogCountSpan = document.getElementById('loaded-log-count');


        if (data.logs && data.logs.length > 0) {

            data.logs.forEach(log => {

                const logEntry = document.createElement('div');
                logEntry.classList.add('log-entry'); 

                if (log.tags && log.tags.length > 0) {
                    log.tags.forEach(tag => {

                        const cssClass = tag.toLowerCase().replace(/[^a-z0-9-_]/g, '');
                        if (cssClass) { 
                             logEntry.classList.add(cssClass);
                        }
                    });
                } else {

                    logEntry.classList.add('no-tag');
                }



                const logText = document.createElement('span');
                logText.classList.add('log-text');
                logText.textContent = log.texto;
                logEntry.appendChild(logText); 


                if (log.mensajes && log.mensajes.length > 0) {
                    const logMessages = document.createElement('div');
                    logMessages.classList.add('log-messages');


                    log.mensajes.forEach(message => {
                        const logMessage = document.createElement('span');
                        logMessage.classList.add('log-message');
                        logMessage.textContent = message;
                        logMessages.appendChild(logMessage); 
                    });
                    logEntry.appendChild(logMessages);
                }


                logsContainer.appendChild(logEntry);
            });
        }



        totalLinesLoaded = data.total_lines;
        if (loadedLogCountSpan) { 
            loadedLogCountSpan.textContent = totalLinesLoaded;
        }


        if (data.logs && data.logs.length > 0) {
             logsContainer.scrollTop = logsContainer.scrollHeight;
        }


    } catch (error) {
        console.error("Error al cargar los logs:", error);

        const logsContainer = document.getElementById('logs-container');
        if (logsContainer) {
            const errorMessage = document.createElement('div');
            errorMessage.classList.add('log-entry', 'error'); 
            const errorText = document.createElement('span');
            errorText.classList.add('log-text');
            errorText.textContent = `Error al cargar logs: ${error.message}`;
            errorMessage.appendChild(errorText);
            logsContainer.appendChild(errorMessage);
        }
    }
}


async function clearLogs() {
    try {

        const response = await fetch('/api/logs/clear', {
            method: 'POST'
        });


        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data.message);


        const logsContainer = document.getElementById('logs-container');
        const loadedLogCountSpan = document.getElementById('loaded-log-count');

        if (logsContainer) {
             logsContainer.innerHTML = '';
        }
        totalLinesLoaded = 0;
        if (loadedLogCountSpan) {
            loadedLogCountSpan.textContent = totalLinesLoaded;
        }


    } catch (error) {
        console.error("Error al limpiar los logs:", error);

        const logsContainer = document.getElementById('logs-container');
         if (logsContainer) {
            const errorMessage = document.createElement('div');
            errorMessage.classList.add('log-entry', 'error');
            const errorText = document.createElement('span');
            errorText.classList.add('log-text');
            errorText.textContent = `Error al limpiar logs: ${error.message}`;
            errorMessage.appendChild(errorText);
            logsContainer.appendChild(errorMessage);
        }
    }
}


document.addEventListener('DOMContentLoaded', () => {

    loadLogs();


    setInterval(loadLogs, 3000); 


    const clearButton = document.getElementById('clear-logs-button');
    if (clearButton) { 
        clearButton.addEventListener('click', clearLogs);
    }
});
