from flask import Flask, render_template, request, send_file, Response
import os
import pandas as pd
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
UPLOAD_FOLDER = "data"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def interpolar_csv(file_path):
    df = pd.read_csv(file_path)
    df['Temperatura'] = pd.to_numeric(df['Temperatura'], errors='coerce')
    df_interp = df.copy()
    df_interp['Temperatura'] = df['Temperatura'].interpolate(method='linear')

    salida_path = os.path.join("data", "interpolado.csv")
    df_interp.to_csv(salida_path, index=False)

    df_json = df.where(pd.notnull(df), None)
    df_interp_json = df_interp.where(pd.notnull(df_interp), None)

    return df_json.to_dict(orient="records"), df_interp_json.to_dict(orient="records")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/procesar", methods=["POST"])
def procesar():
    if "archivo" not in request.files:
        return "No se envió archivo", 400
    archivo = request.files["archivo"]
    if archivo.filename == "":
        return "Nombre de archivo vacío", 400
    filename = secure_filename(archivo.filename)
    ruta = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    archivo.save(ruta)

    original, interpolado = interpolar_csv(ruta)

    respuesta = json.dumps(
        {"original": original, "interpolado": interpolado},
        default=lambda x: None
    )

    return Response(respuesta, content_type="application/json")

@app.route("/descargar")
def descargar():
    return send_file("data/interpolado.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
