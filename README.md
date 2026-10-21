# visenda-mapas

Mapas y datos de rutas offline por región de Chile para [Visenda](https://trello.com/b/AAhJ7hXT/visenda), una app Android para visitadores en terreno que funciona sin internet.

Este repositorio no contiene datos de clientes ni código de la app: solo genera y publica datos geográficos públicos.

## Qué se publica

Cada [Release](../../releases) trae, por cada una de las 16 regiones:

| Archivo | Contenido | Para qué |
|---|---|---|
| `<region>-rutas.tar` | Teselas de [Valhalla](https://github.com/valhalla/valhalla) 3.9.1 | Calcular rutas y tiempos de viaje sin conexión |
| `<region>-mapa.pmtiles` | Mapa base de [Protomaps](https://protomaps.com) | Dibujar el mapa sin conexión |

Además, `indice.json` lista las regiones con el tamaño y el SHA-256 de cada archivo; la app lo usa para verificar las descargas. El último índice siempre está en:

```
https://github.com/Jose94D/visenda-mapas/releases/latest/download/indice.json
```

Las rutas de todas las regiones salen de un mismo build nacional, así que las teselas de borde coinciden y las rutas cruzan de una región a otra sin cortes.

## Cómo se generan

El flujo [Publicar mapas y rutas](.github/workflows/publicar.yml) se lanza a mano desde la pestaña **Actions**:

1. Descarga OpenStreetMap de Chile desde [Geofabrik](https://download.geofabrik.de/south-america/chile.html).
2. Construye las teselas de Valhalla de todo el país y las corta por región ([`cortar_regiones.py`](herramientas/cortar_regiones.py)).
3. Extrae el mapa de cada región del build diario de Protomaps.
4. Arma `indice.json` ([`indice.py`](herramientas/indice.py)) y publica un Release nuevo.

Los límites de cada región están en [`regiones.json`](herramientas/regiones.json): rectángulos aproximados de la parte continental, con margen y solapados entre regiones vecinas. No incluyen Isla de Pascua, Juan Fernández ni el Territorio Antártico.

## Licencia y atribución

Los datos publicados derivan de OpenStreetMap:

**© colaboradores de [OpenStreetMap](https://www.openstreetmap.org/copyright)**, disponibles bajo la [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/). Cualquier uso de estos archivos debe mantener esta atribución, y las bases de datos derivadas se comparten bajo la misma licencia.

El mapa base usa el esquema de [Protomaps Basemaps](https://github.com/protomaps/basemaps).
