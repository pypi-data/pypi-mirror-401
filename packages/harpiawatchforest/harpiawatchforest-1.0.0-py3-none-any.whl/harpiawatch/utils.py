"""
Módulo de utilidades para HarpiaWatchForest
Contiene funciones auxiliares para procesamiento
"""

import unicodedata
import ee


def normalizar_texto(texto):
    """
    Normaliza texto removiendo acentos, espacios y caracteres especiales
    
    Args:
        texto (str): Texto a normalizar
        
    Returns:
        str: Texto normalizado
    """
    if texto is None or texto == '':
        return texto

    texto_norm = (texto
        .replace(" ", "_")
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
        .replace("Á", "A")
        .replace("É", "E")
        .replace("Í", "I")
        .replace("Ó", "O")
        .replace("Ú", "U")
        .replace("Ñ", "N")
        .replace("(", "_")
        .replace(")", "_")
        .replace("%", "")
    )
    return texto_norm


def quitar_tildes(texto):
    """
    Quita tildes usando unicodedata
    
    Args:
        texto (str): Texto con tildes
        
    Returns:
        str: Texto sin tildes
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def apply_cloud_score_plus(img_col, roi, start, end, qa_band='cs_cdf', threshold=0.8):
    """
    Aplica Cloud Score Plus para enmascarar nubes
    
    Args:
        img_col: Colección de imágenes
        roi: Región de interés
        start: Fecha inicio
        end: Fecha fin
        qa_band: Banda de calidad
        threshold: Umbral de confianza
        
    Returns:
        ee.ImageCollection: Colección con nubes enmascaradas
    """
    cs_plus = ee.ImageCollection('GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED') \
        .filterBounds(roi).filterDate(start, end)

    joined = ee.Join.inner().apply(
        primary=img_col,
        secondary=cs_plus,
        condition=ee.Filter.equals(leftField='system:index', rightField='system:index')
    )

    def merge_and_mask(pair):
        primary = ee.Image(pair.get('primary'))
        score = ee.Image(pair.get('secondary')).select(qa_band)
        return primary.updateMask(score.gte(threshold))

    return ee.ImageCollection(joined.map(merge_and_mask))


def weekly_ndvi_median(s2_collection, year, week_num, study_area):
    """
    Calcula NDVI mediano semanal
    
    Args:
        s2_collection: Colección Sentinel-2
        year: Año
        week_num: Número de semana
        study_area: Área de estudio
        
    Returns:
        ee.Image o None: Imagen NDVI o None si no hay datos
    """
    start_of_year = ee.Date.fromYMD(year, 1, 1)
    start = start_of_year.advance(week_num - 1, 'week')
    end = start.advance(1, 'week')

    weekly_collection = s2_collection.filterDate(start, end).filterBounds(study_area)
    count_value = weekly_collection.size().getInfo()

    if count_value > 0:
        weekly = weekly_collection.median()
        ndvi = weekly.normalizedDifference(['B8', 'B12']).rename('NDVI')
        return ndvi.clip(study_area)
    else:
        return None


def add_ndvi(img):
    """
    Agrega banda NDVI a imagen
    
    Args:
        img: Imagen Sentinel-2
        
    Returns:
        ee.Image: Imagen con banda NDVI
    """
    ndvi = img.normalizedDifference(['B8', 'B4']).multiply(10000).int16().rename('ndvi')
    return img.addBands(ndvi)


def remove_holes(feature):
    """
    Remueve huecos interiores de polígonos
    
    Args:
        feature: Feature con geometría
        
    Returns:
        ee.Feature: Feature sin huecos
    """
    geom = feature.geometry()
    tipo = geom.type()

    def process_polygon(polygon_coords):
        outer_ring = ee.List(polygon_coords).get(0)
        return ee.Geometry.Polygon([outer_ring])

    cleaned_geom = ee.Algorithms.If(
        tipo.equals('Polygon'),
        process_polygon(geom.coordinates()),
        ee.Geometry.MultiPolygon(
            ee.List(geom.coordinates()).map(lambda part:
                ee.List([ee.List(part).get(0)])
            )
        )
    )

    return feature.setGeometry(ee.Geometry(cleaned_geom))


def agregar_capacidad_agrologica(feature, capacidad_agrologica_fc):
    """
    Realiza intersect con la capa de Capacidad Agrológica
    
    Args:
        feature: Feature a enriquecer
        capacidad_agrologica_fc: FeatureCollection de capacidad agrológica
        
    Returns:
        ee.Feature: Feature con atributo Cap_Agrolog
    """
    geom = feature.geometry()
    capacidad_intersect = capacidad_agrologica_fc.filterBounds(geom)

    def get_intersection_area(cap_feature):
        intersection = cap_feature.geometry().intersection(geom, 1)
        area = intersection.area(1)
        return cap_feature.set('intersect_area', area)

    capacidad_con_area = capacidad_intersect.map(get_intersection_area)
    capacidad_sorted = capacidad_con_area.sort('intersect_area', False)
    capacidad_primera = ee.Feature(capacidad_sorted.first())

    tipos_value = ee.Algorithms.If(
        capacidad_primera,
        capacidad_primera.get('Tipos'),
        'Sin_Datos'
    )

    return feature.set('Cap_Agrolog', tipos_value)


def agregar_area_protegida(feature, sinap_fc):
    """
    Realiza intersect con la capa SINAP
    
    Args:
        feature: Feature a enriquecer
        sinap_fc: FeatureCollection del SINAP
        
    Returns:
        ee.Feature: Feature con atributos SINAP
    """
    geom = feature.geometry()
    sinap_intersect = sinap_fc.filterBounds(geom)
    num_areas = sinap_intersect.size()

    def get_intersection_area(sinap_feature):
        intersection = sinap_feature.geometry().intersection(geom, 1)
        area = intersection.area(1)
        return sinap_feature.set('intersect_area', area)

    sinap_con_area = sinap_intersect.map(get_intersection_area)
    sinap_sorted = sinap_con_area.sort('intersect_area', False)
    sinap_primera = ee.Feature(sinap_sorted.first())

    nombre_area_raw = ee.Algorithms.If(
        num_areas.gt(0),
        sinap_primera.get('Nombre'),
        'Fuera_del_SINAP'
    )

    en_area_protegida = ee.Algorithms.If(
        num_areas.gt(0),
        'Si',
        'No'
    )

    return feature.set({
        'SINAP': en_area_protegida,
        'Nom_SINAP_raw': nombre_area_raw
    })


def normalizar_atributos_sinap(feature):
    """
    Normaliza el atributo Nom_SINAP
    
    Args:
        feature: Feature con Nom_SINAP_raw
        
    Returns:
        ee.Feature: Feature con Nom_SINAP normalizado
    """
    nombre_raw = ee.String(feature.get('Nom_SINAP_raw'))

    nombre_norm = (nombre_raw
        .replace(' ', '_', 'g')
        .replace('á', 'a', 'g')
        .replace('é', 'e', 'g')
        .replace('í', 'i', 'g')
        .replace('ó', 'o', 'g')
        .replace('ú', 'u', 'g')
        .replace('ñ', 'n', 'g')
        .replace('Á', 'A', 'g')
        .replace('É', 'E', 'g')
        .replace('Í', 'I', 'g')
        .replace('Ó', 'O', 'g')
        .replace('Ú', 'U', 'g')
        .replace('Ñ', 'N', 'g')
        .replace('\\(', '_', 'g')
        .replace('\\)', '_', 'g')
        .replace('%', '', 'g')
    )

    return feature.set('Nom_SINAP', nombre_norm).set('Nom_SINAP_raw', None)


# Diccionario de meses
MESES = {
    1: "ENERO", 2: "FEBRERO", 3: "MARZO", 4: "ABRIL",
    5: "MAYO", 6: "JUNIO", 7: "JULIO", 8: "AGOSTO",
    9: "SEPTIEMBRE", 10: "OCTUBRE", 11: "NOVIEMBRE", 12: "DICIEMBRE"
}
