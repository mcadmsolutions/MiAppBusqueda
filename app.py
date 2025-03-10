from flask import Flask, render_template, request
import gspread
from google.oauth2.service_account import Credentials
import os
import json

app = Flask(__name__)

# Credenciales de Google Sheets desde la variable de entorno
creds_json = os.getenv("GOOGLE_CREDENTIALS")  # Obtener el JSON como una cadena de la variable de entorno
creds_dict = json.loads(creds_json)  # Convertir la cadena a un diccionario
scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(creds)

# Abre la hoja de cálculo con el nombre correcto
spreadsheet = client.open("Mapa Picking Json")
sheet = spreadsheet.sheet1  # Primera hoja

# Página principal (búsqueda)
@app.route('/', methods=['GET'])
def index():
    query = request.args.get('query', '').lower()  # Obtener la búsqueda y convertirla a minúsculas
    data = []
    message = None  # Mensaje por defecto vacío

    if query:
        # Filtrar los datos de acuerdo a la búsqueda
        all_data = sheet.get_all_records()  # Obtener todos los registros de la hoja
        for row in all_data:
            # Convertimos los valores a cadena antes de hacer la comparación
            modelo = str(row['MODELO']).lower()
            nombre_corto = str(row['NOMBRE CORTO']).lower()

            # Verificamos si la consulta aparece en el modelo o el nombre corto
            if query in modelo or query in nombre_corto:
                data.append(row)

        if not data:
            message = f"No se encontraron resultados para '{query}'."  # Mostrar el mensaje solo si no hay resultados

    return render_template('index.html', data=data, query=query, message=message)

# Página de la tabla
@app.route('/tabla')
def tabla():
    # Leer todos los datos de la hoja, excepto los encabezados
    data = sheet.get_all_records()  # Esto obtiene todos los datos de la hoja sin los encabezados

    # Verifica si estamos obteniendo datos
    # print("Datos obtenidos desde Google Sheets:")
    # print(data)  # Esto imprimirá los datos en la consola

    return render_template('tabla.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
