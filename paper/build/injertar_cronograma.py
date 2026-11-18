"""Reemplaza el cuerpo de '7. Cronograma del proyecto' en una copia del Final (no inserta: sustituye).

Uso:
    node build_seccion7.js                                        # genera build/_tmp/seccion7.docx (secciones 7 y 8)
    python injertar_cronograma.py ENTRADA.docx SALIDA.docx        # nunca sobrescribe ENTRADA

- Sustituye todo lo que hay entre el titulo '7. Cronograma del proyecto' y '8. Presupuesto del proyecto' por el cuerpo
  de la seccion 7 de seccion7.docx (prosa, Tabla 9 y nota). No toca nada mas: los campos de Mendeley (citas y
  bibliografia), sus overrides y la seccion 8 quedan byte a byte iguales.
"""
import os
import re
import sys
import zipfile
from xml.dom import minidom

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from injertar_seccion7 import partir, texto, titulo1, SEC7  # noqa: E402


def main(entrada, salida):
    if os.path.abspath(entrada) == os.path.abspath(salida):
        sys.exit('ENTRADA y SALIDA deben ser distintas')
    zin = zipfile.ZipFile(entrada)
    datos = [(i, zin.read(i.filename)) for i in zin.infolist()]
    zin.close()
    doc = next(d for i, d in datos if i.filename == 'word/document.xml').decode('utf-8')
    pre, items, post = partir(doc)

    # cuerpo nuevo (entre los titulos 7 y 8 de seccion7.docx)
    _, it7, _ = partir(zipfile.ZipFile(SEC7).read('word/document.xml').decode('utf-8'))
    h = [k for k, it in enumerate(it7) if it.startswith('<w:p') and 'w:val="Heading1"' in it]
    assert len(h) == 2, h
    cuerpo = []
    for c in it7[h[0] + 1:h[1]]:
        c = c.replace('w:val="Heading1"', 'w:val="Ttulo1"').replace('w:val="Heading2"', 'w:val="Ttulo2"')
        c = c.replace('<w:rFonts w:ascii="Arial" w:cs="Arial" w:eastAsia="Arial" w:hAnsi="Arial"/>', '')
        c = c.replace('<w:sz w:val="22"/><w:szCs w:val="22"/>', '').replace('<w:rPr></w:rPr>', '')
        cuerpo.append(c)
    assert not re.search(r'<w:drawing>|r:embed|<w:sdt>', ''.join(cuerpo))

    # rango a reemplazar en el Final
    i7 = next(i for i, it in enumerate(items) if titulo1(it) and texto(it).strip() == '7. Cronograma del proyecto')
    i8 = next(i for i, it in enumerate(items) if i > i7 and titulo1(it) and texto(it).strip() == '8. Presupuesto del proyecto')
    viejo = items[i7 + 1:i8]
    assert not any('<w:sdt>' in v for v in viejo), 'la seccion 7 vigente tiene campos: no se reemplaza'
    items[i7 + 1:i8] = cuerpo
    nuevo = pre + ''.join(items) + post
    minidom.parseString(nuevo.encode('utf-8'))
    tmp = salida + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as out:
        for info, d in datos:
            out.writestr(info, nuevo.encode('utf-8') if info.filename == 'word/document.xml' else d)
    os.replace(tmp, salida)
    print(f'OK {salida}: {len(viejo)} elementos reemplazados por {len(cuerpo)}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
