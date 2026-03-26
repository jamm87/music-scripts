import os
import json
import urllib.request
import time
from mutagen.easyid3 import EasyID3

# --- CONFIGURACIÓN ---
DIRECTORIO_RAIZ = '[RUTA DE LA CARPETA]' # Pon tu ruta real aquí
API_KEY = '[API de GEMINI]' # Pon tu API real aquí
API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}'
EXTENSIONES_VALIDAS = {'.mp3', '.wav', '.flac', '.m4a', '.ogg', '.aac'}

def obtener_tags_crudos(ruta_completa):
    """Extrae lo que haya en los metadatos sin filtrar nada."""
    try:
        if ruta_completa.lower().endswith('.mp3'):
            audio = EasyID3(ruta_completa)
            artista = audio.get('artist', [''])[0]
            titulo = audio.get('title', [''])[0]
            if artista and titulo:
                return f"{artista} - {titulo}"
    except:
        pass
    return "No hay metadatos"

def preguntar_a_gemini_maestro(nombre_archivo, metadatos_crudos):
    """La IA recibe ambas fuentes y decide el nombre y formato correcto."""
    prompt = f"""Actúa como un experto en ordenación de bibliotecas musicales.
    Datos:
    - Archivo: "{nombre_archivo}"
    - ID3: "{metadatos_crudos}"

    TAREA: Extrae el Artista y la Canción.
    
    REGLAS DE ORO:
    1. FORMATO OBLIGATORIO: "Artista - Canción". 
    2. CAPITALIZACIÓN: Usa 'Title Case'. Ejemplo: "ARTIST - track name" DEBE ser "Artist - Track Name". No dejes todo en mayúsculas ni todo en minúsculas.
    3. LIMPIEZA: Borra direcciones web, dominios (.tk, .com, .org, www), trackers o basura de foros.
    4. PRECISIÓN: Si los metadatos son basura pero el nombre de archivo tiene información, usa el nombre.
    5. Si tienes dudas o ambos datos son ilegibles, devuelve: REVISAR.
    
    Responde SOLO con el nombre corregido, sin comillas."""

    data = {"contents": [{"parts": [{"text": prompt}]}]}
    req = urllib.request.Request(API_URL, method="POST")
    req.add_header('Content-Type', 'application/json')
    
    try:
        respuesta = urllib.request.urlopen(req, data=json.dumps(data).encode('utf-8'))
        res_json = json.loads(respuesta.read().decode('utf-8'))
        if 'candidates' in res_json:
            # Limpieza extra por si la IA añade espacios locos
            resultado = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
            return resultado
    except Exception as e:
        print(f"  [!] Error de API: {e}")
    return None

def procesar_biblioteca():
    print(f"--- Iniciando Sistema de Doble Verificación ---")
    
    for root, dirs, files in os.walk(DIRECTORIO_RAIZ):
        for filename in files:
            if filename.startswith("REVISAR"): continue
            nombre_sin_ext, extension = os.path.splitext(filename)
            extension = extension.lower()
            if extension not in EXTENSIONES_VALIDAS: continue

            ruta_completa = os.path.join(root, filename)
            
            # Obtener metadatos aunque sean malos
            tags = obtener_tags_crudos(ruta_completa)
            
            print(f"  [*] Procesando: {filename}")
            # La IA decide comparando nombre vs metadatos
            res_ia = preguntar_a_gemini_maestro(nombre_sin_ext, tags)
            
            if res_ia:
                if res_ia.upper() == "REVISAR":
                    nuevo_nombre_base = f"REVISAR {nombre_sin_ext}"
                else:
                    nuevo_nombre_base = res_ia
                
                # Limpiar caracteres prohibidos en macOS
                nuevo_nombre_base = nuevo_nombre_base.replace('/', '-').replace(':', '-')
                nuevo_nombre_final = f"{nuevo_nombre_base}{extension}"
                
                if nuevo_nombre_final != filename:
                    ruta_nueva = os.path.join(root, nuevo_nombre_final)
                    try:
                        os.rename(ruta_completa, ruta_nueva)
                        print(f"    [OK] -> {nuevo_nombre_final}")
                    except Exception as e:
                        print(f"    [!] Error: {e}")
                else:
                    print(f"    [=] Ya está correcto.")
            
            time.sleep(1.2) # Respetar cuota de API

if __name__ == "__main__":
    procesar_biblioteca()
