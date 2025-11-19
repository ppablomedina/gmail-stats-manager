from gcp.utils import upload_files_to_gcp, get_missing_files
from gcp.paths import identify_attachments
from mail      import get_new_mail, notify_warning
from flask import Flask, request
import pandas  as pd


def entry_point(request):
    """ 
    Este programa se ejecutará cada día, su función es:

    1. Buscar correos nuevos en la bandeja de entrada de los remitentes permitidos.
    2. Descargar los archivos adjuntos de esos correos.
    3. Identificar esos archivos con su ruta de GCS.
    4. Subir los archivos a GCS.
    
    5. El día 10 de cada mes, comprobar si faltan archivos en los buckets de GCS.
    6. Si faltan, enviar un correo de aviso a los responsables de los ficheros faltantes.
    
    """

    attachments = get_new_mail()
    if attachments: 
        attachments = identify_attachments(attachments)
        upload_files_to_gcp(attachments)

    send_email("pabloms.lp@gmail.com", "Funciona", "hola")

    if pd.Timestamp.now().day == 10: 
        missing_files = get_missing_files()
        if missing_files: notify_warning(missing_files)

    return "ETL ejecutado correctamente\n", 200

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def run():
    return entry_point(request)
