from gcp.utils import get_active_pos_names_norm
from gcp.paths import * 


active_pos_names_norm = get_active_pos_names_norm()

agenda = {

    "moxsi": {
        
            "jmunoz": [
                path_incidencias,
                path_abonos,
                path_alquileres,
                path_alquileres_con_bono,
                path_alquileres_sin_bono,
                path_ingresos,
                path_inventario,
                path_repuestos,
                path_vehiculo_id,
                path_clientes
            ]

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
