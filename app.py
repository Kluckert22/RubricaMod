from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Para que no intente abrir ventanas gráficas
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

def interpolar_datos(df):
    df_original = df.copy()  # copia sin cambios

    # Interpolar la columna Temperatura (lineal)
    df_interpolado = df.copy()
    df_interpolado['Temperatura'] = df_interpolado['Temperatura'].interpolate(method='linear')

    # Crear gráfica
    plt.figure(figsize=(10, 5))
    plt.plot(df_interpolado['Hora'], df_interpolado['Temperatura'], marker='o', label='Temperatura Interpolada')
    plt.xticks(rotation=45)
    plt.xlabel('Hora')
    plt.ylabel('Temperatura (°C)')
    plt.title('Temperatura interpolada')
    plt.grid(True)
    plt.legend()

    ruta_imagen = os.path.join(app.config['RESULTS_FOLDER'], 'grafica.png')
    plt.tight_layout()
    plt.savefig(ruta_imagen)
    plt.close()

    return df_original, df_interpolado, ruta_imagen

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    archivo = request.files.get('archivo')
    if not archivo:
        return "No se subió ningún archivo", 400

    ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], archivo.filename)
    archivo.save(ruta_archivo)

    df = pd.read_csv(ruta_archivo)

    df_original, df_interpolado, ruta_grafica = interpolar_datos(df)

    # Guardar CSVs en results/
    df_original.to_csv(os.path.join(app.config['RESULTS_FOLDER'], 'datos_originales.csv'), index=False)
    df_interpolado.to_csv(os.path.join(app.config['RESULTS_FOLDER'], 'datos_interpolados.csv'), index=False)

    tabla_original = df_original.to_html(classes='data-table', index=False)
    tabla_interpolado = df_interpolado.to_html(classes='data-table', index=False)

    nombre_imagen = os.path.basename(ruta_grafica)

    return render_template('resultado.html',
                           tabla_original=tabla_original,
                           tabla_interpolado=tabla_interpolado,
                           nombre_imagen=nombre_imagen)

@app.route('/results/<path:filename>')
def mostrar_resultado(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
