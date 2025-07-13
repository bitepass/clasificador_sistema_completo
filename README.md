# OSINT-Nexus

OSINT-Nexus es una aplicación web modular que automatiza la recolección, correlación y visualización de inteligencia de fuentes abiertas (OSINT).

## Características clave

* Interfaz web en Streamlit muy simple: seleccione el tipo de objetivo, introduzca el dato y haga clic en «Iniciar investigación».
* Arquitectura modular. Cada tipo de objetivo tiene su propio módulo (`domain`, `email`, `username`, `social`).
* Integración sencilla de APIs externas mediante el gestor de API-keys.
* Generación de informe descargable en PDF.
* Visualización gráfica de relaciones básica con NetworkX (placeholder).
* Marco ético incorporado: recordatorio de uso responsable y restricción a fuentes públicas.

## Instalación rápida

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Cree un archivo `.env` en la raíz del proyecto con sus claves de API, por ejemplo:

```
SHODAN_API_KEY=xxxxx
HIBP_API_KEY=yyyyy
```

## Uso

```bash
streamlit run osint_nexus/main.py
```

La aplicación se abrirá en su navegador por defecto.

## Añadir nuevas claves de API

Abra la barra lateral de la aplicación y complete los campos en «Configuración de APIs». Las claves se almacenan solo en la sesión local de Streamlit.

## Añadir un nuevo módulo

1. Cree un archivo en `osint_nexus/modules/` siguiendo la plantilla de los módulos existentes.
2. Implemente una función `run(target: str, api_manager: APIManager) -> dict` que devuelva un diccionario serializable con los hallazgos.
3. Añada el módulo al diccionario `MODULE_REGISTRY` en `main.py`.

## Consideraciones éticas y legales

El proyecto fue diseñado bajo el principio «Privacy by Design» y solo realiza consultas a fuentes de acceso público. 
No debe emplearse para hostigar, discriminar, difundir desinformación ni realizar intrusiones. El usuario es el único responsable del uso que haga de la herramienta.

## Visualización de grafos

A partir de los hallazgos, la aplicación genera un grafo con NetworkX y Matplotlib para representar las relaciones entre entidades.

## Ejecutar con Docker (recomendado para OPSEC)

```bash
docker build -t osint-nexus .
docker run -p 8501:8501 --rm osint-nexus
```

Puede añadir proxies, VPN u otras configuraciones de red al contenedor para mejorar la OPSEC.

---
**Autor**: Prompt generado por ChatGPT-4 asistiendo a un investigador OSINT.