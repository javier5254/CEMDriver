"""Genera los archivos RIS y BibTeX de las referencias para importarlos en Mendeley.

Uso:  python generar_referencias.py

Lee paper/secciones/referencias-entrega1.md y referencias-entrega2.md y escribe, en paper/referencias/,
entrega1, entrega2 y referencias-unificado (.ris y .bib). El unificado trae las fuentes de las dos
entregas sin duplicados (la lista del documento unificado) y es el que conviene importar.
"""
import os
import re
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MESES = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
         'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
INI = r"(?:(?:[A-ZÁÉÍÓÚ]\.|de|van|del|da)\s?)+"


def entries(path):
    t = open(path, encoding='utf-8').read()
    return [l.strip() for l in t.splitlines() if l.strip() and not l.startswith('#')]


def parse_authors(s):
    s = s.replace(', . . . ', ', ').replace('&', '').strip()
    out = re.findall(r"([^,]+?),\s*(" + INI + r")", s + ' ')
    if not out:
        return [(s.strip().rstrip('.'), '')]  # autor institucional
    return [(a.strip(), i.strip()) for a, i in out]


def split_head(e):
    m = re.match(r"^(.*?)\s\((\d{4}|s\. f\.)(?:,\s*(\d{1,2}) de (\w+))?\)\.\s*(.*)$", e)
    au, y, d, mes, rest = m.groups()
    return au, y, d, mes, rest


def make(e):
    au, y, d, mes, rest = split_head(e)
    r = {'AU': parse_authors(au), 'PY': None if y == 's. f.' else y, 'raw': e, 'N1': []}
    if d and mes:
        r['DA'] = f"{y}/{MESES[mes]:02d}/{int(d):02d}/"
    doi = re.search(r"https://doi\.org/(\S+)$", e)
    url = re.search(r"(https?://\S+)$", e)
    if doi:
        r['DO'] = doi.group(1)
    if url:
        r['UR'] = url.group(1)
    first = au

    # --- artículos de revista
    m = re.match(r"^(.*?[.?])\s+\*([^*]+?),\s*(\d+)\*(?:\((\d+)\))?,?\s*(?:(?:Article|Artículo)\s+(\S+?)|(\d+)[–-](\d+))?\.\s*https", rest)
    if m and 'En S. Latifi' not in rest:
        t, jo, vl, iss, art, sp, ep = m.groups()
        r.update(TY='JOUR', T1=t.rstrip('.') if not t.endswith('?') else t, JO=jo.strip(), VL=vl)
        if iss: r['IS'] = iss
        if art: r['SP'] = art; r['N1'].append(f'Número de artículo: {art}')
        if sp: r['SP'], r['EP'] = sp, ep
        return r
    # Mogire: sin páginas ni número
    if first.startswith('Mogire'):
        r.update(TY='JOUR', T1='Customer satisfaction with last-mile delivery in Kenya: An online customer perspective',
                 JO='Journal of Transport and Supply Chain Management', VL='17')
        return r
    # --- capítulo de actas
    if first.startswith('Beaulieu'):
        r.update(TY='CPAPER', T1='API-first design: A survey of the state of academia and industry',
                 T2='ITNG 2022 19th International Conference on Information Technology-New Generations',
                 A2=[('Latifi', 'S.')], SP='73', EP='79', PB='Springer')
        return r
    # --- libros
    if first.startswith(('Bass', 'Hernández', 'Sommerville')):
        mm = re.match(r"^\*(.+?)\*(?:\s\((\d+)\.ª ed\.\))?\.\s*(.+)\.$", rest)
        r.update(TY='BOOK', T1=mm.group(1), PB=mm.group(3))
        if mm.group(2): r['ET'] = mm.group(2)
        if first.startswith('Hernández'): r['N1'].append('Pendiente confirmar el tercer autor de la obra.')
        return r
    # --- informes
    if first.startswith('Cámara'):
        r.update(TY='RPRT', T1='Informe de cierre del comercio electrónico en Colombia – 2025')
        return r
    if first.startswith('Ministerio'):
        r.update(TY='RPRT', T1='Boletín trimestral del sector postal: Cuarto trimestre de 2025', PB='Colombia TIC')
        return r
    # --- comunicados de prensa del DNP
    if first.startswith('Departamento'):
        t = re.match(r"^\*(.+?)\*\s*\[Comunicado de prensa\]", rest).group(1)
        r.update(TY='ELEC', T1=t)
        r['N1'].append('Comunicado de prensa')
        return r
    # --- leyes y normas
    if first.startswith(('Ley', 'Comisión')):
        mm = re.match(r"^(.+?)\.\s+(Diario Oficial[^.]*?No\. [\d.]+|Gaceta Oficial[^.]*?No\. \d+)\.\s*https?", rest)
        if first.startswith('Comisión'):
            mm = re.match(r"^(Decisión 351: .+?)\.\s+(Gaceta Oficial del Acuerdo de Cartagena No\. 145)\.\s*https?", rest)
        r.update(TY='GEN', T1=mm.group(1))
        r['N1'].append(mm.group(2))
        r['N1'].append('Norma / legislación')
        if y != 's. f.': r.setdefault('DA', f"{y}///")
        return r
    if first.startswith('ISO'):
        r.update(TY='GEN', T1='Systems and software engineering — Life cycle processes — Requirements engineering')
        r['N1'].append('ISO/IEC/IEEE 29148:2018, 2.ª ed.')
        return r
    # --- sitios web, guías y modelo de lenguaje
    if first.startswith('Anthropic'):
        r.update(TY='GEN', T1='Claude')
        r['N1'].append('Modelo de lenguaje grande')
        return r
    mm = re.match(r"^\*(.+?)\*\.\s*(?:(.+?)\.\s*)?https?", rest)
    r.update(TY='ELEC', T1=mm.group(1))
    if mm.group(2): r['PB'] = mm.group(2)
    return r


def ris(rec):
    L = [f"TY  - {rec['TY']}"]
    for a, i in rec['AU']:
        L.append(f"AU  - {a}, {i}" if i else f"AU  - {a}")
    for a, i in rec.get('A2', []):
        L.append(f"A2  - {a}, {i}")
    L.append(f"T1  - {rec['T1']}")
    for k in ('T2', 'JO', 'VL', 'IS', 'SP', 'EP', 'ET', 'PB'):
        if k in rec: L.append(f"{k}  - {rec[k]}")
    if rec['PY']:
        L.append(f"PY  - {rec['PY']}")
    if 'DA' in rec:
        L.append(f"DA  - {rec['DA']}")
    if 'DO' in rec: L.append(f"DO  - {rec['DO']}")
    if 'UR' in rec: L.append(f"UR  - {rec['UR']}")
    for n in rec['N1']:
        L.append(f"N1  - {n}")
    if rec['PY'] is None:
        L.append('N1  - Sin fecha (s. f.)')
    L.append('ER  - ')
    return '\r\n'.join(L)


BT = {'JOUR': 'article', 'CPAPER': 'inproceedings', 'BOOK': 'book', 'RPRT': 'techreport', 'ELEC': 'misc', 'GEN': 'misc'}


def bib(rec, n):
    import unicodedata
    base = unicodedata.normalize('NFKD', rec['AU'][0][0].split()[0].lower()).encode('ascii', 'ignore').decode()
    key = re.sub(r"\W", '', base) + (rec['PY'] or 'sf') + str(n)
    au = ' and '.join((f"{a}, {i}" if i else '{' + a + '}') for a, i in rec['AU'])
    F = [('author', au), ('title', rec['T1'])]
    if 'JO' in rec: F.append(('journal', rec['JO']))
    if 'T2' in rec: F.append(('booktitle', rec['T2']))
    if rec.get('A2'): F.append(('editor', ' and '.join(f"{a}, {i}" for a, i in rec['A2'])))
    if 'VL' in rec: F.append(('volume', rec['VL']))
    if 'IS' in rec: F.append(('number', rec['IS']))
    if 'SP' in rec: F.append(('pages', rec['SP'] + (('--' + rec['EP']) if 'EP' in rec else '')))
    if 'ET' in rec: F.append(('edition', rec['ET']))
    if 'PB' in rec: F.append(('publisher' if rec['TY'] in ('BOOK', 'CPAPER') else 'institution' if rec['TY'] == 'RPRT' else 'organization', rec['PB']))
    if rec['PY']: F.append(('year', rec['PY']))
    if 'DA' in rec:
        y, m, d = rec['DA'].strip('/').split('/')[:3] if rec['DA'].count('/') >= 3 and rec['DA'].split('/')[1] else (rec['PY'], None, None)
        if m: F += [('month', str(int(m))), ('day', str(int(d)))]
    if 'DO' in rec: F.append(('doi', rec['DO']))
    if 'UR' in rec: F.append(('url', rec['UR']))
    if rec['N1']: F.append(('note', '; '.join(rec['N1'])))
    body = ',\n'.join(f"  {k} = {{{v}}}" for k, v in F)
    return f"@{BT[rec['TY']]}{{{key},\n{body}\n}}"


def escribir(nombre, recs):
    ruta = os.path.join(P, 'referencias', nombre)
    open(ruta + '.ris', 'w', encoding='utf-8', newline='').write('\r\n'.join(ris(r) for r in recs) + '\r\n')
    open(ruta + '.bib', 'w', encoding='utf-8', newline='').write('\n\n'.join(bib(r, i + 1) for i, r in enumerate(recs)) + '\n')


todas = {}
for tag, fn in (('1', 'referencias-entrega1.md'), ('2', 'referencias-entrega2.md')):
    recs = [make(e) for e in entries(os.path.join(P, 'secciones', fn))]
    escribir('entrega' + tag, recs)
    print(f'=== entrega{tag}: {len(recs)} registros')
    for r in recs:
        k = (re.sub(r'\W', '', r['AU'][0][0].lower()), r['PY'], r['T1'][:30].lower())
        todas.setdefault(k, r)

unificado = sorted(todas.values(), key=lambda r: re.sub(r'[^a-z0-9]', '', r['AU'][0][0].lower()))
escribir('referencias-unificado', unificado)
print(f'=== referencias-unificado: {len(unificado)} registros (sin duplicados)')
for r in unificado:
    print(f"  {r['TY']:7} {r['AU'][0][0][:30]:30} {str(r['PY']):5} doi={'si' if 'DO' in r else 'no'} | {r['T1'][:58]}")
