"""Une la Entrega 1 y la Entrega 2 en un solo .docx sin regenerar nada.

Uso:  python unir_entregas.py

- Lee  paper/Proyecto_CMEDriver_Entrega1.docx  (base: se conserva tal cual, incluidas
  las citas de Mendeley Cite) y  paper/Proyecto_CMEDriver_Entrega2.docx.
- Escribe  paper/Proyecto_CMEDriver_Unificado.docx.  No modifica los archivos de origen.

Del documento 1 se conserva todo (portada, contraportada, resumen, introduccion).
Del documento 2 se toma el cuerpo desde "4. Marco Teorico" hasta antes de las referencias.
La lista de referencias se une, sin duplicados, en orden alfabetico.
Solo se cambia el rotulo de la portada y la contraportada ("Entrega 1" -> "Entregas 1 y 2").
Solo usa la libreria estandar de Python.
"""
import os
import re
import sys
import unicodedata
import zipfile
from xml.dom import minidom

AQUI = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.dirname(AQUI)
E1 = os.path.join(PAPER, 'Proyecto_CMEDriver_Entrega1.docx')
E2 = os.path.join(PAPER, 'Proyecto_CMEDriver_Entrega2.docx')
SALIDA = os.path.join(PAPER, 'Proyecto_CMEDriver_Unificado.docx')

T = r'<w:t(?: [^>]*)?>(.*?)</w:t>'
ITEM = r'(<w:p[ >].*?</w:p>|<w:tbl>.*?</w:tbl>|<w:sdt>.*?</w:sdt>|<w:sectPr.*?</w:sectPr>)'


def texto(xml):
    t = ''.join(re.findall(T, xml, flags=re.S))
    return t.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&apos;', "'")


def partir(doc_xml):
    m = re.search(r'(<w:body>)(.*)(</w:body>)', doc_xml, flags=re.S)
    return doc_xml[:m.start(2)], re.findall(ITEM, m.group(2), flags=re.S), doc_xml[m.end(2):]


def indice(items, estilo, rotulo):
    for i, it in enumerate(items):
        if f'w:val="{estilo}"' in it and texto(it).strip() == rotulo:
            return i
    raise SystemExit(f'No se encontro "{rotulo}" ({estilo})')


def clave_ref(p):
    t = texto(p)
    autor = re.split(r',|\. \(', t, maxsplit=1)[0]
    anio = re.search(r'\((\d{4}|s\. f\.)', t)
    return (norm(autor), anio.group(1) if anio else '')


def norm(s):
    s = unicodedata.normalize('NFKD', s.lower())
    return re.sub(r'[^a-z0-9]', '', ''.join(c for c in s if not unicodedata.combining(c)))


def main():
    z1, z2 = zipfile.ZipFile(E1), zipfile.ZipFile(E2)
    d1 = z1.read('word/document.xml').decode('utf-8')
    d2 = z2.read('word/document.xml').decode('utf-8')
    pre1, it1, post1 = partir(d1)
    _, it2, _ = partir(d2)

    # ---- Documento 1: hasta antes de "7. Referencias"
    ref1 = indice(it1, 'Ttulo1', '7. Referencias')
    base = it1[:ref1]
    encabezado_ref = it1[ref1]
    refs1 = [p for p in it1[ref1 + 1:-1] if p.startswith('<w:p')]
    sect_final = it1[-1]
    assert sect_final.startswith('<w:sectPr'), 'el ultimo elemento de la Entrega 1 no es sectPr'

    # ---- Documento 2: desde "4. Marco Teorico" hasta antes de "7. Referencias"
    ini2 = indice(it2, 'Heading1', '4. Marco Teórico')
    ref2 = indice(it2, 'Heading1', '7. Referencias')
    cuerpo2 = it2[ini2:ref2]
    refs2 = [p for p in it2[ref2 + 1:-1] if p.startswith('<w:p')]

    # estilos: los de la Entrega 2 (docx) pasan a los de la Entrega 1 (guardada por Word)
    cuerpo2 = [c.replace('w:val="Heading1"', 'w:val="Ttulo1"').replace('w:val="Heading2"', 'w:val="Ttulo2"') for c in cuerpo2]

    # figura: nueva relacion en el paquete
    rid_viejo = re.search(r'r:embed="(rId\d+)"', ''.join(cuerpo2)).group(1)
    rels2 = z2.read('word/_rels/document.xml.rels').decode('utf-8')
    destino = re.search(r'Id="%s"[^>]*Target="([^"]+)"' % rid_viejo, rels2) or re.search(r'Target="([^"]+)"[^>]*Id="%s"' % rid_viejo, rels2)
    ruta_media = destino.group(1)
    rels1 = z1.read('word/_rels/document.xml.rels').decode('utf-8')
    usados = [int(n) for n in re.findall(r'Id="rId(\d+)"', rels1)]
    rid_nuevo = f'rId{max(usados) + 1}'
    cuerpo2 = [c.replace(f'r:embed="{rid_viejo}"', f'r:embed="{rid_nuevo}"') for c in cuerpo2]
    rels1_nuevo = rels1.replace('</Relationships>',
        f'<Relationship Id="{rid_nuevo}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{ruta_media}"/></Relationships>')

    # ---- Referencias unidas (sin duplicados; se conserva la version de la Entrega 1)
    vistas, refs = {}, []
    for p in refs1 + refs2:
        k = clave_ref(p)
        if k in vistas:
            continue
        vistas[k] = True
        refs.append(p)
    refs.sort(key=lambda p: norm(texto(p)))

    # ---- Rotulo de portada y contraportada
    def rotular(items):
        out = []
        for it in items:
            t = texto(it)
            if t == 'Entrega 1: Resumen e Introducción':
                it = it.replace('Entrega 1: Resumen e Introducción', 'Entregas 1 y 2: Resumen, Introducción, Marco Teórico y Metodología')
            elif t == 'Proyecto (Ingeniería de Software), Entrega 1':
                it = it.replace('Entrega 1', 'Entregas 1 y 2')
            out.append(it)
        return out
    base = rotular(base)
    assert any('Entregas 1 y 2' in texto(i) for i in base), 'no se pudo rotular la portada'

    # Saltos de pagina manuales dentro de la Introduccion (parrafos vacios con solo un salto):
    # dejaban media pagina en blanco y hacian que la Introduccion ocupara una pagina de mas.
    # Se quitan solo aqui; el texto de la Entrega 1 no cambia.
    ini_intro = indice(base, 'Ttulo1', '3. Introducción')
    quitados = 0
    limpio = []
    for i, it in enumerate(base):
        if i > ini_intro and it.startswith('<w:p') and 'w:type="page"' in it and texto(it).strip() == '':
            quitados += 1
            continue
        limpio.append(it)
    base = limpio

    nuevo = pre1 + ''.join(base) + ''.join(cuerpo2) + encabezado_ref + ''.join(refs) + sect_final + post1

    # ---- Validacion de XML antes de escribir
    minidom.parseString(nuevo.encode('utf-8'))
    minidom.parseString(rels1_nuevo.encode('utf-8'))
    ct = z1.read('[Content_Types].xml').decode('utf-8')
    if 'Extension="png"' not in ct:
        ct = ct.replace('<Default ', '<Default Extension="png" ContentType="image/png"/><Default ', 1)
    minidom.parseString(ct.encode('utf-8'))

    # ---- Escribir paquete
    with zipfile.ZipFile(SALIDA, 'w', zipfile.ZIP_DEFLATED) as out:
        for info in z1.infolist():
            datos = z1.read(info.filename)
            if info.filename == 'word/document.xml':
                datos = nuevo.encode('utf-8')
            elif info.filename == 'word/_rels/document.xml.rels':
                datos = rels1_nuevo.encode('utf-8')
            elif info.filename == '[Content_Types].xml':
                datos = ct.encode('utf-8')
            out.writestr(info, datos)
        out.writestr('word/' + ruta_media, z2.read('word/' + ruta_media))

    print('OK', SALIDA)
    print(f'  Entrega 1 conservada: {len(base)} elementos | Entrega 2 agregada: {len(cuerpo2)} elementos')
    print(f'  Saltos de pagina manuales quitados de la Introduccion: {quitados}')
    print(f'  Referencias: {len(refs1)} + {len(refs2)} -> {len(refs)} unicas')
    print('  Figura:', ruta_media, '->', rid_nuevo)


if __name__ == '__main__':
    sys.exit(main())
