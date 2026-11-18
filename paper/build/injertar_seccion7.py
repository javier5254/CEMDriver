"""Injerta las secciones 7 (Cronograma del proyecto) y 8 (Presupuesto del proyecto) en una copia del Final.

Uso:
    node build_seccion7.js                                   # genera build/_tmp/seccion7.docx
    python injertar_seccion7.py ENTRADA.docx SALIDA.docx     # nunca sobrescribe ENTRADA
    python injertar_seccion7.py ENTRADA.docx SALIDA.docx --sin-medir   # omite la medicion con Word

- (a) inserta el cuerpo de seccion7.docx inmediatamente antes del titulo "7. Referencias", sin tocar
      los campos de Mendeley (solo se edita XML; nada se regenera desde markdown);
- (b) renumera "7. Referencias" a "9. Referencias";
- (c) mide con Word COM (medir_paginas.ps1). Si el contenido (Resumen hasta la seccion 8) pasa de 25 paginas,
      reduce las figuras de la seccion 6 (wp:extent y a:ext) un 15 %, 25 %, 35 %... del tamano original,
      hasta cumplir o llegar al 50 %; informa si no alcanza;
- (d) amplia la frase de 3.6 "Organizacion del documento" con las secciones 7 y 8.
Solo usa la libreria estandar. Es seguro ejecutarlo sobre la version actual del estudiante (parte de ENTRADA).
"""
import os
import re
import subprocess
import sys
import time
import zipfile
from xml.dom import minidom

AQUI = os.path.dirname(os.path.abspath(__file__))
SEC7 = os.path.join(AQUI, '_tmp', 'seccion7.docx')
MEDIR = os.path.join(AQUI, 'medir_paginas.ps1')
LIMITE = 25

T = r'<w:t(?: [^>]*)?>([^<]*)</w:t>'
ITEM = r'(<w:p[ >].*?</w:p>|<w:tbl>.*?</w:tbl>|<w:sdt>.*?</w:sdt>|<w:sectPr.*?</w:sectPr>)'


def texto(xml):
    return ''.join(re.findall(T, xml, flags=re.S)).replace('&amp;', '&')


def partir(doc):
    m = re.search(r'(<w:body>)(.*)(</w:body>)', doc, flags=re.S)
    return doc[:m.start(2)], re.findall(ITEM, m.group(2), flags=re.S), doc[m.end(2):]


def titulo1(it):
    return it.startswith('<w:p') and 'w:val="Ttulo1"' in it


def escalar_figuras(items, desde, hasta, f):
    """Escala (factor f sobre el tamano ORIGINAL guardado en items0) las imagenes de items[desde:hasta]."""
    n = 0
    for k in range(desde, hasta):
        it = items[k]
        if '<w:drawing>' not in it:
            continue

        def esc(m):
            return f'{m.group(1)}cx="{round(int(m.group(2)) * f)}" cy="{round(int(m.group(3)) * f)}"'
        nuevo = re.sub(r'(<wp:extent )cx="(\d+)" cy="(\d+)"', esc, it)
        nuevo = re.sub(r'(<a:ext )cx="(\d+)" cy="(\d+)"', esc, nuevo)
        if nuevo != it:
            n += it.count('<wp:extent ')
        items[k] = nuevo
    return n


def escribir(zf, ruta, nuevo_doc):
    # zf: lista (info, datos) leida una sola vez
    minidom.parseString(nuevo_doc.encode('utf-8'))
    tmp = ruta + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as out:
        for info, datos in zf:
            if info.filename == 'word/document.xml':
                datos = nuevo_doc.encode('utf-8')
            out.writestr(info, datos)
    for intento in range(20):
        try:
            os.replace(tmp, ruta)
            break
        except PermissionError:
            time.sleep(1.5)  # Word aun libera el archivo tras medir
    else:
        raise


def medir(ruta):
    r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', MEDIR, '-Ruta', ruta],
                       capture_output=True, timeout=600)
    salida = (r.stdout or b'').decode('cp1252', errors='replace')
    lineas = [l for l in salida.splitlines() if re.search(r'paginas (\d+)-(\d+)', l)]
    rangos = [tuple(map(int, re.search(r'paginas (\d+)-(\d+)', l).groups())) for l in lineas]
    if len(rangos) < 3:
        raise RuntimeError('medicion fallida:\n' + salida + (r.stderr or b'').decode('cp1252', errors='replace'))
    # primer titulo = Resumen; el ultimo = Referencias; el penultimo = seccion 8
    return rangos[0][0], rangos[-2][1], salida


def main(entrada, salida, con_medicion=True):
    if os.path.abspath(entrada) == os.path.abspath(salida):
        sys.exit('ENTRADA y SALIDA deben ser distintas')
    zin = zipfile.ZipFile(entrada)
    zf = [(i, zin.read(i.filename)) for i in zin.infolist()]
    zin.close()
    z7 = zipfile.ZipFile(SEC7)
    doc = next(d for i, d in zf if i.filename == 'word/document.xml').decode('utf-8')
    campos0 = len(re.findall(r'MENDELEY_CITATION_v3_', doc))
    pre, items, post = partir(doc)

    # ---- cuerpo de las secciones 7 y 8 (docx-js) -> estilos del Final
    _, it7, _ = partir(z7.read('word/document.xml').decode('utf-8'))
    assert it7[-1].startswith('<w:sectPr')
    cuerpo = []
    for c in it7[:-1]:
        c = c.replace('w:val="Heading1"', 'w:val="Ttulo1"').replace('w:val="Heading2"', 'w:val="Ttulo2"')
        c = c.replace('<w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/>', '')
        c = c.replace('<w:sz w:val="22"/><w:szCs w:val="22"/>', '')
        c = c.replace('<w:rPr></w:rPr>', '')
        cuerpo.append(c)
    assert not re.search(r'<w:drawing>|r:embed', ''.join(cuerpo)), 'el cuerpo no debe tener imagenes'

    # ---- (b) referencias
    ref = next(i for i, it in enumerate(items) if titulo1(it) and texto(it).strip() == '7. Referencias')
    assert '7. Referencias' in items[ref]
    items[ref] = items[ref].replace('7. Referencias', '9. Referencias')

    # ---- (d) frase de 3.6
    cambios = 0
    for i, it in enumerate(items):
        if not it.startswith('<w:p') or 'cierran el documento las referencias;' not in it and 'Cierran las referencias;' not in it:
            continue
        if 'cierran el documento las referencias;' in it:
            items[i] = it.replace(', y cierran el documento las referencias;',
                                  '; el cronograma y el presupuesto se presentan en las secciones 7 y 8, y cierran el documento las referencias (sección 9);')
        else:
            items[i] = it.replace('Cierran las referencias;',
                                  'El cronograma y el presupuesto se presentan en las secciones 7 y 8, y cierran el documento las referencias (sección 9);')
        cambios += items[i] != it
    print('  frase de 3.6 actualizada:', cambios)
    if cambios != 1:
        print('  AVISO: no se encontro la frase esperada en 3.6; revisar a mano')

    # ---- (a) insercion
    n_cuerpo = len(cuerpo)
    items[ref:ref] = cuerpo
    ini6 = next((i for i, it in enumerate(items) if titulo1(it) and texto(it).strip().startswith('6. ')), None)
    fin6 = ref  # primer elemento de la seccion 7
    original = list(items)

    def doc_con(f):
        its = list(original)
        if f < 1.0 and ini6 is not None:
            escalar_figuras(its, ini6, fin6, f)
        return pre + ''.join(its) + post

    escribir(zf, salida, doc_con(1.0))
    campos = len(re.findall(r'MENDELEY_CITATION_v3_', doc_con(1.0)))
    print(f'OK {salida}: {n_cuerpo} elementos insertados; campos de cita {campos0} -> {campos}')
    assert campos == campos0

    if not con_medicion:
        return
    # ---- (c) medicion y reduccion de figuras
    mejor = None
    for f in (1.0, 0.85, 0.75, 0.65, 0.55, 0.50):
        if f < 1.0:
            escribir(zf, salida, doc_con(f))
        ini, fin, bruto = medir(salida)
        paginas = fin - ini + 1
        print(f'  figuras de la seccion 6 al {round(f * 100)} %: contenido (resumen a seccion 8) = {paginas} paginas (pag. {ini} a {fin})')
        if mejor is None or paginas < mejor[0]:
            mejor = (paginas, f)
        if paginas <= LIMITE:
            print('  CUMPLE el limite de', LIMITE, 'paginas')
            return
    # no se alcanza: deja la reduccion minima que logra el menor numero de paginas
    escribir(zf, salida, doc_con(mejor[1]))
    print(f'  NO se alcanza el limite de {LIMITE} paginas solo con las figuras; queda en {mejor[0]} paginas con las figuras al {round(mejor[1] * 100)} %')

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 2:
        sys.exit(__doc__)
    main(args[0], args[1], '--sin-medir' not in sys.argv)
