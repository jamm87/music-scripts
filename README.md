# Script de Renombrado Automático de Archivos de Música

Este script utiliza inteligencia artificial (Gemini) para renombrar archivos de música automáticamente, corrigiendo nombres mal formateados y aplicando un estándar consistente.

## ¿Qué hace?

El script analiza tus archivos de música y los renombra al formato:
- **Artista - Canción** (con capitalización correcta)

Por ejemplo:
- `track_001.mp3` → `Artist Name - Song Title.mp3`
- `"ARTIST - track name"` → `"Artist - Track Name"`

También limpia información basura como URLs, dominios y trackers de los nombres.

---

## Instalación

### 1. Abre la carpeta del proyecto en Visual Studio Code

```bash
# En terminal, navega a la carpeta raíz del proyecto
cd ruta/a/tu/proyecto

# Abre con VS Code
code .
```

### 2. Crea un entorno virtual de Python

Esto es importante para evitar conflictos con otras librerías:

```bash
python3 -m venv .venv
```

### 3. Activa el entorno virtual

```bash
# En macOS/Linux
source .venv/bin/activate

# Verás que el prompt cambia a algo como: (.venv) $
```

### 4. Instala las dependencias necesarias

```bash
pip install mutagen
```

Esto instala la librería `mutagen`, que lee los metadatos (ID3) de archivos MP3.

### 5. Configura tu API Key de Gemini

El script necesita acceso a la API de Google Gemini para funcionar:

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. **[RECOMENDADO] Configura un plan de pago** para evitar limitaciones:
   - Las API Keys gratuitas tienen límites muy restrictivos (~15 solicitudes/minuto)
   - Con un plan de pago, obtendrás mejor rendimiento y mayor límite de solicitudes
   - Es la opción recomendada si tienes una biblioteca grande de música
3. Crea una API Key (o usa la del plan gratuito si prefieres)
4. Abre `renombrar.py` en el editor
5. Encuentra esta línea (línea 9):
   ```python
   API_KEY = '[API de GEMINI]'
   ```
6. Reemplaza la clave con la tuya

---

## Cómo usar

### Opción 1: Renombrar todos los archivos de la carpeta Temas

```bash
# Asegúrate de que el entorno virtual está activado
source .venv/bin/activate

# Ejecuta el script
python renombrar.py
```

El script:
- Recorre toda la carpeta `Temas/` recursivamente
- Analiza cada archivo de música (MP3, WAV, FLAC, M4A, OGG, AAC)
- Lo renombra automáticamente
- Muestra el progreso en terminal

### Opción 2: Renombrar una carpeta específica

Si quieres personalizar qué carpeta procesar, edita la línea 7 en `renombrar.py`:

```python
DIRECTORIO_RAIZ = '/ruta/a/tu/carpeta'  # Cambia esto
```

Ejemplo:
```python
DIRECTORIO_RAIZ = '/ruta/completa/Discos, temas y generos'
```

---

## Archivos soportados

El script trabaja con estos formatos:
- `.mp3`
- `.wav`
- `.flac`
- `.m4a`
- `.ogg`
- `.aac`

---

## ¿Qué son los archivos "REVISAR"?

Si el script no puede decidir con certeza cómo renombrar un archivo (por falta de metadatos claros), lo renombra como:

```
REVISAR nombre_original.mp3
```

**Qué hacer:**
1. Abre estos archivos manualmente
2. Escucha para saber quién es el artista y cuál es el título
3. Renómbralos correctamente a mano: `Artista - Canción.mp3`

---

## Estructura de carpetas

```
ruta/a/tu/carpeta/
├── README.md (este archivo)
├── renombrar.py (el script)
├── .venv/ (entorno virtual, se crea al instalar)
├── Temas/ (carpeta de música a renombrar)
└── ...
```

---

## Solucionar problemas

### "Comando no encontrado: python3"
Instala Python desde [python.org](https://www.python.org)

### "No module named 'mutagen'"
Asegúrate de haber ejecutado:
```bash
source .venv/bin/activate
pip install mutagen
```

### "API key inválida"
1. Revisa que hayas reemplazado la clave correctamente en `renombrar.py`
2. Verifica que la clave sea válida en [Google AI Studio](https://aistudio.google.com/apikey)
3. Comprueba que tienes conexión a internet

### El script va muy lento
Es normal. El script espera 1.2 segundos entre llamadas a la API para respetar los límites de uso. Esto protege tu cuenta.

---

## Contacto / Soporte

Si tienes problemas o dudas, revisa que:
1. ✅ Python 3 esté instalado
2. ✅ El entorno virtual esté activado
3. ✅ Hayas instalado mutagen: `pip install mutagen`
4. ✅ Tu API Key de Gemini sea válida
5. ✅ Tengas conexión a internet

---

**Última actualización:** Marzo 2026
