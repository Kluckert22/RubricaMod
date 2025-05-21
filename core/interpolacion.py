import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os

def interpolar_datos(df):
    df_original = df.copy()  # Copia sin cambios

    # Interpolación lineal en copia nueva
    df_interpolado = df.copy()
    df_interpolado['Temperatura'] = df_interpolado['Temperatura'].interpolate(method='linear')

    # Crear carpeta results si no existe
    carpeta_resultados = 'results'
    os.makedirs(carpeta_resultados, exist_ok=True)

    # Graficar datos interpolados
    plt.figure(figsize=(10, 5))
    plt.plot(df_interpolado['Hora'], df_interpolado['Temperatura'], marker='o', label='Temperatura Interpolada')
    plt.xticks(rotation=45)
    plt.xlabel('Hora')
    plt.ylabel('Temperatura (°C)')
    plt.title('Temperatura interpolada')
    plt.grid(True)
    plt.legend()

    ruta_imagen = os.path.join(carpeta_resultados, 'grafica.png')
    plt.tight_layout()
    plt.savefig(ruta_imagen)
    plt.close()

    return df_original, df_interpolado, ruta_imagen
