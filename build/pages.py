"""Generates Elementor page data (_elementor_data) for every page of the site.

Run:  python build/pages.py      -> writes build/out/*.json and build/out/manifest.json
Then: wp eval-file build/import.php  (see README.md)

Layouts use Elementor containers and standard widgets (Heading, Text Editor,
Button, HTML) so the client can edit everything visually. Styling hooks are
the t-* CSS classes defined in wp-custom/site.css.
"""
import json
import os
import random

from parts import REFS, km, trench_svg, length_chart, documented_total

random.seed(24101997)  # stable element IDs between builds
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
os.makedirs(OUT, exist_ok=True)

PHONE_MAIN = ('+381 21 47 41 048', 'tel:+381214741048')
PHONE_2 = ('+381 21 551 044', 'tel:+38121551044')
PHONE_3 = ('+381 21 6413 900, lok. 116', 'tel:+381216413900')
MOBILE = ('+381 63 503 333', 'tel:+38163503333')
EMAIL = '24oktobar.ns@gmail.com'
MAP_URL = 'https://www.google.com/maps/search/?api=1&query=Temerinska+50%2C+21000+Novi+Sad'


# --------------------------------------------------------------------------- helpers
def _id():
    return '%07x' % random.getrandbits(28)


def px(v):
    return {'unit': 'px', 'size': v, 'sizes': []}


def pad(t, r, b, l):
    return {'unit': 'px', 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': False}


def gap(v):
    return {'unit': 'px', 'size': v, 'column': str(v), 'row': str(v), 'isLinked': True}


def section(children, cls='', bg=None, pad_d=(112, 24, 112, 24), pad_t=(80, 24, 80, 24), pad_m=(56, 20, 56, 20),
            direction='column', gap_d=32, gap_m=None, eid=None, tag='section', tablet_dir=None, align=None):
    """Top-level boxed container (full-bleed background, 1240px content)."""
    s = {
        'content_width': 'boxed', 'boxed_width': px(1240),
        'flex_direction': direction, 'flex_direction_mobile': 'column',
        'flex_gap': gap(gap_d), 'flex_gap_mobile': gap(gap_m if gap_m is not None else min(gap_d, 32)),
        'padding': pad(*pad_d), 'padding_tablet': pad(*pad_t), 'padding_mobile': pad(*pad_m),
        'html_tag': tag, 'css_classes': ('t-sec ' + cls).strip(),
    }
    if tablet_dir:
        s['flex_direction_tablet'] = tablet_dir
    if align:
        s['flex_align_items'] = align
    if bg:
        s['background_background'] = 'classic'
        s['background_color'] = bg
    if eid:
        s['_element_id'] = eid
    return {'id': _id(), 'elType': 'container', 'isInner': False, 'settings': s, 'elements': children}


def box(children, width=None, cls='', direction='column', gap_d=16, tablet_width=None, tablet_dir=None,
        align=None, justify=None, wrap=False, tag=None):
    """Inner container. width in % of the parent row (desktop)."""
    s = {
        'content_width': 'full', 'flex_direction': direction, 'flex_direction_mobile': 'column',
        'flex_gap': gap(gap_d), 'padding': pad(0, 0, 0, 0), 'css_classes': cls,
    }
    if width:
        s['width'] = {'unit': '%', 'size': width}
        s['width_tablet'] = {'unit': '%', 'size': tablet_width or width}
        s['width_mobile'] = {'unit': '%', 'size': 100}
    if tablet_dir:
        s['flex_direction_tablet'] = tablet_dir
    if align:
        s['flex_align_items'] = align
    if justify:
        s['flex_justify_content'] = justify
    if wrap:
        s['flex_wrap'] = 'wrap'
    if tag:
        s['html_tag'] = tag
    return {'id': _id(), 'elType': 'container', 'isInner': True, 'settings': s, 'elements': children}


def w(kind, settings):
    # Widgets keep their CSS class in `_css_classes` (Advanced → CSS Classes); containers use `css_classes`.
    if 'css_classes' in settings:
        settings['_css_classes'] = settings.pop('css_classes')
    return {'id': _id(), 'elType': 'widget', 'widgetType': kind, 'settings': settings, 'elements': []}


def h(text, level='h2', cls=''):
    return w('heading', {'title': text, 'header_size': level, 'css_classes': cls})


def eyebrow(text):
    return w('heading', {'title': text, 'header_size': 'p', 'css_classes': 't-eyebrow'})


def txt(html, cls=''):
    return w('text-editor', {'editor': html, 'css_classes': cls})


def btn(text, url, variant='primary', cls=''):
    external = 'on' if url.startswith('http') else ''
    return w('button', {'text': text, 'link': {'url': url, 'is_external': external, 'nofollow': ''},
                        'size': 'md', 'css_classes': f't-btn t-btn--{variant} {cls}'.strip()})


def html(code, cls=''):
    return w('html', {'html': code, 'css_classes': cls})


def page_head(eyebrow_text, title, lead, extra=None):
    left = [eyebrow(eyebrow_text), h(title, 'h1', 't-h1'), txt(f'<p>{lead}</p>', 't-lead')]
    if extra:
        left += extra
    return section([box(left, width=72, tablet_width=100, gap_d=20)], cls='t-pagehead', bg='#F2EEE6',
                   pad_d=(96, 24, 72, 24), pad_t=(72, 24, 56, 24), pad_m=(48, 20, 40, 20))


def ul(items, cls='t-list'):
    return f'<ul class="{cls}">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def ledger_row(period, title, place, scope):
    return box([
        txt(f'<p>{period}</p>', 't-ledger__period'),
        h(title, 'h3', 't-ledger__title'),
        txt(f'<p>{place}</p>', 't-ledger__place'),
        txt(f'<p>{scope}</p>', 't-ledger__scope'),
    ], cls='t-ledger__row', direction='row', gap_d=24, tablet_dir='row', align='baseline')


def contact_band():
    return section([
        box([eyebrow('Kontakt'), h('Temerinska 50, Novi Sad', 'h2', 't-h2'),
             txt('<p>Radno vreme: ponedeljak–petak, 08:00–15:00.</p>', 't-lead')], width=50, tablet_width=100, gap_d=16),
        box([
            txt(f'<p class="t-bigtel"><a href="{PHONE_MAIN[1]}">{PHONE_MAIN[0]}</a></p>'
                f'<p class="t-bigtel"><a href="{MOBILE[1]}">{MOBILE[0]}</a></p>'
                f'<p class="t-bigmail"><a href="mailto:{EMAIL}">{EMAIL}</a></p>'),
            btn('Svi kontakt podaci', '/kontakt/', 'light'),
        ], width=50, tablet_width=100, gap_d=24),
    ], cls='t-contactband t-on-red', bg='#A92D3D', direction='row', tablet_dir='column', gap_d=48,
        pad_d=(96, 24, 96, 24))


# --------------------------------------------------------------------------- HOME
def home():
    intro = section([
        box([
            eyebrow('Novi Sad · od 1997.'),
            h('Gasovodi, vodovod i podzemne mreže — od iskopa do vraćanja terena u prvobitno stanje.', 'h1', 't-h1 t-h1--home'),
            txt('<p>Građevinsko preduzeće „24. Oktobar“ izvodi grube građevinske radove i specifične radove niskogradnje: '
                'magistralne gasovode, distributivne gasne mreže i kućne gasne priključke, vodovodnu, toplovodnu i PTT mrežu '
                'i mrežu za odvod atmosferskih voda.</p>', 't-lead'),
            box([
                btn('Reference 1998–2018', '/reference/', 'primary'),
                txt(f'<p class="t-inline-tel">ili pozovite <a href="{PHONE_MAIN[1]}">{PHONE_MAIN[0]}</a></p>'),
            ], direction='row', gap_d=28, align='center', cls='t-actions', wrap=True),
        ], width=54, tablet_width=100, gap_d=24, cls='t-intro__text'),
        box([html(trench_svg())], width=46, tablet_width=100, cls='t-intro__figure'),
    ], cls='t-intro', bg='#F2EEE6', direction='row', tablet_dir='column', gap_d=64, align='center',
        pad_d=(72, 24, 96, 24), pad_t=(56, 24, 72, 24), pad_m=(36, 20, 56, 20))

    services = section([
        box([eyebrow('Delatnosti'), h('Niskogradnja i grubi građevinski radovi', 'h2', 't-h2'),
             txt('<p>Radove izvodimo sopstvenim mašinama i alatom — od raščišćavanja terena i iskopa '
                 'do mašinskog nabijanja i dovođenja površine u prvobitno stanje.</p>'),
             btn('Delatnosti sa primerima', '/delatnosti/', 'text')], width=34, tablet_width=100, gap_d=20,
            cls='t-sticky'),
        box([
            box([txt('<p>A</p>', 't-index'), h('Specifični radovi niskogradnje', 'h3', 't-h3'),
                 txt(ul(['Magistralni gasovodi i gasovodi visokog i srednjeg pritiska',
                         'Distributivne gasne mreže i kućni gasni priključci',
                         'Merno-regulacione stanice i otpremno-čistačka mesta',
                         'Vodovodna i toplovodna mreža',
                         'Mreža za odvod atmosferskih voda',
                         'PTT i telekomunikaciona mreža, optički kablovi']))], width=50, tablet_width=50, gap_d=12,
                cls='t-group'),
            box([txt('<p>B</p>', 't-index'), h('Grubi građevinski radovi', 'h3', 't-h3'),
                 txt(ul(['Raščišćavanje terena',
                         'Iskop i zatrpavanje rovova',
                         'Odvoz i dovoz zemlje i građevinskog materijala',
                         'Razbijanje i sečenje betona i asfalta',
                         'Podbušivanje, uključujući HD podbušivanje ispod reka',
                         'Mašinsko nabijanje zemlje i peska u rov']))], width=50, tablet_width=50, gap_d=12,
                cls='t-group'),
        ], width=66, tablet_width=100, direction='row', tablet_dir='row', gap_d=40),
    ], cls='t-services', bg='#FAF8F4', direction='row', tablet_dir='column', gap_d=64)

    ledger = section([
        box([eyebrow('Izabrani radovi'), h('Iz referentne liste', 'h2', 't-h2'),
             txt('<p>Izbor iz 135 radova koje smo evidentirali od 1998. do 2018. godine.</p>')],
            width=70, tablet_width=100, gap_d=16),
        box([
            ledger_row('2017–2018', 'Gasovod visokog pritiska Šepak–Bijeljina', 'Republika Srpska, BiH',
                       'Sa HD podbušivanjem reka Janja, Dašnica i Pilica'),
            ledger_row('2009–2018', 'Distributivna gasna mreža Bijeljina', 'Bijeljina, BiH',
                       '171,3 km evidentirano u periodu 2009–2012.'),
            ledger_row('2002–2003', 'Gasovod srednjeg pritiska Rumenka–Kisač, „Severni krak“', 'Novi Sad',
                       '38.900 m'),
            ledger_row('2002–2003', 'Gasovod u podgrađu Petrovaradinske tvrđave', 'Petrovaradin',
                       '1.600 m, celokupna gasna mreža u istorijskom delu grada'),
            ledger_row('2017–2018', 'Glavne merno-regulacione stanice (GMRS)', 'Obrovac, Bijeljina',
                       'GMRS Obrovac 2017, GMRS Bijeljina 2018.'),
            ledger_row('2007', 'Gasovod Bačka Topola–Feketić i gasne mreže Feketić, Lovćenac i Mali Iđoš',
                       'Bačka Topola, Mali Iđoš', '20.230 m gasovoda i 90.535 m mreže'),
        ], cls='t-ledger', gap_d=0),
        btn('Sve reference 1998–2018', '/reference/', 'secondary'),
    ], cls='t-featured', bg='#F2EEE6', gap_d=40)

    total = documented_total()
    evidence = section([
        box([eyebrow('Evidentirane dužine'),
             txt(f'<p class="t-figure">{km(total, 0)}</p>'),
             txt('<p>Zbir dužina gasovoda i mreža navedenih u našoj referentnoj listi za period 1998–2012. '
                 'Za kasnije godine lista ne navodi dužine, pa one nisu uračunate.</p>', 't-muted')],
            width=38, tablet_width=100, gap_d=16),
        box([html(length_chart())], width=62, tablet_width=100),
    ], cls='t-evidence t-on-dark', bg='#1C1D1B', direction='row', tablet_dir='column', gap_d=64, align='center')

    partner = section([
        box([eyebrow('Saradnja'),
             h('Dugogodišnja saradnja sa Novi Sad Gasom', 'h2', 't-h2'),
             txt('<p>Sa investitorom Novi Sad Gas ostvarili smo dugogodišnju saradnju kao glavni izvođač građevinskih radova na dovodnim '
                 'gasovodima, distributivnim gasnim mrežama i kućnim gasnim priključcima — na teritoriji Novog Sada, '
                 'Bačkog Petrovca, Bačke Palanke, Beočina, Sremskih Karlovaca, Bukovca i drugih mesta.</p>'
                 '<p>Među gasnim mrežama koje smo izveli u Novom Sadu su Sajlovo, Šumice, Lipov Gaj, Veternička rampa, '
                 'Adice i ulica Novosadskog sajma.</p>')],
            width=50, tablet_width=100, gap_d=20),
        box([h('Primer: podgrađe Petrovaradinske tvrđave', 'h3', 't-h3'),
             txt('<p>Celokupnu gasnu mrežu u podgrađu izveli smo u gusto izgrađenom, istorijskom delu grada. '
                 'Posao je obuhvatio:</p>'
                 '<ol class="t-steps"><li>obezbeđivanje gradilišta</li><li>vađenje starih betonskih kocki</li>'
                 '<li>iskop kanala</li><li>postavljanje cevi</li><li>mašinsko nabijanje peska i zemlje</li>'
                 '<li>zatrpavanje kanala</li><li>dovođenje terena u prvobitno stanje</li></ol>')],
            width=50, tablet_width=100, gap_d=16, cls='t-casebox'),
    ], cls='t-partner', bg='#FAF8F4', direction='row', tablet_dir='column', gap_d=64)

    machines = section([
        box([eyebrow('Mehanizacija'), h('Sopstveni mašinski park', 'h2', 't-h2'),
             txt('<p>Bageri rovokopači-utovarivači, mini bageri, alati za sečenje, razbijanje i nabijanje '
                 'i vozila za prevoz materijala i ekipa.</p>'),
             btn('Kompletna lista mehanizacije', '/mehanizacija/', 'text')], width=40, tablet_width=100, gap_d=20),
        box([
            box([h('Bageri rovokopači-utovarivači', 'h3', 't-h4'),
                 txt(ul(['JCB 4CX <em>2 kom.</em>', 'JCB 3CX <em>2 kom.</em>', 'Takeuchi TB1140 <em>1 kom.</em>'],
                        't-spec'))], width=50, tablet_width=50, gap_d=12),
            box([h('Mini bageri', 'h3', 't-h4'),
                 txt(ul(['JCB 8018 <em>1 kom.</em>', 'Takeuchi TB 235 <em>3 kom.</em>'], 't-spec'))],
                width=50, tablet_width=50, gap_d=12),
        ], width=60, tablet_width=100, direction='row', tablet_dir='row', gap_d=40),
    ], cls='t-machines', bg='#F2EEE6', direction='row', tablet_dir='column', gap_d=64)

    return [intro, services, ledger, evidence, partner, machines, contact_band()]


# --------------------------------------------------------------------------- DELATNOSTI
def delatnosti():
    def block(no, title, text, examples):
        ex = ''
        if examples:
            ex = '<p class="t-exlabel">Iz referenci</p>' + ul(examples, 't-reflist')
        return section([
            box([txt(f'<p>{no}</p>', 't-index'), h(title, 'h2', 't-h2 t-h2--s')], width=36, tablet_width=100, gap_d=12),
            box([txt(text), txt(ex)] if ex else [txt(text)], width=64, tablet_width=100, gap_d=20),
        ], cls='t-service', bg='#FAF8F4', direction='row', tablet_dir='column', gap_d=48,
            pad_d=(64, 24, 64, 24), pad_t=(56, 24, 56, 24), pad_m=(44, 20, 44, 20))

    return [
        page_head('Delatnosti', 'Šta izvodimo',
                  'Specijalizovani smo za grube građevinske radove i specifične radove niskogradnje — pre svega za '
                  'izgradnju gasovoda i gasnih mreža, ali i vodovodne, toplovodne, PTT i atmosferske mreže.'),
        block('01', 'Gasovodi visokog i srednjeg pritiska',
              '<p>Izvodimo građevinske radove na magistralnim i dovodnim gasovodima i gasovodima visokog i srednjeg '
              'pritiska, uključujući prelaze ispod vodotokova.</p>',
              ['Gasovod visokog pritiska Šepak–Bijeljina <em>2017–2018</em>',
               'Gasovod visokog pritiska Bačka Palanka–Bač <em>2016–2017</em>',
               'Gasovod srednjeg pritiska Rumenka–Kisač, „Severni krak“ <em>38.900 m</em>',
               'Gasovod srednjeg pritiska Čerević–Banoštor–Susek <em>21.300 m</em>',
               'Gasovod srednjeg pritiska Bačka Topola–Feketić <em>20.230 m</em>']),
        block('02', 'Distributivne gasne mreže i kućni priključci',
              '<p>Najveći deo naših referenci čine distributivne gasne mreže u naseljima — od iskopa i polaganja '
              'cevi do kućnih gasnih priključaka i dovođenja terena u prvobitno stanje.</p>',
              ['Distributivna gasna mreža Bijeljina (BiH) <em>2009–2018</em>',
               'Distributivna gasna mreža Bački Petrovac <em>47.000 m</em>',
               'Distributivna gasna mreža Mali Iđoš <em>46.900 m</em>',
               'Distributivna gasna mreža Kisač <em>41.000 m</em>',
               'Distributivna gasna mreža Kovilj <em>40.100 m</em>',
               'Novi Sad: Sajlovo, Šumice, Lipov Gaj, Veternička rampa, Adice, Petrovaradin']),
        block('03', 'Merno-regulacione stanice i prateći objekti',
              '<p>Na gasnim sistemima izvodimo i građevinske radove na objektima: glavnim merno-regulacionim '
              'stanicama, otpremno-čistačkim mestima i priključnim gasovodima.</p>',
              ['Glavna merno-regulaciona stanica (GMRS) Bijeljina <em>2018</em>',
               'Glavna merno-regulaciona stanica (GMRS) Obrovac <em>2017</em>',
               'Otpremno-čistačko mesto Gajdobra <em>2018</em>',
               'Gasovod TNG Elemir do RUS-6 i RUS-10, Rusanda <em>2013</em>']),
        block('04', 'Vodovod, toplovod i atmosferska kanalizacija',
              '<p>Gradimo vodovodnu i toplovodnu mrežu i mrežu za odvod atmosferskih voda.</p>',
              ['Vodovodna mreža Bečej <em>4.228 m</em>',
               'Vodovodna mreža Susek <em>2.900 m</em>',
               'Vodovodna mreža Čenej <em>2.700 m</em>',
               'Toplovod za stambene objekte u ulicama Danila Kiša i Kornelija Stankovića, investitor „Greping“ <em>1999–2000</em>',
               'Mreža za atmosferske vode Bački Petrovac, Maglić i Gložan <em>2006</em>']),
        block('05', 'Telekomunikacione mreže',
              '<p>Izvodimo građevinske radove za PTT i telekomunikacione mreže, uključujući polaganje optičkih kablova.</p>',
              ['Telekomunikaciona mreža (optički kabl) Bijeljina–Šepak <em>2017–2018</em>',
               'Priključni gasovod, vodovodna i PTT instalacija, Centar za privredno-tehnološki razvoj Andrevlje <em>6.000 m</em>']),
        block('06', 'Podbušivanje',
              '<p>Podbušivanjem se cevi i kablovi polažu ispod prepreka bez otvaranja površine. '
              'Na gasovodu Šepak–Bijeljina izveli smo HD podbušivanje ispod reka.</p>',
              ['HD podbušivanje reka Janja, Dašnica i Pilica, gasovod visokog pritiska Šepak–Bijeljina <em>2018</em>']),
        block('07', 'Grubi građevinski radovi',
              ul(['Raščišćavanje terena', 'Iskop i zatrpavanje rovova',
                  'Odvoz i dovoz zemlje i građevinskog materijala', 'Razbijanje i sečenje betona i asfalta',
                  'Podbušivanje', 'Mašinsko nabijanje zemlje i peska u rov']),
              ['Sanacija deponije otpadaka u Adi <em>2010</em>']),
        block('08', 'Ostali građevinski objekti',
              '<p>Pored mreža, izvodili smo i radove na pojedinačnim objektima.</p>',
              ['Zidana trafo stanica ZTS „7“ u krugu „Koteks-Viskofan“ d.o.o., Novi Sad <em>2018</em>',
               'Proizvodno-klanička hala za „Zmajevac“ d.o.o., Irig <em>2015</em>',
               'Centralni magacin opreme za odbranu od poplava JVP „Vode Vojvodine“, Novi Sad <em>2012</em>']),
        section([
            box([eyebrow('Redosled radova'), h('Kako izgleda posao na rovu', 'h2', 't-h2'),
                 txt('<p>Na gradskim gradilištima, kao u podgrađu Petrovaradinske tvrđave, radovi idu ovim redom — '
                     'a završavaju se tek kada je površina vraćena u stanje u kakvom smo je zatekli.</p>')],
                width=40, tablet_width=100, gap_d=20),
            box([html(trench_svg())], width=60, tablet_width=100),
        ], cls='t-process', bg='#F2EEE6', direction='row', tablet_dir='column', gap_d=64, align='center'),
        contact_band(),
    ]


# --------------------------------------------------------------------------- REFERENCE
def reference():
    years = [g['period'] for g in REFS]
    jump = '<nav class="t-jump" aria-label="Godine">' + ''.join(
        f'<a href="#g{p[:4]}">{p}</a>' for p in years) + '</nav>'
    blocks = [page_head('Reference', 'Reference 1998–2018',
                        'Kompletna lista radova koje smo evidentirali, po godinama. Dužine su navedene prema evidenciji '
                        'preduzeća. Za radove posle 2012. godine dužine nisu navedene.',
                        extra=[html(jump)])]
    rows = []
    for g in REFS:
        items = []
        for i in g['items']:
            t = i['title']
            if i.get('note'):
                t += f' ({i["note"]})'
            if i.get('length'):
                t += f' <em>{i["length"]}</em>'
            items.append(t)
        n = len(g['items'])
        count = f'{n} {"rad" if n % 10 == 1 and n % 100 != 11 else ("rada" if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14) else "radova")}'
        row = box([
            box([h(g['period'], 'h2', 't-year'), txt(f'<p>{count}</p>', 't-year__count')], width=24,
                tablet_width=24, gap_d=4, cls='t-year__head'),
            box([txt(ul(items, 't-reflist'))], width=76, tablet_width=76),
        ], direction='row', tablet_dir='row', gap_d=32, cls='t-yearrow')
        row['settings']['_element_id'] = 'g' + g['period'][:4]
        rows.append(row)
    blocks.append(section(rows, cls='t-years', bg='#FAF8F4', gap_d=0, pad_d=(24, 24, 96, 24),
                          pad_t=(16, 24, 72, 24), pad_m=(8, 20, 56, 20)))
    blocks.append(contact_band())
    return blocks


# --------------------------------------------------------------------------- MEHANIZACIJA
def mehanizacija():
    def group(title, items, note=''):
        content = [h(title, 'h2', 't-h3'), txt(ul(items, 't-spec'))]
        if note:
            content.append(txt(f'<p>{note}</p>', 't-muted'))
        return box(content, width=50, tablet_width=50, gap_d=16, cls='t-group')

    return [
        page_head('Mehanizacija', 'Mašinski park i vozila',
                  'Radove izvodimo sopstvenom mehanizacijom. U našem mašinskom parku su bageri rovokopači-utovarivači '
                  'i mini bageri rovokopači, uz alate i mašine za sečenje, razbijanje, bušenje i nabijanje.'),
        section([
            box([group('Bageri rovokopači-utovarivači',
                       ['JCB 4CX <em>2 kom.</em>', 'JCB 3CX <em>2 kom.</em>', 'Takeuchi TB1140 <em>1 kom.</em>']),
                 group('Mini bageri rovokopači',
                       ['JCB 8018 <em>1 kom.</em>', 'Takeuchi TB 235 <em>3 kom.</em>'])],
                direction='row', tablet_dir='row', gap_d=48),
            box([group('Alati i mašine',
                       ['Vibro-ploča Bomag BT 60/4', 'Pneumatski čekić Bosch GSH27 <em>2 kom.</em>',
                        'Pneumatska štemalica Hitachi H90', 'Kompresorska stanica Hycon HPP13',
                        'Sekač asfalta Norton Clipper C99', 'Mašina za sečenje betona i asfalta Gölz FS170',
                        'Vibronabijač Wacker Neuson', 'Mašina za podbušivanje sa spiralom',
                        'Kärcher HD 7/18', 'Mešalica za malter']),
                 group('Vozni park',
                       ['Daimler Chrysler 970 – Atego 1015 <em>kiper</em>', 'Mercedes 1117 L <em>kiper</em>',
                        'TAM 80T 5BK', 'Iveco Daily 50C', 'Iveco Daily 35S', 'GAZ 3302', 'GAZ Cab 112',
                        'VW Transporter T5 <em>furgon</em>', 'VW Caddy <em>furgon</em>',
                        'Opel Combo-C <em>pick-up</em>', 'Renault Kangoo <em>pick-up</em>', 'Dacia Duster'])],
                direction='row', tablet_dir='row', gap_d=48),
        ], cls='t-fleet', bg='#FAF8F4', gap_d=72),
        contact_band(),
    ]


# --------------------------------------------------------------------------- O NAMA
def o_nama():
    timeline = [
        ('1997.', 'Osnivanje preduzeća u Novom Sadu.'),
        ('1998.', 'Distributivne gasne mreže Gložan, Čardak, Bocke i Petrovaradin — prvi radovi na referentnoj listi.'),
        ('1999–2000.', 'Toplovod za stambene objekte u ulicama Danila Kiša i Kornelija Stankovića, za investitora „Greping“.'),
        ('2002–2003.', 'Gasovod srednjeg pritiska Rumenka–Kisač i gasna mreža u podgrađu Petrovaradinske tvrđave.'),
        ('2007.', 'Gasovod Bačka Topola–Feketić i gasne mreže Feketić, Lovćenac i Mali Iđoš.'),
        ('2009.', 'Početak radova na distributivnoj gasnoj mreži Bijeljine (BiH).'),
        ('2017–2018.', 'Gasovod visokog pritiska Šepak–Bijeljina sa HD podbušivanjem reka, GMRS Obrovac i Bijeljina.'),
    ]
    tl = '<ol class="t-timeline">' + ''.join(
        f'<li><span class="t-timeline__y">{y}</span><span class="t-timeline__t">{t}</span></li>' for y, t in timeline) + '</ol>'
    company = ('<dl class="t-dl">'
               '<dt>Naziv</dt><dd>Građevinsko preduzeće „24. Oktobar“ d.o.o.</dd>'
               '<dt>Sedište</dt><dd>Temerinska 50, 21000 Novi Sad, Srbija</dd>'
               '<dt>Osnovano</dt><dd>1997.</dd>'
               '<dt>PIB</dt><dd>101 699 336</dd>'
               '<dt>Matični broj</dt><dd>0866 4102</dd>'
               '<dt>Radno vreme</dt><dd>Ponedeljak–petak, 08:00–15:00</dd>'
               '</dl>')
    return [
        page_head('O nama', 'Građevinsko preduzeće iz Novog Sada, od 1997. godine',
                  'Građevinsko preduzeće „24. Oktobar“ d.o.o. osnovano je 1997. godine u Novom Sadu. '
                  'Specijalizovani smo za grube građevinske radove i specifične radove niskogradnje.'),
        section([
            box([eyebrow('Rad'), h('Gasifikacija kao stalno otvoreno gradilište', 'h2', 't-h2')],
                width=40, tablet_width=100, gap_d=16),
            box([txt('<p>Najveći deo našeg rada vezan je za gasifikaciju Novog Sada i okolnih naselja. Sa investitorom '
                     'Novi Sad Gas ostvarili smo dugogodišnju saradnju kao glavni izvođač građevinskih radova na dovodnim gasovodima, '
                     'distributivnim gasnim mrežama i kućnim gasnim priključcima — na teritoriji Novog Sada, Bačkog '
                     'Petrovca, Bačke Palanke, Beočina, Sremskih Karlovaca, Bukovca i drugih mesta.</p>'
                     '<p>U gradskim uslovima organizovali smo niz zahtevnih gradilišta. U podgrađu Petrovaradinske '
                     'tvrđave izveli smo celokupnu gasnu mrežu: od obezbeđivanja gradilišta i vađenja starih betonskih '
                     'kocki, preko iskopa kanala, postavljanja cevi i mašinskog nabijanja peska i zemlje, do zatrpavanja '
                     'kanala i dovođenja terena u prvobitno stanje.</p>'
                     '<p>Pored gasnih mreža, gradili smo toplovod za investitora „Greping“ iz Novog Sada, vodovodne mreže '
                     'u Bečeju, Suseku i Čeneju i mreže za odvod atmosferskih voda u Bačkom Petrovcu, Magliću i Gložanu. '
                     'Od 2009. godine radimo i u Bijeljini (BiH), gde smo gradili distributivnu gasnu mrežu, gasovod '
                     'visokog pritiska Šepak–Bijeljina i telekomunikacionu mrežu.</p>', 't-prose')],
                width=60, tablet_width=100),
        ], cls='t-about', bg='#FAF8F4', direction='row', tablet_dir='column', gap_d=64),
        section([
            box([eyebrow('Hronologija'), h('Nekoliko tačaka iz referentne liste', 'h2', 't-h2')],
                width=40, tablet_width=100, gap_d=16),
            box([html(tl)], width=60, tablet_width=100),
        ], cls='t-chrono', bg='#F2EEE6', direction='row', tablet_dir='column', gap_d=64),
        section([
            box([eyebrow('Podaci o preduzeću'), h('Osnovni podaci', 'h2', 't-h2')], width=40, tablet_width=100,
                gap_d=16),
            box([txt(company)], width=60, tablet_width=100),
        ], cls='t-company', bg='#FAF8F4', direction='row', tablet_dir='column', gap_d=64),
        contact_band(),
    ]


# --------------------------------------------------------------------------- KONTAKT
def kontakt():
    phones = ('<ul class="t-contactlist">'
              f'<li><span>Telefon / faks</span><a href="{PHONE_MAIN[1]}">{PHONE_MAIN[0]}</a></li>'
              f'<li><span>Telefon</span><a href="{PHONE_2[1]}">{PHONE_2[0]}</a></li>'
              f'<li><span>Telefon</span><a href="{PHONE_3[1]}">{PHONE_3[0]}</a></li>'
              f'<li><span>Mobilni</span><a href="{MOBILE[1]}">{MOBILE[0]}</a></li>'
              f'<li><span>E-pošta</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>'
              '</ul>')
    address = ('<p class="t-address">Temerinska 50<br>21000 Novi Sad<br>Srbija</p>')
    return [
        page_head('Kontakt', 'Pozovite nas ili pišite',
                  'Pozovite nas radnim danima od 08:00 do 15:00 ili nam pišite na e-poštu.'),
        section([
            box([h('Telefoni i e-pošta', 'h2', 't-h3'), txt(phones)], width=58, tablet_width=100, gap_d=20),
            box([h('Adresa', 'h2', 't-h3'), txt(address),
                 btn('Prikaži na mapi', MAP_URL, 'secondary'),
                 h('Radno vreme', 'h2', 't-h3 t-mt'), txt('<p>Ponedeljak–petak<br>08:00–15:00</p>'),
                 h('Podaci o preduzeću', 'h2', 't-h3 t-mt'),
                 txt('<p>Građevinsko preduzeće „24. Oktobar“ d.o.o.<br>PIB 101 699 336<br>Matični broj 0866 4102</p>',
                     't-muted-light')],
                width=42, tablet_width=100, gap_d=16, cls='t-contactside'),
        ], cls='t-contact', bg='#FAF8F4', direction='row', tablet_dir='column', gap_d=64),
    ]


PAGES = [
    # slug, title, builder, SEO title, meta description, menu order
    ('pocetna', 'Početna', home,
     'Gasovodi, gasne mreže i niskogradnja, Novi Sad | „24. Oktobar“ d.o.o.',
     'Građevinsko preduzeće „24. Oktobar“ iz Novog Sada od 1997. izvodi gasovode, distributivne gasne mreže, '
     'vodovod, toplovod i PTT mrežu, kao i grube građevinske radove.'),
    ('delatnosti', 'Delatnosti', delatnosti,
     'Delatnosti — gasovodi, mreže i grubi građevinski radovi | „24. Oktobar“',
     'Gasovodi visokog i srednjeg pritiska, distributivne gasne mreže, GMRS, vodovod, toplovod, atmosferska '
     'kanalizacija, PTT mreže, podbušivanje i grubi građevinski radovi.'),
    ('reference', 'Reference', reference,
     'Reference 1998–2018 | „24. Oktobar“ d.o.o. Novi Sad',
     'Kompletna lista od 135 radova 1998–2018: gasovodi i gasne mreže u Vojvodini i Bijeljini, vodovodne mreže, '
     'GMRS, telekomunikacione mreže i objekti.'),
    ('mehanizacija', 'Mehanizacija', mehanizacija,
     'Mehanizacija — bageri, alati i vozila | „24. Oktobar“ d.o.o.',
     'Bageri rovokopači-utovarivači JCB 4CX i 3CX, mini bageri JCB i Takeuchi, alati za sečenje, razbijanje i '
     'nabijanje i vozni park preduzeća „24. Oktobar“.'),
    ('o-nama', 'O nama', o_nama,
     'O nama — građevinsko preduzeće iz Novog Sada od 1997. | „24. Oktobar“',
     'Građevinsko preduzeće „24. Oktobar“ d.o.o. osnovano je 1997. u Novom Sadu. Dugogodišnji glavni izvođač '
     'građevinskih radova za Novi Sad Gas.'),
    ('kontakt', 'Kontakt', kontakt,
     'Kontakt | „24. Oktobar“ d.o.o., Temerinska 50, Novi Sad',
     'Temerinska 50, 21000 Novi Sad. Tel. +381 21 47 41 048, mob. +381 63 503 333, '
     'e-pošta 24oktobar.ns@gmail.com. Radno vreme pon–pet 08–15.'),
]

if __name__ == '__main__':
    manifest = []
    for slug, title, fn, seo_title, seo_desc in PAGES:
        data = fn()
        with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        manifest.append({'slug': slug, 'title': title, 'seo_title': seo_title, 'seo_desc': seo_desc})
    with open(os.path.join(OUT, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print('built', [m['slug'] for m in manifest], 'documented total', km(documented_total(), 0))
