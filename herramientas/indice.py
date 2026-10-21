"""Arma indice.json: qué regiones hay en este Release, con tamaño y SHA-256 de cada archivo.

La app lo lee para mostrar los tamaños y verificar que cada descarga llegó completa e intacta.

Uso: python indice.py <regiones.json> <dir_salida> <fecha AAAA-MM-DD>
"""
import hashlib
import json
import sys
from pathlib import Path

VERSION = 1  # subir si cambia el formato; la app rechaza versiones que no conoce


def archivo(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return {"archivo": ruta.name, "bytes": ruta.stat().st_size, "sha256": h.hexdigest()}


def indice(regiones, dir_salida, fecha):
    salida = {"version": VERSION, "fecha": fecha, "regiones": {}}
    for clave, region in regiones.items():
        if clave.startswith("_"):
            continue
        rutas, mapa = dir_salida / f"{clave}-rutas.tar", dir_salida / f"{clave}-mapa.pmtiles"
        if not (rutas.exists() and mapa.exists()):
            sys.exit(f"Falta un archivo de {clave}: no se publica un índice incompleto")
        salida["regiones"][clave] = {"nombre": region["nombre"], "rect": region["rect"], "rutas": archivo(rutas), "mapa": archivo(mapa)}
    return salida


def autoprueba():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "x-rutas.tar").write_bytes(b"abc")
        (d / "x-mapa.pmtiles").write_bytes(b"")
        i = indice({"_nota": "", "x": {"nombre": "X", "rect": [0, 0, 1, 1]}}, d, "2026-10-21")
        assert i["regiones"]["x"]["rutas"] == {"archivo": "x-rutas.tar", "bytes": 3,
                                               "sha256": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"}
        assert i["regiones"]["x"]["mapa"]["bytes"] == 0 and i["version"] == VERSION


if __name__ == "__main__":
    autoprueba()
    if len(sys.argv) == 4:
        datos = indice(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")), Path(sys.argv[2]), sys.argv[3])
        (Path(sys.argv[2]) / "indice.json").write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"indice.json: {len(datos['regiones'])} regiones")
    else:
        print("autoprueba OK. Uso: python indice.py <regiones.json> <dir_salida> <fecha>")
