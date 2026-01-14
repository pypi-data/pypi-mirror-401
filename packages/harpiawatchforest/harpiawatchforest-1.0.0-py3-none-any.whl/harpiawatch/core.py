"""
Módulo principal de HarpiaWatchForest
Contiene la lógica de procesamiento y análisis
"""

import ee
import datetime
from .utils import (
    normalizar_texto, quitar_tildes, apply_cloud_score_plus,
    weekly_ndvi_median, add_ndvi, remove_holes,
    agregar_capacidad_agrologica, agregar_area_protegida,
    normalizar_atributos_sinap, MESES
)
from .config import HarpiaConfig


class HarpiaAnalyzer:
    """
    Clase principal para el análisis de pérdida de cobertura vegetal
    """
    
    def __init__(self, config=None):
        """
        Inicializa el analizador
        
        Args:
            config (HarpiaConfig, optional): Configuración personalizada
        """
        self.config = config if config else HarpiaConfig()
        self._initialized = False
        
    def initialize(self, authenticate=True):
        """
        Inicializa Google Earth Engine
        
        Args:
            authenticate (bool): Si debe autenticar (primera vez)
        """
        try:
            if authenticate:
                try:
                    ee.Authenticate()
                except:
                    print("Ya autenticado o error de autenticación")
            
            ee.Initialize(project=self.config.ee_project)
            
            # Cargar capas base
            self.Distrito = ee.FeatureCollection(self.config.asset_distrito)
            self.Corregimientos = ee.FeatureCollection(self.config.asset_corregimientos)
            self.Sinap = ee.FeatureCollection(self.config.asset_sinap)
            self.Hexagonos = ee.FeatureCollection(self.config.asset_hexagonos)
            self.Capacidad_Agrologica = ee.FeatureCollection(self.config.asset_capacidad_agrologica)
            
            self._initialized = True
            print("✅ HarpiaWatchForest inicializado correctamente")
            
        except Exception as e:
            print(f"❌ Error al inicializar: {e}")
            raise
            
    def listar_corregimientos(self):
        """Lista todos los corregimientos disponibles"""
        if not self._initialized:
            raise RuntimeError("Debe llamar a initialize() primero")
            
        return listar_corregimientos(self.Corregimientos)
        
    def obtener_hexagonos(self, nombre_corregimiento):
        """
        Obtiene hexágonos de un corregimiento
        
        Args:
            nombre_corregimiento (str): Nombre del corregimiento
            
        Returns:
            list: Lista de IDs de hexágonos
        """
        if not self._initialized:
            raise RuntimeError("Debe llamar a initialize() primero")
            
        return obtener_hexagonos_corregimiento(
            nombre_corregimiento,
            self.Corregimientos,
            self.Hexagonos
        )
        
    def procesar(self):
        """
        Procesa todos los corregimientos configurados
        
        Returns:
            list: Resultados del procesamiento
        """
        if not self._initialized:
            raise RuntimeError("Debe llamar a initialize() primero")
            
        return procesar_todos_corregimientos(
            self.config,
            self.Corregimientos,
            self.Hexagonos,
            self.Sinap,
            self.Capacidad_Agrologica
        )
        
    def procesar_corregimiento(self, nombre_corregimiento):
        """
        Procesa un corregimiento específico
        
        Args:
            nombre_corregimiento (str): Nombre del corregimiento
        """
        if not self._initialized:
            raise RuntimeError("Debe llamar a initialize() primero")
            
        return procesar_corregimiento_individual(
            nombre_corregimiento,
            self.config,
            self.Corregimientos,
            self.Hexagonos,
            self.Sinap,
            self.Capacidad_Agrologica
        )


def listar_corregimientos(corregimientos_fc):
    """
    Lista todos los corregimientos disponibles
    
    Args:
        corregimientos_fc: FeatureCollection de corregimientos
        
    Returns:
        list: Lista de nombres de corregimientos
    """
    try:
        nombres = corregimientos_fc.aggregate_array('LMCO_NOMB').getInfo()
        nombres_unicos = sorted(list(set(nombres)))

        print("\n" + "="*80)
        print("CORREGIMIENTOS DISPONIBLES")
        print("="*80)
        for i, nombre in enumerate(nombres_unicos, 1):
            print(f"{i:3d}. {nombre}")
        print("="*80)
        print(f"Total: {len(nombres_unicos)} corregimientos\n")

        return nombres_unicos
    except Exception as e:
        print(f"❌ Error al listar corregimientos: {e}")
        return []


def obtener_hexagonos_corregimiento(nombre_corregimiento, corregimientos_fc, hexagonos_fc):
    """
    Extrae la lista de hexágonos que intersectan con un corregimiento
    
    Args:
        nombre_corregimiento (str): Nombre del corregimiento
        corregimientos_fc: FeatureCollection de corregimientos
        hexagonos_fc: FeatureCollection de hexágonos
        
    Returns:
        list: Lista de IDs de hexágonos
    """
    try:
        corregimiento = corregimientos_fc.filter(ee.Filter.eq("LMCO_NOMB", nombre_corregimiento))

        if corregimiento.size().getInfo() == 0:
            print(f"❌ Error: No se encontró el corregimiento '{nombre_corregimiento}'")
            return []

        hexagonos_en_area = hexagonos_fc.filterBounds(corregimiento)
        grid_ids = hexagonos_en_area.aggregate_array('GRID_ID').getInfo()
        grid_ids_sorted = sorted(grid_ids)

        print(f"✅ Corregimiento: {nombre_corregimiento}")
        print(f"✅ Total de hexágonos encontrados: {len(grid_ids_sorted)}\n")

        return grid_ids_sorted

    except Exception as e:
        print(f"❌ Error al obtener hexágonos: {e}")
        return []


def procesar_corregimiento_individual(nombre_corregimiento, config, 
                                      corregimientos_fc, hexagonos_fc,
                                      sinap_fc, capacidad_fc):
    """
    Procesa un corregimiento completo
    
    Args:
        nombre_corregimiento (str): Nombre del corregimiento
        config (HarpiaConfig): Configuración
        corregimientos_fc: FeatureCollection de corregimientos
        hexagonos_fc: FeatureCollection de hexágonos
        sinap_fc: FeatureCollection del SINAP
        capacidad_fc: FeatureCollection de capacidad agrológica
    """
    print(f"\n{'#'*80}")
    print(f"# INICIANDO PROCESAMIENTO: {nombre_corregimiento}")
    print(f"{'#'*80}\n")

    # Fecha de ejecución
    fecha_ejecucion = datetime.datetime.now().strftime('%Y-%m-%d')

    # Obtener hexágonos
    cuadriculas = obtener_hexagonos_corregimiento(nombre_corregimiento, corregimientos_fc, hexagonos_fc)

    if len(cuadriculas) == 0:
        print(f"⚠️ No se encontraron hexágonos para {nombre_corregimiento}. Saltando...")
        return

    # Normalizar nombre
    nombre_norm = normalizar_texto(nombre_corregimiento)
    corregimiento_clean = quitar_tildes(nombre_corregimiento).upper().replace(" ", "-")
    mes_texto = MESES.get(config.month_analisis, f"MES-{config.month_analisis}")
    name_folder = f"SHP-PERDIDAS-CORREGIMIENTO-{corregimiento_clean}-{mes_texto}-{config.year_analisis}"

    # Calcular semanas
    first_day = datetime.date(config.year_analisis, config.month_analisis, 1)
    if config.month_analisis == 12:
        last_day = datetime.date(config.year_analisis + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        last_day = datetime.date(config.year_analisis, config.month_analisis + 1, 1) - datetime.timedelta(days=1)

    first_week = first_day.isocalendar()[1]
    last_week = last_day.isocalendar()[1]

    if config.month_analisis == 1 and first_week > 50:
        first_week = 1
    if config.month_analisis == 12 and last_week < 10:
        last_week = 52

    mes_nombre = first_day.strftime('%B')
    area_str = str(config.min_area_ha).replace('.', '_')

    print("="*80)
    print("CONFIGURACIÓN DEL ANÁLISIS")
    print("="*80)
    print(f"📍 Corregimiento: {nombre_corregimiento}")
    print(f"📅 Período: {mes_nombre} {config.year_analisis} (Semanas {first_week}-{last_week})")
    print(f"🔷 Cuadrículas a procesar: {len(cuadriculas)}")
    print(f"📏 Área mínima: {config.min_area_ha} ha")
    print(f"📉 Umbral NDVI: {config.threshold_ndvi_low}")
    print(f"📁 Carpeta: {name_folder}")
    print("="*80)

    # Contadores
    hexagonos_exitosos = 0
    hexagonos_sin_datos = 0
    hexagonos_con_error = 0

    # Procesar cada hexágono
    for num_cuadricula in cuadriculas:
        print(f"\n{'='*80}")
        print(f"PROCESANDO HEXÁGONO {num_cuadricula} ({cuadriculas.index(num_cuadricula)+1}/{len(cuadriculas)})")
        print(f"{'='*80}")

        try:
            # Seleccionar cuadrícula
            cuadricula_seleccionada = hexagonos_fc.filter(ee.Filter.eq('GRID_ID', num_cuadricula))
            study_area = cuadricula_seleccionada.geometry()

            # Cargar Sentinel-2
            print(f"[{num_cuadricula}] Cargando imágenes Sentinel-2...")
            s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
                .filterBounds(study_area) \
                .filterDate(config.date_start, config.date_end)

            s2_clipped = s2.map(lambda img: img.clip(study_area))
            s2_filtered = apply_cloud_score_plus(s2_clipped, study_area, config.date_start, config.date_end)

            # Calcular NDVI semanales
            print(f"[{num_cuadricula}] Calculando NDVI semanales...")
            weekly_ndvi = {}

            for w in range(first_week, last_week + 1):
                label = f'{config.year_analisis}-W{str(w).zfill(2)}'
                ndvi_img = weekly_ndvi_median(s2_filtered, config.year_analisis, w, study_area)
                weekly_ndvi[label] = ndvi_img

                if ndvi_img is not None:
                    print(f"  ✓ NDVI calculado para {label}")
                else:
                    print(f"  ✗ Sin datos para {label}")

            # Calcular cambios
            print(f"[{num_cuadricula}] Calculando cambios NDVI...")
            ndvi_changes = {}

            for w in range(first_week + 1, last_week + 1):
                current_label = f'{config.year_analisis}-W{str(w).zfill(2)}'
                previous_label = f'{config.year_analisis}-W{str(w-1).zfill(2)}'

                if weekly_ndvi[current_label] is not None and weekly_ndvi[previous_label] is not None:
                    change = weekly_ndvi[current_label].subtract(weekly_ndvi[previous_label])
                    ndvi_changes[f'{previous_label}_to_{current_label}'] = change
                    print(f"  ✓ Cambio {previous_label} → {current_label}")

            if len(ndvi_changes) == 0:
                print(f"  ⚠️ No hay cambios NDVI para cuadrícula {num_cuadricula}, saltando...")
                hexagonos_sin_datos += 1
                continue

            # CCDC
            print(f"[{num_cuadricula}] Ejecutando CCDC...")
            s2_ndvi = s2_filtered.map(add_ndvi)

            ccdc = ee.Algorithms.TemporalSegmentation.Ccdc(
                s2_ndvi.select(['ndvi', 'B5', 'B12']),
                ['ndvi', 'B5', 'B12'],
                ['B5', 'B12'],
                8, 0.90, 0.80, 2, 50, 35000
            )

            tbreak = ccdc.select('tBreak')
            argmax = tbreak.arrayArgmax()
            argmax_scalar = argmax.arrayFlatten([['argmax_array']])
            last_break = tbreak.arrayGet(argmax_scalar).focal_min(1).focal_max(1)

            # Filtrar fechas
            start_millis = ee.Date(f'{config.year_analisis}-01-01').millis()
            end_millis = ee.Date(f'{config.year_analisis}-12-31').millis()
            filtered = last_break.updateMask(
                last_break.gte(start_millis).And(last_break.lte(end_millis))
            )

            # Calcular semana
            year = filtered.divide(1000 * 60 * 60 * 24 * 365.25).add(1970).floor()
            days_since_1970 = filtered.divide(1000 * 60 * 60 * 24).floor()
            weeks_since_1970 = days_since_1970.divide(7).floor()
            weeks_in_years = year.subtract(1970).multiply(52.18)
            week = weeks_since_1970.subtract(weeks_in_years).mod(52).add(1).floor()
            year_week = year.multiply(100).add(week).rename('year_week')

            # Generar polígonos
            print(f"[{num_cuadricula}] Generando polígonos de pérdida...")

            perdidas_todas = ee.ImageCollection([
                change_img.lt(config.threshold_ndvi_low).selfMask()
                for key, change_img in ndvi_changes.items()
            ]).max()

            yyyyww_init = config.year_analisis * 100 + first_week
            yyyyww_end = config.year_analisis * 100 + last_week
            todos_cambios_mask = year_week.gte(yyyyww_init).And(year_week.lte(yyyyww_end))
            perdidas_filtradas = perdidas_todas.updateMask(todos_cambios_mask)

            poligonos_perdida = perdidas_filtradas.reduceToVectors(**{
                'geometry': study_area,
                'scale': 10,
                'geometryType': 'polygon',
                'eightConnected': False,
                'labelProperty': 'change',
                'maxPixels': 1e8
            })

            # Filtrar por área
            error_margin = 1
            poligonos_area = poligonos_perdida.map(
                lambda f: f.set('Area_Ha', f.geometry(error_margin).area(error_margin).divide(10000))
            )
            poligonos_filtrados = poligonos_area.filter(ee.Filter.gt('Area_Ha', config.min_area_ha))

            poligonos_limpios = poligonos_filtrados.map(remove_holes)

            # Agregar metadatos
            def extract_date_feature(f):
                date_info = filtered.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=f.geometry(),
                    scale=10,
                    maxPixels=1e8
                )
                millis = ee.Number(date_info.get(filtered.bandNames().get(0)))
                date = ee.Date(millis)
                formatted_date = date.format('yyyy-MM-dd')
                week_num = date.getRelative('week', 'year').add(1)

                return f.set({
                    'Fecha_Detec': formatted_date,
                    'Semana': week_num,
                    'Year': config.year_analisis,
                    'Month': config.month_analisis,
                    'GRID_ID': num_cuadricula,
                    'Corregimiento': nombre_norm,
                    'Fecha_Ejec': fecha_ejecucion
                })

            poligonos_con_fecha = poligonos_limpios.map(extract_date_feature)

            # Capacidad agrológica
            print(f"[{num_cuadricula}] Agregando Capacidad Agrológica...")
            poligonos_con_capacidad = poligonos_con_fecha.map(
                lambda f: agregar_capacidad_agrologica(f, capacidad_fc)
            )

            # SINAP
            print(f"[{num_cuadricula}] Agregando información de Áreas Protegidas...")
            poligonos_con_sinap = poligonos_con_capacidad.map(
                lambda f: agregar_area_protegida(f, sinap_fc)
            )

            poligonos_finales = poligonos_con_sinap.map(normalizar_atributos_sinap)

            # Exportar
            print(f"[{num_cuadricula}] Verificando polígonos antes de exportar...")
            num_poligonos = poligonos_finales.size().getInfo()

            if num_poligonos == 0:
                print(f"  ⚠️ No se detectaron pérdidas > {config.min_area_ha} ha")
                hexagonos_sin_datos += 1
                continue

            print(f"[{num_cuadricula}] Iniciando exportación de {num_poligonos} polígonos...")

            export_description = f'Perdidas_NDVI_GRID_ID_{num_cuadricula}_{area_str}ha_{mes_nombre}{config.year_analisis}_W{first_week}-W{last_week}'

            export_perdidas = ee.batch.Export.table.toDrive(
                collection=poligonos_finales,
                description=export_description,
                folder=name_folder,
                fileFormat='SHP'
            )
            export_perdidas.start()

            print(f"  ✓ Exportación iniciada: {export_description}")
            hexagonos_exitosos += 1

        except Exception as e:
            print(f"  ✗ ERROR en cuadrícula {num_cuadricula}: {str(e)}")
            hexagonos_con_error += 1
            continue

    # Resumen
    print(f"\n{'='*80}")
    print(f"RESUMEN - {nombre_corregimiento}")
    print(f"{'='*80}")
    print(f"✅ Hexágonos procesados: {hexagonos_exitosos}")
    print(f"⚠️  Hexágonos sin datos: {hexagonos_sin_datos}")
    print(f"❌ Hexágonos con error: {hexagonos_con_error}")
    print("="*80)


def procesar_todos_corregimientos(config, corregimientos_fc, hexagonos_fc, 
                                  sinap_fc, capacidad_fc):
    """
    Procesa todos los corregimientos configurados
    """
    print("\n" + "="*80)
    print("SISTEMA DE ANÁLISIS DE PÉRDIDA DE COBERTURA VEGETAL")
    print("="*80)
    print(f"📅 Período: {MESES[config.month_analisis]} {config.year_analisis}")
    print(f"📋 Corregimientos: {len(config.lista_corregimientos)}")
    print("="*80)

    resultados = []

    for idx, nombre in enumerate(config.lista_corregimientos, 1):
        print(f"\n{'█'*80}")
        print(f"█ CORREGIMIENTO {idx}/{len(config.lista_corregimientos)}: {nombre}")
        print(f"{'█'*80}")

        try:
            procesar_corregimiento_individual(
                nombre, config, corregimientos_fc, 
                hexagonos_fc, sinap_fc, capacidad_fc
            )
            resultados.append({'corregimiento': nombre, 'estado': 'COMPLETADO'})
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            resultados.append({'corregimiento': nombre, 'estado': 'ERROR'})

    return resultados


# Funciones de conveniencia para uso directo
def procesar_corregimiento(nombre_corregimiento, config=None):
    """Función de conveniencia para procesar un corregimiento"""
    analyzer = HarpiaAnalyzer(config)
    analyzer.initialize(authenticate=False)
    return analyzer.procesar_corregimiento(nombre_corregimiento)
