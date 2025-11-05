from gcp.paths    import BUCKET_NAME, TABLE_SUBJECTS_POS, TABLE_STATES_POS, PROJECT_ID
from google.cloud import storage, bigquery
import mimetypes
import io


bucket = storage.Client().bucket(BUCKET_NAME)

def delete_accents(text):
    replacements = str.maketrans('áéíóúÁÉÍÓÚ', 'aeiouAEIOU')
    return text.translate(replacements)

def get_active_pos_names_norm():
    # Obtener los nombres normalizados de parkings off-street activos

    query = f"""
    SELECT p.name_norm
    FROM `{TABLE_SUBJECTS_POS}` p
    JOIN `{TABLE_STATES_POS}` a
      ON p.states_id = a.id
    WHERE a.is_open = true
    """
    rows = bigquery.Client().query(query).result()

    active_pos_names_norm = [row['name_norm'] for row in rows]

    # Crear un diccionario con los nombres de los parkings y una lista de sus posibles alias
    parkings_alias = {
        delete_accents(parking.lower()): [delete_accents(parking.lower())]
        for parking in active_pos_names_norm
    }

    # Añadir alias manualmente
    parkings_alias["san-bernardo"].append("sb")
    parkings_alias["nuevos-juzgados"].append("juzgados")

    return parkings_alias

def upload_files_to_gcp(attachments):
    for filename, data in attachments.items():
        blob = bucket.blob(filename)
        content_type, _ = mimetypes.guess_type(filename)
        blob.upload_from_file(
            io.BytesIO(data),
            content_type=content_type or "application/octet-stream"
        )

def get_missing_files():
    # Obtener los archivos faltantes de un datalake
    from agenda  import agenda

    missing_files = {}

    for _, responsibles in agenda.items():
        for responsible, file_paths in responsibles.items():
            for f in file_paths:
                exists = bucket.blob(f).exists()
                if not exists:
                    if responsible not in missing_files: missing_files[responsible] = []
                    missing_files[responsible].append(f)
                    
    return missing_files
