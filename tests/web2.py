import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from datetime import datetime
import re
from urllib.parse import urljoin

class ScraperEconomiaElPeruano:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        })
        self.base_url = "https://elperuano.pe"
        self.economia_url = "https://elperuano.pe/economia"
        
    def obtener_pagina_economia(self):
        """Obtiene la página principal de economía"""
        print("💰 Obteniendo sección Economía...")
        
        try:
            response = self.session.get(self.economia_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f"✅ Página de economía obtenida - Status: {response.status_code}")
            return soup
            
        except requests.RequestException as e:
            print(f"❌ Error al obtener la página de economía: {e}")
            return None
    
    def extraer_articulos_economia(self, soup):
        """Extrae artículos de la sección economía"""
        print("\n📊 EXTRAYENDO ARTÍCULOS DE ECONOMÍA...")
        
        articulos = []
        
        # Estrategia 1: Buscar elementos específicos de noticias económicas
        selectores = [
            'article', 
            '.noticia',
            '.news-item',
            '.economia-item',
            '[class*="economia"]',
            '[class*="noticia"]',
            '.card',
            '.post'
        ]
        
        for selector in selectores:
            elementos = soup.select(selector)
            for elemento in elementos:
                articulo = self._procesar_articulo_economia(elemento, f"selector_{selector}")
                if articulo:
                    articulos.append(articulo)
        
        # Estrategia 2: Buscar en contenedores principales
        contenedores_principales = soup.find_all(['div', 'section'], 
                                               class_=lambda x: x and any(word in x.lower() for word in 
                                                                         ['content', 'main', 'principal', 'noticias', 'economia']))
        
        for contenedor in contenedores_principales:
            enlaces_noticias = contenedor.find_all('a', href=True)
            for enlace in enlaces_noticias:
                if self._es_enlace_noticia_economia(enlace):
                    articulo = self._procesar_desde_enlace(enlace, "contenedor_principal")
                    if articulo:
                        articulos.append(articulo)
        
        return articulos
    
    def _es_enlace_noticia_economia(self, enlace):
        """Determina si un enlace es probablemente de noticia económica"""
        href = enlace.get('href', '')
        texto = enlace.get_text().strip()
        
        # Filtros para enlaces de noticias
        if not href or href.startswith(('#', 'javascript:', 'mailto:')):
            return False
        
        # El texto debe tener características de título de noticia
        if len(texto) < 20 or len(texto) > 200:
            return False
            
        # Palabras clave que sugieren contenido económico
        palabras_clave_economia = [
            'economía', 'económico', 'económicos', 'finanzas', 'financiero',
            'mercado', 'bolsa', 'inversión', 'empresa', 'negocio', 'comercio',
            'exportación', 'importación', 'dólar', 'sol', 'inflación', 'PBI',
            'crecimiento', 'empleo', 'salario', 'presupuesto', 'gasto', 'ingreso'
        ]
        
        texto_lower = texto.lower()
        if any(palabra in texto_lower for palabra in palabras_clave_economia):
            return True
            
        return len(texto) > 30  # Títulos largos suelen ser noticias
    
    def _procesar_articulo_economia(self, elemento, fuente):
        """Procesa un elemento de artículo económico"""
        try:
            # Extraer título
            titulo_element = elemento.find(['h1', 'h2', 'h3', 'h4', 'h5']) or elemento
            titulo = titulo_element.get_text().strip()
            
            if not titulo or len(titulo) < 15:
                return None
            
            # Extraer enlace
            enlace_element = elemento.find('a', href=True)
            enlace = enlace_element.get('href', '') if enlace_element else ''
            if enlace:
                enlace = urljoin(self.base_url, enlace)
            
            # Extraer resumen/descripción
            resumen = self._extraer_resumen(elemento)
            
            # Extraer fecha si está disponible
            fecha = self._extraer_fecha(elemento)
            
            # Verificar que sea contenido económico
            if not self._es_contenido_economico(titulo, resumen):
                return None
            
            return {
                'titulo': titulo,
                'resumen': resumen,
                'enlace': enlace,
                'fecha': fecha,
                'fuente_deteccion': fuente,
                'timestamp_extraccion': datetime.now().isoformat(),
                'longitud_texto': len(titulo) + len(resumen),
                'categoria': 'economia'
            }
            
        except Exception as e:
            print(f"⚠️ Error procesando artículo: {e}")
            return None
    
    def _procesar_desde_enlace(self, enlace, fuente):
        """Procesa un artículo desde un enlace"""
        try:
            titulo = enlace.get_text().strip()
            href = enlace.get('href', '')
            enlace_completo = urljoin(self.base_url, href)
            
            if not titulo or len(titulo) < 15:
                return None
            
            # Verificar que sea contenido económico
            if not self._es_contenido_economico(titulo, ""):
                return None
            
            return {
                'titulo': titulo,
                'resumen': "",  # Se puede extraer después si es necesario
                'enlace': enlace_completo,
                'fecha': "",
                'fuente_deteccion': fuente,
                'timestamp_extraccion': datetime.now().isoformat(),
                'longitud_texto': len(titulo),
                'categoria': 'economia'
            }
            
        except Exception as e:
            print(f"⚠️ Error procesando desde enlace: {e}")
            return None
    
    def _extraer_resumen(self, elemento):
        """Extrae el resumen/descripción del artículo"""
        # Buscar párrafos de descripción
        posibles_resumenes = elemento.find_all(['p', 'span', 'div'], 
                                             class_=lambda x: x and any(word in x.lower() for word in 
                                                                       ['resumen', 'descripcion', 'summary', 'excerpt']))
        
        for resumen_element in posibles_resumenes:
            texto = resumen_element.get_text().strip()
            if len(texto) > 30 and len(texto) < 300:
                return texto
        
        # Si no encuentra resumen específico, buscar cualquier párrafo
        parrafos = elemento.find_all('p')
        for p in parrafos:
            texto = p.get_text().strip()
            if len(texto) > 50 and len(texto) < 400:
                return texto[:200] + '...' if len(texto) > 200 else texto
        
        return ""
    
    def _extraer_fecha(self, elemento):
        """Extrae la fecha del artículo si está disponible"""
        # Buscar elementos de fecha
        elementos_fecha = elemento.find_all(['time', 'span', 'div'], 
                                          class_=lambda x: x and any(word in x.lower() for word in 
                                                                    ['fecha', 'date', 'time', 'publicacion']))
        
        for fecha_element in elementos_fecha:
            texto = fecha_element.get_text().strip()
            if texto and len(texto) < 50:
                return texto
        
        return ""
    
    def _es_contenido_economico(self, titulo, resumen):
        """Determina si el contenido es económico basado en palabras clave"""
        texto_analizar = f"{titulo} {resumen}".lower()
        
        palabras_clave_economia = [
            'economía', 'económico', 'económicos', 'finanzas', 'financiero', 'financiera',
            'mercado', 'bolsa', 'inversión', 'inversiones', 'empresa', 'empresas', 'negocio', 'negocios',
            'comercio', 'exportación', 'importación', 'dólar', 'sol', 'inflación', 'PBI',
            'crecimiento', 'empleo', 'desempleo', 'salario', 'sueldo', 'presupuesto', 
            'gasto', 'ingreso', 'ingresos', 'consumo', 'producción', 'industria',
            'sector', 'empresarial', 'mercado', 'acciones', 'bolsa', 'banco', 'bancario',
            'crédito', 'deuda', 'fiscal', 'tributario', 'impuesto', 'arancel',
            'tratado', 'acuerdo comercial', 'OMC', 'FMI', 'BCRP', 'MEF'
        ]
        
        # Contar coincidencias con palabras clave económicas
        coincidencias = sum(1 for palabra in palabras_clave_economia if palabra in texto_analizar)
        
        return coincidencias >= 1  # Al menos una palabra clave económica
    
    def obtener_contenido_completo(self, articulos):
        """Obtiene el contenido completo de los artículos (opcional)"""
        print("\n📖 OBTENIENDO CONTENIDO COMPLETO...")
        
        for i, articulo in enumerate(articulos):
            if i >= 10:  # Limitar para no sobrecargar el servidor
                break
                
            if articulo['enlace']:
                try:
                    time.sleep(1)  # Respeta el servidor
                    response = self.session.get(articulo['enlace'], timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Extraer contenido principal
                        contenido = self._extraer_contenido_completo(soup)
                        if contenido:
                            articulo['contenido_completo'] = contenido
                            articulo['longitud_texto'] = len(articulo['titulo']) + len(contenido)
                            print(f"✅ Contenido completo obtenido: {articulo['titulo'][:50]}...")
                    
                except Exception as e:
                    print(f"⚠️ Error obteniendo contenido completo: {e}")
        
        return articulos
    
    def _extraer_contenido_completo(self, soup):
        """Extrae el contenido completo de un artículo"""
        # Buscar el contenido principal
        contenido_element = soup.find('article') or \
                           soup.find('div', class_=lambda x: x and any(word in x.lower() for word in 
                                                                      ['content', 'contenido', 'article', 'post-content']))
        
        if contenido_element:
            # Extraer todos los párrafos
            parrafos = contenido_element.find_all('p')
            texto_completo = ' '.join([p.get_text().strip() for p in parrafos])
            return texto_completo[:2000]  # Limitar longitud
        
        return ""
    
    def limpiar_y_filtrar(self, articulos):
        """Limpia y filtra los artículos"""
        print("\n🧹 LIMPIANDO Y FILTRANDO ARTÍCULOS...")
        
        # Eliminar None y duplicados
        articulos_limpios = [a for a in articulos if a is not None]
        
        articulos_unicos = {}
        for articulo in articulos_limpios:
            titulo_limpio = re.sub(r'\s+', ' ', articulo['titulo']).strip().lower()
            if titulo_limpio not in articulos_unicos:
                articulos_unicos[titulo_limpio] = articulo
        
        return list(articulos_unicos.values())
    
    def generar_dataset_analisis(self, articulos):
        """Genera un dataset optimizado para análisis de sentimientos"""
        print("\n📈 GENERANDO DATASET PARA ANÁLISIS...")
        
        dataset = []
        for articulo in articulos:
            # Texto para análisis (combinar título y resumen/contenido)
            texto_analisis = articulo['titulo']
            if articulo.get('resumen'):
                texto_analisis += " " + articulo['resumen']
            if articulo.get('contenido_completo'):
                texto_analisis += " " + articulo['contenido_completo']
            
            item_analisis = {
                'id': f"eco_{hash(articulo['titulo']) % 10000:04d}",
                'titulo': articulo['titulo'],
                'texto_completo': texto_analisis.strip(),
                'fecha': articulo.get('fecha', ''),
                'enlace': articulo['enlace'],
                'longitud_caracteres': len(texto_analisis),
                'longitud_palabras': len(texto_analisis.split()),
                'timestamp_extraccion': articulo['timestamp_extraccion'],
                'categoria': 'economia'
            }
            dataset.append(item_analisis)
        
        return dataset
    
    def ejecutar_scraping_economia(self, obtener_contenido_completo=False):
        """Ejecuta el scraping completo de la sección economía"""
        print("🎯 INICIANDO SCRAPING ESPECIALIZADO - SECCIÓN ECONOMÍA")
        print("=" * 70)
        
        try:
            # 1. Obtener página de economía
            soup = self.obtener_pagina_economia()
            if not soup:
                return None, None
            
            # 2. Extraer artículos
            articulos_brutos = self.extraer_articulos_economia(soup)
            print(f"📥 Artículos brutos encontrados: {len(articulos_brutos)}")
            
            # 3. Limpiar y filtrar
            articulos_limpios = self.limpiar_y_filtrar(articulos_brutos)
            print(f"🧼 Artículos después de limpieza: {len(articulos_limpios)}")
            
            # 4. Opcional: Obtener contenido completo
            if obtener_contenido_completo:
                articulos_limpios = self.obtener_contenido_completo(articulos_limpios)
            
            # 5. Generar dataset para análisis
            dataset = self.generar_dataset_analisis(articulos_limpios)
            
            # 6. Guardar resultados
            self.guardar_resultados_analisis(dataset, articulos_limpios)
            
            # 7. Mostrar resumen
            self.mostrar_resumen_economia(dataset, articulos_limpios)
            
            return dataset, articulos_limpios
            
        except Exception as e:
            print(f"❌ Error en el proceso de scraping: {e}")
            return None, None
    
    def guardar_resultados_analisis(self, dataset, articulos):
        """Guarda los resultados optimizados para análisis"""
        print("\n💾 GUARDANDO RESULTADOS PARA ANÁLISIS...")
        
        try:
            # Dataset para análisis de sentimientos
            df_analisis = pd.DataFrame(dataset)
            df_analisis.to_csv('dataset_economia_analisis.csv', index=False, encoding='utf-8-sig')
            print("✅ Dataset para análisis: dataset_economia_analisis.csv")
            
            # Artículos completos
            df_articulos = pd.DataFrame(articulos)
            df_articulos.to_csv('articulos_economia_completos.csv', index=False, encoding='utf-8-sig')
            print("✅ Artículos completos: articulos_economia_completos.csv")
            
            # Resumen en JSON
            resumen = {
                'metadata': {
                    'fecha_scraping': datetime.now().isoformat(),
                    'url': self.economia_url,
                    'total_articulos': len(dataset),
                    'objetivo': 'analisis_sentimientos'
                },
                'estadisticas_texto': {
                    'longitud_promedio': df_analisis['longitud_caracteres'].mean(),
                    'total_palabras': df_analisis['longitud_palabras'].sum(),
                    'articulos_con_fecha': sum(1 for a in articulos if a.get('fecha'))
                }
            }
            
            with open('resumen_analisis_economia.json', 'w', encoding='utf-8') as f:
                json.dump(resumen, f, ensure_ascii=False, indent=2)
            print("✅ Resumen JSON: resumen_analisis_economia.json")
            
        except Exception as e:
            print(f"❌ Error guardando archivos: {e}")
    
    def mostrar_resumen_economia(self, dataset, articulos):
        """Muestra resumen especializado para economía"""
        print("\n" + "=" * 70)
        print("💰 SCRAPING ECONOMÍA COMPLETADO!")
        print("=" * 70)
        
        if not dataset:
            print("❌ No se encontraron artículos económicos")
            return
        
        print(f"\n📈 ESTADÍSTICAS PARA ANÁLISIS:")
        print(f"   • Artículos económicos: {len(dataset)}")
        print(f"   • Longitud promedio: {int(sum(d['longitud_caracteres'] for d in dataset) / len(dataset))} caracteres")
        print(f"   • Palabras totales: {sum(d['longitud_palabras'] for d in dataset)}")
        
        print(f"\n📰 EJEMPLOS DE ARTÍCULOS ECONÓMICOS:")
        print("-" * 60)
        for i, articulo in enumerate(dataset[:5], 1):
            print(f"{i}. {articulo['titulo']}")
            print(f"   📊 Caracteres: {articulo['longitud_caracteres']}, Palabras: {articulo['longitud_palabras']}")
            if articulo['fecha']:
                print(f"   📅 Fecha: {articulo['fecha']}")
            print()

# EJECUCIÓN PRINCIPAL
if __name__ == "__main__":
    # Crear scraper especializado
    scraper_economia = ScraperEconomiaElPeruano()
    
    # Ejecutar scraping (cambiar a True si quieres contenido completo)
    dataset, articulos = scraper_economia.ejecutar_scraping_economia(
        obtener_contenido_completo=False  # Cambia a True para más texto
    )
    
    if dataset:
        print("\n✅ Dataset listo para análisis de sentimientos!")
        print("   Archivos generados:")
        print("   • dataset_economia_analisis.csv - Para tu modelo")
        print("   • articulos_economia_completos.csv - Metadatos completos")
        print("   • resumen_analisis_economia.json - Estadísticas")
    else:
        print("\n❌ No se pudo generar el dataset")