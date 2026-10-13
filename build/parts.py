"""Shared HTML fragments used inside Elementor HTML widgets.

The trench diagram and the length chart are the only HTML-widget content;
everything else on the pages is built from standard Elementor widgets.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REFS = json.load(open(os.path.join(HERE, '..', 'docs', 'data', 'references.json'), encoding='utf-8'))


def km(m, decimals=1):
    v = m / 1000
    s = f'{v:,.{decimals}f}'.replace(',', ' ').replace('.', ',').replace(' ', '.')
    return s + ' km'


# Steps as described for the Petrovaradin fortress site (old site, index.html)
TRENCH_STEPS = [
    'Vađenje kocke, sečenje i razbijanje asfalta i betona',
    'Iskop kanala',
    'Postavljanje cevi',
    'Nabijanje peska oko cevi',
    'Zatrpavanje kanala i mašinsko nabijanje zemlje',
    'Dovođenje terena u prvobitno stanje',
]


def trench_svg():
    # Pavement cubes along the surface (left and right of the trench)
    cubes = []
    for x in list(range(20, 196, 22)) + list(range(372, 548, 22)):
        cubes.append(f'<rect x="{x}" y="84" width="20" height="14" />')
    # restored cubes over the trench (drawn red-outlined = restored)
    restored = ''.join(f'<rect x="{x}" y="84" width="20" height="14" />' for x in range(196, 372, 22))
    compaction = ''.join(
        f'<line x1="{206 + (y - 104) * 0.06:.1f}" y1="{y}" x2="{354 - (y - 104) * 0.06:.1f}" y2="{y}" />'
        for y in range(132, 262, 26))

    def callout(n, cx, cy, tx, ty):
        return (f'<line class="t-tr-lead" x1="{cx}" y1="{cy}" x2="{tx}" y2="{ty}" />'
                f'<circle class="t-tr-dot" cx="{tx}" cy="{ty}" r="13" />'
                f'<text class="t-tr-num" x="{tx}" y="{ty + 4.5}" text-anchor="middle">{n}</text>'
                f'<circle class="t-tr-pin" cx="{cx}" cy="{cy}" r="3" />')

    return f'''<figure class="t-trench" aria-labelledby="t-trench-cap">
<svg viewBox="0 0 570 420" role="img" aria-labelledby="t-trench-title t-trench-desc" xmlns="http://www.w3.org/2000/svg">
<title id="t-trench-title">Presek rova pri izgradnji gasne mreže</title>
<desc id="t-trench-desc">Šematski presek: površina od kocke, rov iskopan kroz tlo, cev položena u pesak, zatrpan i nabijen rov i obnovljena površina. Brojevi 1 do 6 označavaju redosled radova navedenih ispod crteža.</desc>
<defs>
 <pattern id="t-soil" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#D9CCB4"/><circle cx="3" cy="4" r="1.1" fill="#B9A585"/><circle cx="10" cy="10" r="1.1" fill="#B9A585"/></pattern>
 <pattern id="t-sand" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="#EFE3C2"/><circle cx="2" cy="2" r=".8" fill="#CDB98C"/><circle cx="6" cy="6" r=".8" fill="#CDB98C"/></pattern>
 <pattern id="t-fill" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#CBBB9E"/><circle cx="4" cy="9" r="1.2" fill="#A8926F"/><circle cx="11" cy="3" r="1" fill="#A8926F"/></pattern>
</defs>
<rect x="0" y="98" width="570" height="300" fill="url(#t-soil)"/>
<path d="M196 98 L214 372 L346 372 L364 98 Z" fill="url(#t-fill)"/>
<path d="M210 312 L214 372 L346 372 L350 312 Z" fill="url(#t-sand)"/>
<path d="M207 268 L210 312 L350 312 L353 268 Z" fill="url(#t-sand)"/>
<g class="t-tr-compact">{compaction}</g>
<line class="t-tr-sandline" x1="207" y1="268" x2="353" y2="268"/>
<circle cx="280" cy="336" r="20" fill="#E5B323" stroke="#1C1D1B" stroke-width="2"/>
<circle cx="280" cy="336" r="14" fill="none" stroke="#1C1D1B" stroke-width="1" opacity=".45"/>
<path class="t-tr-wall" d="M196 98 L214 372 L346 372 L364 98"/>
<g class="t-tr-cubes">{''.join(cubes)}</g>
<g class="t-tr-cubes t-tr-restored">{restored}</g>
<line class="t-tr-route" x1="196" y1="70" x2="364" y2="70"/>
<line class="t-tr-route" x1="196" y1="62" x2="196" y2="78"/><line class="t-tr-route" x1="364" y1="62" x2="364" y2="78"/>
<text class="t-tr-tag" x="280" y="56" text-anchor="middle">TRASA</text>
{callout(1, 120, 91, 70, 40)}
{callout(2, 352, 200, 470, 170)}
{callout(3, 296, 330, 470, 330)}
{callout(4, 220, 300, 100, 300)}
{callout(5, 230, 200, 100, 200)}
{callout(6, 300, 91, 470, 40)}
</svg>
<figcaption id="t-trench-cap" class="t-trench__legend"><ol>{''.join(f'<li>{s}</li>' for s in TRENCH_STEPS)}</ol></figcaption>
</figure>'''


def length_chart():
    """Horizontal bars: documented length per period, 1998–2012 (ascending)."""
    rows = []
    for g in REFS:
        total = sum(i.get('length_m', 0) for i in g['items'] if not i.get('note'))
        if total:
            rows.append((g['period'], total))
    rows.sort(key=lambda r: r[0])
    peak = max(t for _, t in rows)
    out = ['<ul class="t-bars" aria-label="Evidentirane dužine po periodima, 1998–2012.">']
    for period, total in rows:
        pct = round(total / peak * 100, 1)
        out.append(f'<li class="t-bars__row"><span class="t-bars__label">{period}</span>'
                   f'<span class="t-bars__track" aria-hidden="true"><span class="t-bars__fill" style="width:{pct}%"></span></span>'
                   f'<span class="t-bars__val">{km(total)}</span></li>')
    out.append('</ul>')
    return ''.join(out)


def documented_total():
    return sum(i.get('length_m', 0) for g in REFS for i in g['items'] if not i.get('note'))
