from gcp.utils import get_active_pos_names_norm
from gcp.paths import * 


active_pos_names_norm = get_active_pos_names_norm()

agenda = {

    "moxsi": {

            "javieracosta": [path_ingresos]
            
    },

    "parkings-off_street": {

            "jgonzalez":        [
                path_abonos_lpa_y_qr, 
                path_ocupacion_ld, 
                path_ocupacion_lv, 
                path_ocupacion_sd, 
                path_ocupacion] + [
                path_rotacion.replace('$', s) for s in active_pos_names_norm] + [
                path_abonados.replace('$', s) for s in active_pos_names_norm
            ],
            "javieracosta":     [path_recaudacion],
            "maricarmensuarez": [path_abonados_en_banco, path_rincon_estadisticas],
            "aparcamientos":    [path_informes_filtrados.replace('$', s) for s in active_pos_names_norm]
    
    }
}
