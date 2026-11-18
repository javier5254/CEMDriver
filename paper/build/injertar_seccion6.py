"""Injerta la seccion 6 (Avance de Resultados) en Proyecto_CMEDriver_Final.docx editando su XML.

Uso:
    node build_seccion6.js                  # genera build/_tmp/seccion6.docx (solo la seccion 6)
    python injertar_seccion6.py             # lee _respaldo/Final_antes_de_avance.docx, escribe ../Proyecto_CMEDriver_Final.docx

- NO regenera el documento desde markdown: parte del Final que ya tiene las citas y la bibliografia
  como campos de Mendeley Cite y solo agrega la seccion 6 antes de "7. Referencias".
- Cada cita de la seccion 6 se clona de un campo de Mendeley ya existente con el mismo texto visible
  (nuevo citationID, mismo itemData). Si no hay coincidencia, la cita queda como texto normal.
- Ajustes de coherencia minimos (portada, contraportada, fecha, seccion 3.6).
- Idempotente: siempre parte del respaldo, asi que NO ejecutarlo despues de editar el Final en Word
  (se perderian esos cambios). Solo usa la libreria estandar.
"""
import base64
import os
import random
import re
import sys
import uuid
import zipfile
from xml.dom import minidom
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anonimizar import REEMPLAZOS

AQUI = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.dirname(AQUI)
ORIGEN = os.path.join(PAPER, '_respaldo', 'Final_antes_de_avance.docx')
SEC6 = os.path.join(AQUI, '_tmp', 'seccion6.docx')
SALIDA = os.path.join(PAPER, 'Proyecto_CMEDriver_Final.docx')

T = r'<w:t(?: [^>]*)?>([^<]*)</w:t>'
ITEM = r'(<w:p[ >].*?</w:p>|<w:tbl>.*?</w:tbl>|<w:sdt>.*?</w:sdt>|<w:sectPr.*?</w:sectPr>)'
CITAS = ['(Brown, n.d.)', '(Randerath &amp; Friedrich, 2025)', '(OWASP API Security Project, 2023)']


def texto(xml):
    return ''.join(re.findall(T, xml, flags=re.S)).replace('&amp;', '&')


def partir(doc):
    m = re.search(r'(<w:body>)(.*)(</w:body>)', doc, flags=re.S)
    return doc[:m.start(2)], re.findall(ITEM, m.group(2), flags=re.S), doc[m.end(2):]


def reemplazar_parrafo(items, viejo, nuevo):
    n = 0
    for i, it in enumerate(items):
        if it.startswith('<w:p') and texto(it) == viejo:
            ppr = re.search(r'<w:pPr>.*?</w:pPr>', it, flags=re.S)
            rpr = re.search(r'<w:rPr>.*?</w:rPr>', it, flags=re.S)
            cab = re.match(r'<w:p[^>]*>', it).group(0)
            items[i] = f'{cab}{ppr.group(0) if ppr else ""}<w:r>{rpr.group(0) if rpr else ""}<w:t xml:space="preserve">{nuevo}</w:t></w:r></w:p>'
            n += 1
    return n


def reemplazar_texto(items, viejo, nuevo):
    n = 0
    for i, it in enumerate(items):
        if viejo in it and 'MENDELEY' not in it[:0]:
            items[i] = it.replace(viejo, nuevo)
            n += it.count(viejo)
    return n


def main():
    zf = zipfile.ZipFile(ORIGEN)
    z6 = zipfile.ZipFile(SEC6)
    doc = zf.read('word/document.xml').decode('utf-8')
    rels = zf.read('word/_rels/document.xml.rels').decode('utf-8')
    pre, items, post = partir(doc)

    # ---- campos de Mendeley existentes, por texto visible
    campos = {}
    for s in re.findall(r'<w:sdt>(?:(?!<w:sdt>).)*?</w:sdt>', doc, flags=re.S):
        tag = re.search(r'<w:tag w:val="([^"]+)"', s).group(1)
        if tag.startswith('MENDELEY_CITATION_v3_'):
            vis = ''.join(re.findall(T, re.search(r'<w:sdtContent>(.*)</w:sdtContent>', s, flags=re.S).group(1)))
            cont = re.search(r'<w:sdtContent>(.*)</w:sdtContent>', s, flags=re.S).group(1)
            # solo campos en linea dentro de un parrafo normal (no los de celdas de tabla, con letra de 9 pt)
            if '<w:tc>' in cont or '<w:p ' in cont or 'w:sz ' in cont:
                continue
            campos.setdefault(vis, s)
    ids_usados = set(re.findall(r'<w:id w:val="(-?\d+)"', doc))

    def clonar(s):
        tag = re.search(r'<w:tag w:val="([^"]+)"', s).group(1)
        raw = base64.b64decode(tag[len('MENDELEY_CITATION_v3_'):]).decode('utf-8')
        viejo = re.search(r'"citationID":"([^"]+)"', raw).group(1)
        nuevo = 'MENDELEY_CITATION_' + str(uuid.uuid4())
        raw2 = raw.replace(viejo, nuevo)
        tag2 = 'MENDELEY_CITATION_v3_' + base64.b64encode(raw2.encode('utf-8')).decode('ascii')
        while True:
            nid = str(random.randint(-2**31, 2**31 - 1))
            if nid not in ids_usados:
                ids_usados.add(nid)
                break
        s2 = s.replace(tag, tag2)
        s2 = re.sub(r'<w:id w:val="-?\d+"/>', f'<w:id w:val="{nid}"/>', s2, count=1)
        return s2

    # ---- seccion 6 (docx-js) -> cuerpo
    d6 = z6.read('word/document.xml').decode('utf-8')
    _, it6, _ = partir(d6)
    assert it6[-1].startswith('<w:sectPr')
    it6 = it6[:-1]
    cuerpo = []
    for c in it6:
        c = c.replace('w:val="Heading1"', 'w:val="Ttulo1"').replace('w:val="Heading2"', 'w:val="Ttulo2"')
        c = c.replace('<w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/>', '')
        c = c.replace('<w:sz w:val="22"/><w:szCs w:val="22"/>', '')
        c = c.replace('<w:rPr></w:rPr>', '')
        cuerpo.append(c)

    # imagenes: nuevas relaciones y archivos
    rels6 = z6.read('word/_rels/document.xml.rels').decode('utf-8')
    usados = [int(n) for n in re.findall(r'Id="rId(\d+)"', rels)]
    sig = max(usados) + 1
    mapa, nuevos_rels, media = {}, '', []
    for rid in sorted(set(re.findall(r'r:embed="(rId\d+)"', ''.join(cuerpo))), key=lambda x: int(x[3:])):
        destino = (re.search(r'Id="%s"[^>]*Target="([^"]+)"' % rid, rels6) or re.search(r'Target="([^"]+)"[^>]*Id="%s"' % rid, rels6)).group(1)
        nuevo_rid = f'rId{sig}'
        nombre = f'media/fig6_{len(media) + 1}.png'
        mapa[rid] = nuevo_rid
        nuevos_rels += f'<Relationship Id="{nuevo_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{nombre}"/>'
        media.append((nombre, z6.read('word/' + destino)))
        sig += 1
    cuerpo = [re.sub(r'r:embed="(rId\d+)"', lambda m: f'r:embed="{mapa[m.group(1)]}"', c) for c in cuerpo]
    # ids de dibujo unicos
    n_dib = [200]

    def nuevo_docpr(m):
        n_dib[0] += 1
        return f'<wp:docPr id="{n_dib[0]}"'
    cuerpo = [re.sub(r'<wp:docPr id="\d+"', nuevo_docpr, c) for c in cuerpo]
    rels2 = rels.replace('</Relationships>', nuevos_rels + '</Relationships>')

    # ---- citas: clonar campos de Mendeley
    clonadas, enTexto = {}, {}
    for k, c in enumerate(cuerpo):
        for vis in CITAS:
            marca = vis
            pos = 0
            while marca in c[pos:]:
                m = re.compile(r'<w:r>(<w:rPr>.*?</w:rPr>)?<w:t(?: [^>]*)?>([^<]*?)' + re.escape(marca) + r'([^<]*)</w:t></w:r>', re.S).search(c, pos)
                if not m:
                    break
                vis_real = vis.replace('&amp;', '&')
                if vis_real not in campos and vis not in campos:
                    enTexto[vis_real] = enTexto.get(vis_real, 0) + 1
                    break
                src = campos.get(vis_real) or campos.get(vis)
                rpr = m.group(1) or ''
                antes, desp = m.group(2), m.group(3)
                partes = ''
                if antes:
                    partes += f'<w:r>{rpr}<w:t xml:space="preserve">{antes}</w:t></w:r>'
                partes += clonar(src)
                if desp:
                    partes += f'<w:r>{rpr}<w:t xml:space="preserve">{desp}</w:t></w:r>'
                c = c[:m.start()] + partes + c[m.end():]
                pos = m.start() + len(partes)
                clonadas[vis_real] = clonadas.get(vis_real, 0) + 1
        cuerpo[k] = c

    # ---- coherencia minima
    quitados = {}
    quitados['portada'] = reemplazar_parrafo(items, 'Entregas 1 y 2: Resumen, Introducción, Marco Teórico y Metodología', 'Documento final (Entregas 1, 2 y 3)')
    quitados['contraportada'] = reemplazar_parrafo(items, 'Proyecto (Ingeniería de Software), Entregas 1 y 2', 'Proyecto (Ingeniería de Software), Documento final (Entregas 1, 2 y 3)')
    quitados['fecha'] = reemplazar_parrafo(items, 'Octubre de 2026', 'Noviembre de 2026')
    viejo36 = 'Cierran las referencias; el avance de resultados y los anexos se incorporan en la entrega final.'
    nuevo36 = ('El avance de resultados (sección 6) presenta el diseño inicial y el prototipo funcional temprano, '
               'y cierran el documento las referencias; la documentación técnica (especificaciones funcionales y no funcionales, '
               'diagramas de arquitectura y UML) se entrega en el Anexo A, como documento separado.')
    quitados['3.6'] = reemplazar_texto(items, viejo36, nuevo36)
    assert all(v == 1 for v in quitados.values()), quitados
    anon = 0
    for a, b in REEMPLAZOS:
        anon += reemplazar_texto(items, a, b)
    print('  reemplazos de anonimizacion en el documento:', anon)

    # ---- ensamblar
    ref = next(i for i, it in enumerate(items) if 'w:val="Ttulo1"' in it and texto(it).strip() == '7. Referencias')
    nuevo_doc = pre + ''.join(items[:ref]) + ''.join(cuerpo) + ''.join(items[ref:]) + post
    minidom.parseString(nuevo_doc.encode('utf-8'))
    minidom.parseString(rels2.encode('utf-8'))
    ct = zf.read('[Content_Types].xml').decode('utf-8')
    assert 'Extension="png"' in ct

    tmp = SALIDA + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as out:
        for info in zf.infolist():
            datos = zf.read(info.filename)
            if info.filename == 'word/document.xml':
                datos = nuevo_doc.encode('utf-8')
            elif info.filename == 'word/_rels/document.xml.rels':
                datos = rels2.encode('utf-8')
            out.writestr(info, datos)
        for nombre, datos in media:
            out.writestr('word/' + nombre, datos)
    os.replace(tmp, SALIDA)
    print('OK', SALIDA)
    print('  elementos de la seccion 6:', len(cuerpo), '| imagenes:', len(media))
    print('  citas clonadas (campo Mendeley):', clonadas)
    print('  citas dejadas como texto:', enTexto)
    print('  ajustes de coherencia:', quitados)


if __name__ == '__main__':
    sys.exit(main())
