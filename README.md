# Proyecto de Interpolación de Temperaturas

## Cómo usar

1. Clonar o copiar el proyecto.
2. Ejecutar `setup.bat` (Windows) o `setup.sh` (Linux/macOS) para crear entorno e instalar dependencias.
3. Activar entorno virtual:
    - Windows: `call venv\Scripts\activate`
    - Linux/macOS: `source venv/bin/activate`
4. Ejecutar la app:
    ```bash
    python app.py
    ```
5. Abrir navegador en [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### Estructura del proyecto

Crea un archivo setup.bat en la raíz del proyecto con este contenido:
@echo off
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo Entorno listo y dependencias instaladas.
echo Para iniciar la app ejecuta: call venv\Scripts\activate && python app.py
pause

