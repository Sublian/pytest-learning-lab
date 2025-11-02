import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from datetime import datetime
import re

class ScraperElPeruano:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        self.base_url = "https://elperuano.pe"
        
    def obtener_pagina_principal(self):
        """Obtiene y analiza la página principal"""
        print("📰 Obteniendo página principal...")
        
        try:
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.RequestException as e:
            print(f"❌ Error al obtener la página: {e}")
            return None
    
    def analizar_estructura_avanzada(self, soup):
        """Análisis más profundo de la estructura del sitio"""
        print("\n🔍 ANALIZANDO ESTRUCTURA AVANZADA...")
        
        # Buscar contenedores comunes de noticias
        contenedores_potenciales = soup.find_all(['div', 'section', 'article'])
        estructuras_detectadas = []
        
        for contenedor in contenedores_potenciales[:20]:  # Analizar primeros 20
            clases = contenedor.get('class', [])
            id_ = contenedor.get('id', '')
            
            # Buscar patrones que sugieran contenido de noticias
            if clases or id_:
                info = {
                    'tag': contenedor.name,
                    'clases': clases,
                    'id': id_,
                    'texto_preview': contenedor.get_text()[:50].strip() + '...' if contenedor.get_text() else '',
                    'enlaces': len(contenedor.find_all('a', href=True)),
                    'imagenes': len(contenedor.find_all('img'))
                }
                
                # Filtrar contenedores interesantes
                if info['enlaces'] > 0 or info['imagenes'] > 0:
                    estructuras_detectadas.append(info)
        
        return estructuras_detectadas
    
    def extraer_noticias_principales(self, soup):
        """Extrae noticias principales basado en el análisis de estructura"""
        print("\n📋 EXTRAYENDO NOTICIAS PRINCIPALES...")
        
        noticias = []
        
        # Estrategia 1: Buscar por patrones de clases específicas
        patrones_clases = [
            'noticia', 'news', 'titular', 'headline', 'destacado',
            'nota', 'article', 'post', 'item', 'card'
        ]
        
        for patron in patrones_clases:
            elementos = soup.find_all(class_=lambda x: x and patron in x.lower())
            for elemento in elementos:
                noticia = self._procesar_elemento_noticia(elemento, f"clase_{patron}")
                if noticia:
                    noticias.append(noticia)
        
        # Estrategia 2: Buscar en estructuras jerárquicas
        contenedores_principales = soup.find_all(['main', 'section', 'div'], 
                                               class_=lambda x: x and any(word in x.lower() for word in ['main', 'content', 'principal']))
        
        for contenedor in contenedores_principales:
            # Buscar artículos dentro de contenedores principales
            articulos = contenedor.find_all(['article', 'div'], 
                                          class_=lambda x: x and any(word in x.lower() for word in ['noticia', 'news', 'item']))
            
            for articulo in articulos:
                noticia = self._procesar_elemento_noticia(articulo, "contenedor_principal")
                if noticia:
                    noticias.append(noticia)
        
        # Estrategia 3: Buscar por estructura semántica
        enlaces_con_texto = soup.find_all('a', href=True, string=True)
        for enlace in enlaces_con_texto:
            texto = enlace.get_text().strip()
            if len(texto) > 20 and len(texto) < 200:  # Probable título de noticia
                href = enlace.get('href', '')
                if href and not href.startswith(('javascript:', '#')):
                    noticia = {
                        'titulo': texto,
                        'enlace': href if href.startswith('http') else self.base_url + href,
                        'fuente_deteccion': 'enlace_semantico',
                        'timestamp': datetime.now().isoformat(),
                        'imagen': '',  # Aseguramos que existe la clave
                        'resumen': ''   # Aseguramos que existe la clave
                    }
                    noticias.append(noticia)
        
        return noticias
    
    def _procesar_elemento_noticia(self, elemento, fuente):
        """Procesa un elemento potencial de noticia"""
        try:
            # Extraer título
            titulo_element = elemento.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) or elemento
            titulo = titulo_element.get_text().strip()
            
            if not titulo or len(titulo) < 10:
                return None
            
            # Extraer enlace
            enlace_element = elemento.find('a', href=True)
            enlace = enlace_element.get('href', '') if enlace_element else ''
            if enlace and not enlace.startswith('http'):
                enlace = self.base_url + enlace
            
            # Extraer resumen si existe
            resumen_element = elemento.find(['p', 'span'])
            resumen = resumen_element.get_text().strip() if resumen_element else ''
            
            # Extraer imagen
            imagen_element = elemento.find('img')
            imagen = imagen_element.get('src', '') if imagen_element else ''
            if imagen and not imagen.startswith('http'):
                imagen = self.base_url + imagen
            
            # Estructura consistente para todas las noticias
            return {
                'titulo': titulo,
                'resumen': resumen[:200] + '...' if len(resumen) > 200 else resumen,
                'enlace': enlace,
                'imagen': imagen,
                'fuente_deteccion': fuente,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"⚠️ Error procesando elemento: {e}")
            return None
    
    def limpiar_y_filtrar_noticias(self, noticias):
        """Limpia y filtra las noticias duplicadas"""
        print("\n🧹 LIMPIANDO Y FILTRANDO NOTICIAS...")
        
        # Eliminar duplicados por título y None values
        noticias_limpias = [n for n in noticias if n is not None]
        
        noticias_unicas = {}
        for noticia in noticias_limpias:
            titulo_limpio = re.sub(r'\s+', ' ', noticia['titulo']).strip().lower()
            if titulo_limpio not in noticias_unicas:
                noticias_unicas[titulo_limpio] = noticia
        
        return list(noticias_unicas.values())
    
    def generar_reporte(self, noticias, estructuras):
        """Genera un reporte completo del scraping"""
        print("\n📊 GENERANDO REPORTE COMPLETO...")
        
        # Aseguramos que todas las noticias tengan las claves necesarias
        noticias_consistente = []
        for noticia in noticias:
            noticia_consistente = {
                'titulo': noticia.get('titulo', ''),
                'resumen': noticia.get('resumen', ''),
                'enlace': noticia.get('enlace', ''),
                'imagen': noticia.get('imagen', ''),
                'fuente_deteccion': noticia.get('fuente_deteccion', ''),
                'timestamp': noticia.get('timestamp', '')
            }
            noticias_consistente.append(noticia_consistente)
        
        # Estadísticas seguras
        noticias_con_enlace = sum(1 for n in noticias_consistente if n.get('enlace'))
        noticias_con_imagen = sum(1 for n in noticias_consistente if n.get('imagen'))
        noticias_con_resumen = sum(1 for n in noticias_consistente if n.get('resumen'))
        
        # Fuentes de detección
        fuentes_deteccion = {}
        for noticia in noticias_consistente:
            fuente = noticia.get('fuente_deteccion', 'desconocida')
            fuentes_deteccion[fuente] = fuentes_deteccion.get(fuente, 0) + 1
        
        reporte = {
            'metadata': {
                'fecha_scraping': datetime.now().isoformat(),
                'url_base': self.base_url,
                'total_noticias_extraidas': len(noticias_consistente),
                'total_estructuras_analizadas': len(estructuras)
            },
            'estructuras_detectadas': estructuras[:10],  # Primeras 10
            'noticias_extraidas': noticias_consistente,
            'resumen_estadisticas': {
                'noticias_con_enlace': noticias_con_enlace,
                'noticias_con_imagen': noticias_con_imagen,
                'noticias_con_resumen': noticias_con_resumen,
                'fuentes_deteccion': fuentes_deteccion
            }
        }
        
        return reporte
    
    def guardar_resultados(self, noticias, reporte):
        """Guarda los resultados en diferentes formatos"""
        print("\n💾 GUARDANDO RESULTADOS...")
        
        try:
            # Asegurar estructura consistente para CSV
            noticias_para_csv = []
            for noticia in noticias:
                noticia_csv = {
                    'titulo': noticia.get('titulo', ''),
                    'resumen': noticia.get('resumen', ''),
                    'enlace': noticia.get('enlace', ''),
                    'imagen': noticia.get('imagen', ''),
                    'fuente_deteccion': noticia.get('fuente_deteccion', ''),
                    'timestamp': noticia.get('timestamp', '')
                }
                noticias_para_csv.append(noticia_csv)
            
            # Guardar en CSV
            df = pd.DataFrame(noticias_para_csv)
            df.to_csv('noticias_elperuano.csv', index=False, encoding='utf-8-sig')
            print("✅ CSV guardado: noticias_elperuano.csv")
            
            # Guardar reporte en JSON
            with open('reporte_scraping_elperuano.json', 'w', encoding='utf-8') as f:
                json.dump(reporte, f, ensure_ascii=False, indent=2)
            print("✅ JSON guardado: reporte_scraping_elperuano.json")
            
            # Guardar resumen en texto
            with open('resumen_scraping_elperuano.txt', 'w', encoding='utf-8') as f:
                f.write("RESUMEN DE SCRAPING - EL PERUANO\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total noticias extraídas: {len(noticias)}\n\n")
                
                f.write("NOTICIAS ENCONTRADAS:\n")
                f.write("-" * 30 + "\n")
                for i, noticia in enumerate(noticias[:10], 1):  # Primeras 10
                    f.write(f"{i}. {noticia.get('titulo', 'Sin título')}\n")
                    f.write(f"   Enlace: {noticia.get('enlace', 'Sin enlace')}\n")
                    f.write(f"   Fuente: {noticia.get('fuente_deteccion', 'Desconocida')}\n\n")
            print("✅ TXT guardado: resumen_scraping_elperuano.txt")
            
        except Exception as e:
            print(f"❌ Error guardando archivos: {e}")
    
    def ejecutar_scraping_completo(self):
        """Ejecuta el proceso completo de scraping"""
        print("🎯 INICIANDO SCRAPING COMPLETO DE EL PERUANO")
        print("=" * 60)
        
        try:
            # 1. Obtener página principal
            soup = self.obtener_pagina_principal()
            if not soup:
                print("❌ No se pudo obtener la página principal")
                return None, None
            
            # 2. Análisis de estructura avanzada
            estructuras = self.analizar_estructura_avanzada(soup)
            
            # 3. Extraer noticias
            noticias_brutas = self.extraer_noticias_principales(soup)
            print(f"📥 Noticias brutas encontradas: {len(noticias_brutas)}")
            
            # 4. Limpiar resultados
            noticias_limpias = self.limpiar_y_filtrar_noticias(noticias_brutas)
            print(f"🧼 Noticias después de limpieza: {len(noticias_limpias)}")
            
            # 5. Generar reporte
            reporte = self.generar_reporte(noticias_limpias, estructuras)
            
            # 6. Guardar resultados
            self.guardar_resultados(noticias_limpias, reporte)
            
            # 7. Mostrar resumen en consola
            self.mostrar_resumen_consola(reporte, noticias_limpias)
            
            return noticias_limpias, reporte
            
        except Exception as e:
            print(f"❌ Error en el proceso de scraping: {e}")
            return None, None
    
    def mostrar_resumen_consola(self, reporte, noticias):
        """Muestra un resumen amigable en consola"""
        print("\n" + "=" * 60)
        print("🎉 SCRAPING COMPLETADO EXITOSAMENTE!")
        print("=" * 60)
        
        if not noticias:
            print("❌ No se encontraron noticias")
            return
        
        print(f"\n📈 ESTADÍSTICAS:")
        print(f"   • Noticias extraídas: {reporte['metadata']['total_noticias_extraidas']}")
        print(f"   • Estructuras analizadas: {reporte['metadata']['total_estructuras_analizadas']}")
        print(f"   • Noticias con enlace: {reporte['resumen_estadisticas']['noticias_con_enlace']}")
        print(f"   • Noticias con imagen: {reporte['resumen_estadisticas']['noticias_con_imagen']}")
        
        print(f"\n🔧 FUENTES DE DETECCIÓN:")
        for fuente, cantidad in reporte['resumen_estadisticas']['fuentes_deteccion'].items():
            print(f"   • {fuente}: {cantidad}")
        
        print(f"\n📰 PRIMERAS 5 NOTICIAS ENCONTRADAS:")
        print("-" * 50)
        for i, noticia in enumerate(noticias[:5], 1):
            print(f"{i}. {noticia.get('titulo', 'Sin título')}")
            resumen = noticia.get('resumen', '')
            if resumen:
                print(f"   📝 {resumen[:80]}...")
            print(f"   🔗 {noticia.get('enlace', 'Sin enlace')}")
            print()

# EJECUCIÓN DEL SCRAPING
if __name__ == "__main__":
    # Crear instancia del scraper
    scraper = ScraperElPeruano()
    
    # Ejecutar scraping completo
    noticias, reporte = scraper.ejecutar_scraping_completo()
    
    if noticias:
        print("\n✅ Proceso completado exitosamente! Revisa los archivos generados!")
    else:
        print("\n❌ El proceso no pudo completarse correctamente")