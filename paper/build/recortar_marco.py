"""Recorta redundancias del Marco Teorico (seccion 4) editando el XML de un .docx, sin tocar tablas ni la bibliografia.

Uso:  python recortar_marco.py ENTRADA.docx SALIDA.docx
- Cada recorte se expresa sobre el texto VISIBLE de un parrafo: 'A ... B' elimina de A a B inclusive.
- Un campo de Mendeley (w:sdt) solo se elimina si esta completo dentro del recorte; despues se comprueba que
  el conjunto de fuentes citadas del documento no cambie (ninguna fuente queda huerfana).
- Los recortes estan documentados en referencias/RECORTES_MARCO.md.
"""
import base64
import re
import sys
import zipfile
from xml.dom import minidom

T = r'<w:t(?: [^>]*)?>([^<]*)</w:t>'
ITEM = r'(<w:p[ >].*?</w:p>|<w:tbl>.*?</w:tbl>|<w:sdt>.*?</w:sdt>|<w:sectPr.*?</w:sectPr>)'
SEG = r'(<w:sdt>.*?</w:sdt>|<w:r(?: [^>]*)?>.*?</w:r>)'

# (inicio_del_parrafo, [(A, B, reemplazo)])  A..B se busca en el texto visible; B=None elimina solo A
RECORTES = [
    ('Este capítulo retoma', [(' Integra conceptos clave', 'sección 3.3.', '')]),
    ('Los dos trabajos discrepan', [(' Queda abierta la pregunta', 'la trazabilidad.', '')]),
    ('La evidencia digital es el segundo', [(' Su valor probatorio se discute en 4.8', 'efecto operativo.', ''),
                                           ('; falta la arquitectura', 'tipos de usuario.', '.')]),
    ('La decisión de CMEDriver', [(' Falta ahora la comunicación', 'no cubre.', '')]),
    ('El seguimiento GPS y el chat', [(' De ahí la decisión de mantener', 'literatura.', '')]),
    ('Sobre las aplicaciones híbridas', [(' A continuación se trata', 'motorizado asignado.', '')]),
    ('Sobre la comunicación directa', [(' OWASP API Security Project (2023) incluye', 'se retoma en 4.7.', ''),
                                      (' y conduce a la planificación', 'mismo backend.', '.'),
                                      (' El más cercano, Gracia', 'sobre la entrega.', '')]),
    ('La asignación de servicios a motorizados', [('discuten la naturaleza de estos problemas', 'parámetros estocásticos',
                                                    'discuten aspectos como la capacidad de la flota, las ventanas de tiempo y el dinamismo de los datos')]),
    ('La geocodificación se apoya', [(' y deja pendiente un aspecto transversal', 'la seguridad.', '.')]),
    ('La plataforma expone una API', [(' Ambos aplican a una plataforma con cuatro roles', 'claves de API.', '')]),
    ('A ellos se suma la autorización', [(' (API1:2023, retomada en 4.5)', None, ' (API1:2023)'),
                                        (' La fuente es una guía abierta', 'criterio de diseño.', ''),
                                        (' La seguridad técnica no agota', 'marco legal.', '')]),
    ('Los datos que circulan por la plataforma', [(' Se presenta lo que las fuentes oficiales', 'profesional del derecho.', '')]),
    ('Datos personales.', [(' Su reglamentación (decretos compilados)', 'personas reales.', '')]),
    ('Mensajes de datos y firma', [(' Se deja como punto a consultar', 'custodia de la evidencia.', '')]),
    ('Calidad y requisitos.', [(' Resta explicar con qué enfoques', 'todo lo anterior.', '')]),
    ('Ágil y Scrum.', [(' En un proyecto de una sola persona', 'el marco completo no.', ''),
                       (', y la propia guía advierte', 'oculta problemas', '')]),
    ('Design Thinking.', [(' La guía lo toma de la d.school de Stanford.', None, '')]),
    ('Arquitectura y modelo C4.', [(' Esa neutralidad y el zoom progresivo', 'es el que adopta',
                                    ' Esa neutralidad lo hace apropiado para comunicar una arquitectura modular, y es el que adopta')]),
    ('Especificación de requisitos. La norma', [('@PARRAFO', None, '')]),
    ('El subtítulo respalda los Objetivos 2 y 4', [('@PARRAFO', None, '')]),
    ('La teoría revisada converge', [('@PARRAFO', None,
        'La teoría revisada converge en tres argumentos que sostienen el diseño de CMEDriver. Primero, la última milla es un problema '
        'de coordinación y de información además de logístico, por lo que una plataforma integrada puede mejorar la visibilidad y no la informalidad '
        'estructural. Segundo, una arquitectura modular orientada a API con comunicación en tiempo real es coherente con la literatura revisada, '
        'siempre que la autorización por rol y por objeto resida en el backend. Tercero, los datos de ubicación, firma, foto y chat convierten la '
        'privacidad y la evidencia en requisitos de diseño.')]),
    ('Con la literatura revisada no se resuelven', [('Con la literatura revisada no se resuelven, y por eso se declaran como vacíos, los siguientes puntos.', None,
                                                   'Con la literatura revisada quedan sin resolver los siguientes vacíos.'),
                                                   (': Jazemi et al. (2023)', 'caso europeo', ''),
                                                   (': Souza et al. (2022)', 'caso brasileño', '')]),
]


def texto(xml):
    return ''.join(re.findall(T, xml, flags=re.S))


def fuentes(doc):
    """Conjunto de fuentes citadas (campos de Mendeley) y numero de campos."""
    ids, n = set(), 0
    for s in re.findall(r'<w:sdt>(?:(?!<w:sdt>).)*?</w:sdt>', doc, flags=re.S):
        m = re.search(r'<w:tag w:val="MENDELEY_CITATION_v3_([^"]+)"', s)
        if not m:
            continue
        n += 1
        raw = base64.b64decode(m.group(1)).decode('utf-8')
        ids.update(re.findall(r'\{"id":"([0-9a-f-]{36})","itemData"', raw))
    return ids, n


def recortar_parrafo(p, cortes):
    cab = re.match(r'<w:p[^>]*>', p).group(0)
    ppr = re.search(r'<w:pPr>.*?</w:pPr>', p, flags=re.S)
    cuerpo = p[len(cab) + (len(ppr.group(0)) if ppr else 0):-len('</w:p>')]
    segs, last = [], 0
    for m in re.finditer(SEG, cuerpo, flags=re.S):
        if m.start() > last:
            segs.append(cuerpo[last:m.start()])  # elementos sin texto (marcas, bookmarks)
        segs.append(m.group(0)); last = m.end()
    if last < len(cuerpo):
        segs.append(cuerpo[last:])
    assert ''.join(segs) == cuerpo
    vis = [texto(s) for s in segs]
    for a, b, rep in cortes:
        full = ''.join(vis)
        if a == '@PARRAFO':
            i0, i1 = 0, len(full)
        else:
            i0 = full.index(a)
            i1 = full.index(b, i0) + len(b) if b else i0 + len(a)
        pos, nuevo, nvis, puesto = 0, [], [], False
        for s, v in zip(segs, vis):
            s0, s1 = pos, pos + len(v)
            pos = s1
            if s1 <= i0 or s0 >= i1:
                nuevo.append(s); nvis.append(v); continue
            if not s.startswith(('<w:sdt>', '<w:r>', '<w:r ')):
                nuevo.append(s); nvis.append(v); continue
            if s.startswith('<w:sdt>'):
                assert s0 >= i0 and s1 <= i1, 'el recorte parte un campo de cita: ' + a
                if not puesto and rep:
                    pass
                continue
            # run de texto plano: recorta la parte solapada
            antes, despues = v[:max(0, i0 - s0)], v[min(len(v), i1 - s0):]
            nt = antes + (rep if not puesto else '') + despues
            puesto = True
            if nt:
                s2 = re.sub(T, lambda m: '<w:t xml:space="preserve">' + nt + '</w:t>', s, count=1, flags=re.S)
                nuevo.append(s2); nvis.append(nt)
        if not puesto and rep:
            raise AssertionError('no hay run de texto plano donde insertar el reemplazo: ' + a)
        segs, vis = nuevo, nvis
    return cab + (ppr.group(0) if ppr else '') + ''.join(segs) + '</w:p>'


def main(entrada, salida):
    zin = zipfile.ZipFile(entrada)
    datos = [(i, zin.read(i.filename)) for i in zin.infolist()]
    doc = next(d for i, d in datos if i.filename == 'word/document.xml').decode('utf-8')
    f0, n0 = fuentes(doc)
    palabras0 = len(texto(doc).split())
    por_hacer = list(RECORTES)
    resultado = []
    for it in re.findall(ITEM, re.search(r'<w:body>(.*)</w:body>', doc, flags=re.S).group(1), flags=re.S):
        if it.startswith('<w:p') and por_hacer and texto(it).strip().startswith(por_hacer[0][0]):
            ini, cortes = por_hacer.pop(0)
            nuevo = recortar_parrafo(it, cortes)
            if not texto(nuevo).strip() and '<w:drawing>' not in nuevo:
                nuevo = ''  # parrafo eliminado por completo
            doc = doc.replace(it, nuevo, 1)
            antes, desp = len(texto(it).split()), len(texto(nuevo).split())
            resultado.append((ini, antes - desp))
    assert not por_hacer, 'no se encontraron: ' + str([p[0] for p in por_hacer])
    f1, n1 = fuentes(doc)
    minidom.parseString(doc.encode('utf-8'))
    for ini, w in resultado:
        print(f'  -{w:3d} palabras: {ini}')
    print('  total recortado:', sum(w for _, w in resultado), '| campos de cita', n0, '->', n1, '| fuentes unicas', len(f0), '->', len(f1))
    assert f0 == f1, 'cambio el conjunto de fuentes: ' + str(f0 ^ f1)
    with zipfile.ZipFile(salida, 'w', zipfile.ZIP_DEFLATED) as out:
        for info, d in datos:
            out.writestr(info, doc.encode('utf-8') if info.filename == 'word/document.xml' else d)
    print('OK', salida)


if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] == sys.argv[2]:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
