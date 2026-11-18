#!/usr/bin/env python3
"""Construye la presentacion de CMEDriver a partir de plantilla.html.

Uso:
    python presentacion/construir.py                      # usa datos/indicadores.json
    python presentacion/construir.py --datos datos/ejemplo-indicadores.json

Genera, dentro de presentacion/:
    index.html            documento completo (abre con doble clic, sin internet)
    index.artifact.html   fragmento (title + meta + style + contenido + script) para publicar como Artifact

Inserta en la plantilla:
    {{datos:indicadores}}  -> contenido de datos/indicadores.json (o `null` si no existe)
    {{datos:proyecto}}     -> contenido de datos/proyecto.json
    {{captura:nombre.png}} -> imagen de capturas/nombre.png como data URI
                              (si falta, la lamina muestra un recuadro "captura pendiente")

Solo usa la libreria estandar. Si Pillow esta disponible (por ejemplo en backend/.venv)
reduce las capturas a 1600 px de ancho como maximo; no es obligatorio.
"""
import argparse
import base64
import io
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
LIMITE_FRAGMENTO = 14 * 1024 * 1024
ANCHO_MAX = 1600
UMBRAL_WEBP = 350 * 1024  # una captura PNG mayor que esto se recodifica a WebP si ahorra al menos 30 %
CLAVES_INDICADORES = (
    "generado_en", "periodo", "resumen", "por_estado", "serie_diaria", "por_zona",
    "novedades", "evidencia", "motorizados", "operacion", "integraciones",
)

try:  # salida legible en consolas de Windows
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def aviso(texto):
    print("AVISO: " + texto, file=sys.stderr)


def error(texto, codigo=1):
    print("ERROR: " + texto, file=sys.stderr)
    sys.exit(codigo)


def tamano(n):
    return f"{n / 1024 / 1024:.2f} MB" if n >= 1024 * 1024 else f"{n / 1024:.1f} KB"


def cargar_pillow():
    """Devuelve el modulo Image de Pillow o None. Prueba tambien backend/.venv."""
    try:
        from PIL import Image  # type: ignore
        return Image
    except Exception:
        pass
    candidatos = [RAIZ / "backend" / ".venv" / "Lib" / "site-packages"]
    candidatos += sorted((RAIZ / "backend" / ".venv" / "lib").glob("python*/site-packages"))
    for c in candidatos:
        if c.is_dir():
            sys.path.append(str(c))
            try:
                from PIL import Image  # type: ignore
                return Image
            except Exception:
                sys.path.remove(str(c))
    return None


def leer_json(ruta, etiqueta):
    """Lee un JSON. Devuelve None si el archivo no existe; falla si esta corrupto."""
    ruta = Path(ruta)
    if not ruta.is_file():
        return None
    try:
        return json.loads(ruta.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as e:
        error(f"{etiqueta} ({ruta}) no es JSON valido: {e}", 2)


def json_para_script(obj):
    """Serializa para incrustar dentro de <script type="application/json">."""
    texto = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return (texto.replace("</", "<\\/").replace("<!--", "<\\!--")
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def reducir(datos, nombre, Image, forzar_webp):
    """Devuelve (bytes, mime). Limita el ancho y comprime; sin Pillow, deja el PNG tal cual."""
    if Image is None:
        return datos, "image/png"
    try:
        img = Image.open(io.BytesIO(datos))
        img.load()
    except Exception as e:  # imagen ilegible: se incrusta sin tocar
        aviso(f"{nombre}: no se pudo abrir con Pillow ({e}); se incrusta sin cambios.")
        return datos, "image/png"
    cambiada = False
    if img.width > ANCHO_MAX:
        alto = round(img.height * ANCHO_MAX / img.width)
        img = img.resize((ANCHO_MAX, alto), Image.LANCZOS)
        cambiada = True
    if forzar_webp:
        buf = io.BytesIO()
        img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB").save(buf, "WEBP", quality=88, method=6)
        return buf.getvalue(), "image/webp"
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    optimizado = buf.getvalue()
    mejor, mime = (optimizado, "image/png") if (cambiada or len(optimizado) < len(datos)) else (datos, "image/png")
    if len(mejor) > UMBRAL_WEBP:  # capturas pesadas (mapas): WebP casi sin perdida visible
        w = io.BytesIO()
        img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB").save(w, "WEBP", quality=88, method=6)
        if len(w.getvalue()) < len(mejor) * 0.7:
            return w.getvalue(), "image/webp"
    return mejor, mime


def construir(args):
    plantilla_ruta = AQUI / "plantilla.html"
    if not plantilla_ruta.is_file():
        error(f"No existe {plantilla_ruta}")
    plantilla = plantilla_ruta.read_text(encoding="utf-8")

    # --- datos ---------------------------------------------------------
    ruta_ind = Path(args.datos) if args.datos else AQUI / "datos" / "indicadores.json"
    if not ruta_ind.is_absolute() and not ruta_ind.is_file() and (AQUI / ruta_ind).is_file():
        ruta_ind = AQUI / ruta_ind
    indicadores = leer_json(ruta_ind, "Indicadores")
    if indicadores is None:
        aviso(f"No existe {ruta_ind}. La presentacion mostrara el estado 'sin datos' en las laminas de indicadores.")
        aviso("Para generarlo: python backend/manage.py exportar_indicadores --salida presentacion/datos/indicadores.json")
    else:
        faltan = [k for k in CLAVES_INDICADORES if k not in indicadores]
        if faltan:
            aviso("El JSON de indicadores no trae estas claves del contrato: " + ", ".join(faltan))
        print(f"Indicadores: {ruta_ind} (generado_en: {indicadores.get('generado_en', 'sin dato')})")

    ruta_pro = Path(args.proyecto) if args.proyecto else AQUI / "datos" / "proyecto.json"
    proyecto = leer_json(ruta_pro, "Datos del proyecto")
    if proyecto is None:
        aviso(f"No existe {ruta_pro}. Las cifras del proyecto mostraran un guion.")
    else:
        print(f"Proyecto: {ruta_pro}")

    html = plantilla
    for marcador, obj in (("{{datos:indicadores}}", indicadores), ("{{datos:proyecto}}", proyecto)):
        if marcador not in html:
            aviso(f"La plantilla no contiene {marcador}.")
        html = html.replace(marcador, json_para_script(obj))

    # --- capturas ------------------------------------------------------
    carpeta_cap = Path(args.capturas) if args.capturas else AQUI / "capturas"
    Image = None if args.sin_reducir else cargar_pillow()
    if Image is None and not args.sin_reducir:
        print("Pillow no disponible: las capturas se incrustan sin reducir.")
    nombres = sorted(set(re.findall(r"\{\{captura:([^}]+)\}\}", html)))
    uris = {}
    faltantes = []

    def preparar(forzar_webp):
        uris.clear()
        for nombre in nombres:
            ruta = carpeta_cap / nombre.strip()
            if not ruta.is_file():
                continue
            crudo = ruta.read_bytes()
            datos, mime = reducir(crudo, nombre, Image, forzar_webp)
            uris[nombre] = f"data:{mime};base64,{base64.b64encode(datos).decode('ascii')}"
            print(f"Captura {nombre}: {tamano(len(crudo))} -> {tamano(len(datos))} ({mime.split('/')[1]})")

    def aplicar(fuente):
        def img(m):
            etiqueta = m.group(0)
            nombre = m.group(1).strip()
            if nombre in uris:
                return etiqueta.replace("{{captura:" + m.group(1) + "}}", uris[nombre])
            if nombre not in faltantes:
                faltantes.append(nombre)
            alt = re.search(r'alt="([^"]*)"', etiqueta)
            texto = alt.group(1) if alt else nombre
            return ('<div class="captura-pendiente" role="img" aria-label="Captura pendiente: ' + texto +
                    '" data-captura="' + nombre + '"><b>Captura pendiente</b><span>' + nombre + "</span></div>")
        salida = re.sub(r"<img\b[^>]*\{\{captura:([^}]+)\}\}[^>]*>", img, fuente, flags=re.I)
        # marcadores fuera de <img> (por ejemplo en CSS)
        return re.sub(r"\{\{captura:([^}]+)\}\}", lambda m: uris.get(m.group(1).strip(), ""), salida)

    preparar(args.webp)
    fragmento = aplicar(html)
    if len(fragmento.encode("utf-8")) > LIMITE_FRAGMENTO and not args.webp:
        if Image is None:
            error(f"El fragmento supera {tamano(LIMITE_FRAGMENTO)} y no hay Pillow para reducir las capturas.")
        aviso("El fragmento supera el limite; se recodifican las capturas a WebP.")
        preparar(True)
        fragmento = aplicar(html)
    for nombre in faltantes:
        aviso(f"Falta la captura capturas/{nombre}: la lamina mostrara 'captura pendiente'.")
    if re.search(r"\{\{[a-z]+:[^}]*\}\}", fragmento):
        aviso("Quedan marcadores {{...}} sin resolver en la salida.")

    # --- salida --------------------------------------------------------
    documento = (
        "<!doctype html>\n"
        '<html lang="es">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        "</head>\n<body>\n" + fragmento + "\n</body>\n</html>\n"
    )
    (AQUI / "index.artifact.html").write_text(fragmento if fragmento.endswith("\n") else fragmento + "\n", encoding="utf-8", newline="\n")
    (AQUI / "index.html").write_text(documento, encoding="utf-8", newline="\n")

    n_frag = (AQUI / "index.artifact.html").stat().st_size
    n_doc = (AQUI / "index.html").stat().st_size
    print("-" * 60)
    print(f"index.html            {tamano(n_doc)}")
    print(f"index.artifact.html   {tamano(n_frag)}  (limite {tamano(LIMITE_FRAGMENTO)})")
    print(f"Capturas incrustadas: {len(uris)} de {len(nombres)}")
    if n_frag > LIMITE_FRAGMENTO:
        error("El fragmento supera el limite de 14 MB.")


def main():
    ap = argparse.ArgumentParser(description="Construye la presentacion de CMEDriver (index.html e index.artifact.html).")
    ap.add_argument("--datos", help="ruta del JSON de indicadores (por defecto datos/indicadores.json)")
    ap.add_argument("--proyecto", help="ruta del JSON del proyecto (por defecto datos/proyecto.json)")
    ap.add_argument("--capturas", help="carpeta de capturas (por defecto capturas/)")
    ap.add_argument("--sin-reducir", action="store_true", help="no usar Pillow aunque este disponible")
    ap.add_argument("--webp", action="store_true", help="recodificar las capturas a WebP (mas livianas)")
    construir(ap.parse_args())


if __name__ == "__main__":
    main()
