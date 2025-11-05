import pandas as pd


# Fecha del mes anterior
prev_month = pd.Timestamp.now() - pd.DateOffset(months=1)
year       = prev_month.year
date       = prev_month.strftime("%Y%m")


PROJECT_ID = 'bigdata-fase2'

# BigQuery
DATASET            = f'{PROJECT_ID}.parkings_datamart'
TABLE_SUBJECTS_POS = f'{DATASET}.subjects'
TABLE_STATES_POS   = f'{DATASET}.states'

# Cloud Storage
BUCKET_NAME         =  'sagulpa-datalake'
PATH_DATALAKE_POS   = f'parkings-off_street/documents/{year}'
PATH_DATALAKE_MOXSI = f'moxsi/documents/{year}'


# Rutas de parkings off-street
path_recaudacion         = f'{PATH_DATALAKE_POS}/financiero.recaudacion'            + f'/{date}.xls'
path_abonados_en_banco   = f'{PATH_DATALAKE_POS}/financiero.abonados-en-banco'      + f'/{date}.xlsx'
path_rincon_estadisticas = f'{PATH_DATALAKE_POS}/aparcamientos.rincon-estadisticas' + f'/{date}.xlsx'
path_informes_filtrados  = f'{PATH_DATALAKE_POS}/aparcamientos.informes-filtrados'  + f'/{date}.$.pdf'
path_abonados            = f'{PATH_DATALAKE_POS}/sistemas.abonados'                 + f'/{date}.$.xlsx'
path_rotacion            = f'{PATH_DATALAKE_POS}/sistemas.rotacion'                 + f'/{date}.$.xlsx'
path_abonos_lpa_y_qr     = f'{PATH_DATALAKE_POS}/sistemas.abonados-qr-lpa'          + f'/{date}.xlsx'
path_ocupacion           = f'{PATH_DATALAKE_POS}/sistemas.ocupacion'                + f'/{date}.xlsx'
path_ocupacion_ld        = f'{PATH_DATALAKE_POS}/sistemas.ocupacion-ld'             + f'/{date}.xls'
path_ocupacion_lv        = f'{PATH_DATALAKE_POS}/sistemas.ocupacion-lv'             + f'/{date}.xls'
path_ocupacion_sd        = f'{PATH_DATALAKE_POS}/sistemas.ocupacion-sd'             + f'/{date}.xls'

# Rutas de moxsi
path_incidencias         = f'{PATH_DATALAKE_MOXSI}/moxsi.incidencias'               + f'/{date}.xlsx'
path_vehiculo_id         = f'{PATH_DATALAKE_MOXSI}/moxsi.vehiculos'                 + f'/{date}.xlsx'
path_repuestos           = f'{PATH_DATALAKE_MOXSI}/moxsi.repuestos'                 + f'/{date}.csv'
path_inventario          = f'{PATH_DATALAKE_MOXSI}/moxsi.inventario'                + f'/{date}.csv'
path_abonos              = f'{PATH_DATALAKE_MOXSI}/financiero.abonos'               + f'/{date}.csv'
path_ingresos            = f'{PATH_DATALAKE_MOXSI}/financiero.ingresos'             + f'/{date}.csv'
path_clientes            = f'{PATH_DATALAKE_MOXSI}/nextbike.customer-details'       + f'/{date}.csv'
path_alquileres          = f'{PATH_DATALAKE_MOXSI}/nextbike.alquileres'             + f'/{date}.csv'
path_alquileres_con_bono = f'{PATH_DATALAKE_MOXSI}/nextbike.alquileres-con-bono'    + f'/{date}.csv'
path_alquileres_sin_bono = f'{PATH_DATALAKE_MOXSI}/nextbike.alquileres-sin-bono'    + f'/{date}.csv'


def get_gcp_path(f_name, parkings_alias):
    'Devuelve la ruta GCP correspondiente al nombre del archivo adjunto.'   # ? Estudiar la posibilidad de meter como parámetro el sender para no tener tantos ifs

    f_name = delete_accents(f_name.lower()).replace('\n', ' ').replace(' ', '-').strip()

    if   f_name.startswith('abonados wps'):                                         return path_abonados_en_banco
    elif f_name.startswith('gestion'):                                              return path_recaudacion
    elif f_name.startswith('ocupacion aparc'):                                      return path_ocupacion
    elif f_name.startswith('ocupacion_todos'):                                      return path_ocupacion_ld
    elif f_name.startswith('ocupacion_lunes_viernes'):                              return path_ocupacion_lv
    elif f_name.startswith('ocupacion_sabados_domingos'):                           return path_ocupacion_sd
    elif f_name.startswith('abonos &'):                                             return path_abonos_lpa_y_qr
    elif f_name.startswith('informe'):                                              return path_informes_filtrados.replace('$', get_parking_from(f_name, parkings_alias))
    elif f_name.startswith('abonados'):                                             return path_abonados.replace('$', get_parking_from(f_name, parkings_alias))
    elif f_name.startswith('rotacion'):                                             return path_rotacion.replace('$', get_parking_from(f_name, parkings_alias))
    elif f_name.startswith('rincon') or f_name.startswith('estadisticas - rincon'): return path_rincon_estadisticas

    elif f_name.startswith(f'{date} - moxsi incidencias'):                          return path_incidencias
    elif f_name.startswith(f'abonos'):                                              return path_abonados
    elif f_name.startswith(f'alquileres con bono'):                                 return path_alquileres_con_bono
    elif f_name.startswith(f'alquileres sin bono'):                                 return path_alquileres_sin_bono
    elif f_name.startswith(f'ingresos'):                                            return path_ingresos
    elif f_name.startswith(f'inventario'):                                          return path_inventario
    elif f_name.startswith(f'repuestos'):                                           return path_repuestos
    elif f_name.startswith(f'rentals'):                                             return path_alquileres
    elif f_name.startswith(f'vehiculo_id'):                                         return path_vehiculo_id
    elif f_name.startswith(f'customers'):                                           return path_clientes
   
    else:                                                                           return None


def identify_attachments(attachments):
    """Identifica y clasifica los archivos adjuntos recibidos."""
    from gcp.utils import get_active_pos_names_norm

    parkings_alias = get_active_pos_names_norm()

    identified_attachments = {}
    for filename, data in attachments.items():
        gcp_path = get_gcp_path(filename, parkings_alias)
        if gcp_path: identified_attachments[gcp_path] = data
    return identified_attachments

def get_parking_from(file_name, parkings_alias):
    for aliases in parkings_alias.values():
        if any(alias in file_name for alias in aliases): 
            return aliases[0].replace(' ', '-')
    raise ValueError(f"Parking no encontrado en {file_name}")

def delete_accents(text):
    replacements = str.maketrans('áéíóúÁÉÍÓÚ', 'aeiouAEIOU')
    return text.translate(replacements)
