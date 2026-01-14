"""
Módulo de configuración para HarpiaWatchForest
Permite al usuario configurar parámetros de análisis y rutas de assets
"""

class HarpiaConfig:
    """
    Clase de configuración para HarpiaWatchForest
    
    Attributes:
        lista_corregimientos (list): Lista de corregimientos a analizar
        year_analisis (int): Año de análisis
        month_analisis (int): Mes de análisis (1-12)
        min_area_ha (float): Área mínima para exportar polígonos (hectáreas)
        threshold_ndvi_low (float): Umbral para pérdida significativa de NDVI
        date_start (str): Fecha inicial para datos Sentinel-2 (formato 'YYYY-MM-DD')
        date_end (str): Fecha final para datos Sentinel-2 (formato 'YYYY-MM-DD')
        ee_project (str): ID del proyecto de Google Earth Engine
        
    Asset paths (pueden ser modificados):
        asset_distrito (str): Ruta al asset de distritos
        asset_corregimientos (str): Ruta al asset de corregimientos
        asset_sinap (str): Ruta al asset del SINAP
        asset_hexagonos (str): Ruta al asset de hexágonos
        asset_capacidad_agrologica (str): Ruta al asset de capacidad agrológica
    """
    
    def __init__(self):
        # Parámetros de análisis editables
        self.lista_corregimientos = ['Buena Vista', 'Chepigana']
        self.year_analisis = 2026
        self.month_analisis = 1
        self.min_area_ha = 0.15
        self.threshold_ndvi_low = -0.15
        self.date_start = '2023-01-01'
        self.date_end = '2029-12-31'
        
        # Proyecto de Google Earth Engine
        self.ee_project = 'proyecto-cobertura-boscosa'
        
        # Assets de capas base (editables)
        self.asset_distrito = "projects/proyecto-cobertura-boscosa/assets/Mapas_Panama/Lim_Distrito"
        self.asset_corregimientos = "projects/proyecto-cobertura-boscosa/assets/Mapas_Panama/Lim_Corregimiento"
        self.asset_sinap = "projects/proyecto-cobertura-boscosa/assets/Mapas_Panama/SINAP"
        self.asset_hexagonos = "projects/proyecto-cobertura-boscosa/assets/Mapas_Panama/hexagonos_2025"
        self.asset_capacidad_agrologica = "projects/proyecto-cobertura-boscosa/assets/Mapas_Panama/Capacidad_Agrologica"
        
    def set_corregimientos(self, lista):
        """
        Establece la lista de corregimientos a analizar
        
        Args:
            lista (list): Lista de nombres de corregimientos
        """
        self.lista_corregimientos = lista
        
    def set_periodo(self, year, month):
        """
        Establece el período de análisis
        
        Args:
            year (int): Año
            month (int): Mes (1-12)
        """
        self.year_analisis = year
        self.month_analisis = month
        
    def set_parametros_deteccion(self, min_area_ha=None, threshold_ndvi=None):
        """
        Establece parámetros de detección
        
        Args:
            min_area_ha (float, optional): Área mínima en hectáreas
            threshold_ndvi (float, optional): Umbral de NDVI
        """
        if min_area_ha is not None:
            self.min_area_ha = min_area_ha
        if threshold_ndvi is not None:
            self.threshold_ndvi_low = threshold_ndvi
            
    def set_rango_fechas(self, date_start, date_end):
        """
        Establece el rango de fechas para datos Sentinel-2
        
        Args:
            date_start (str): Fecha inicial (formato 'YYYY-MM-DD')
            date_end (str): Fecha final (formato 'YYYY-MM-DD')
        """
        self.date_start = date_start
        self.date_end = date_end
        
    def set_ee_project(self, project_id):
        """
        Establece el ID del proyecto de Google Earth Engine
        
        Args:
            project_id (str): ID del proyecto
        """
        self.ee_project = project_id
        
    def set_assets(self, distrito=None, corregimientos=None, sinap=None, 
                   hexagonos=None, capacidad_agrologica=None):
        """
        Establece rutas personalizadas para los assets
        
        Args:
            distrito (str, optional): Ruta al asset de distritos
            corregimientos (str, optional): Ruta al asset de corregimientos
            sinap (str, optional): Ruta al asset del SINAP
            hexagonos (str, optional): Ruta al asset de hexágonos
            capacidad_agrologica (str, optional): Ruta al asset de capacidad agrológica
        """
        if distrito:
            self.asset_distrito = distrito
        if corregimientos:
            self.asset_corregimientos = corregimientos
        if sinap:
            self.asset_sinap = sinap
        if hexagonos:
            self.asset_hexagonos = hexagonos
        if capacidad_agrologica:
            self.asset_capacidad_agrologica = capacidad_agrologica
            
    def __repr__(self):
        """Representación en string de la configuración"""
        return (f"HarpiaConfig(\n"
                f"  Corregimientos: {self.lista_corregimientos}\n"
                f"  Período: {self.month_analisis}/{self.year_analisis}\n"
                f"  Área mínima: {self.min_area_ha} ha\n"
                f"  Umbral NDVI: {self.threshold_ndvi_low}\n"
                f"  Proyecto EE: {self.ee_project}\n"
                f")")
