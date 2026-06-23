#!/usr/bin/env python3
"""Generate A5 cocktail menu HTML — near-black background, gold + pink botanical style."""
import base64, os

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

lr = b64('/tmp/fonts/lora-regular.ttf')
lb = b64('/tmp/fonts/lora-bold.ttf')
li = b64('/tmp/fonts/lora-italic.ttf')
pl = b64('/tmp/fonts/poppins-light.ttf')

# ─── Colour tokens ─────────────────────────────────────────────────────────────
G  = '#D4C890'   # main gold line
G2 = '#E0D4A0'   # gold highlight
G3 = '#B8A868'   # gold shadow
P  = '#D4829A'   # pink (flowers, hearts)
P2 = '#EBB8CA'   # pink highlight
SW = '0.70'

# ─── Petal helper ──────────────────────────────────────────────────────────────
def petal_path(r, wf=0.42):
    w = r * wf
    return (f"M 0,0 C {w*0.8:.2f},{-r*0.08:.2f} {w:.2f},{-r*0.58:.2f} 0,{-r:.2f} "
            f"C {-w:.2f},{-r*0.58:.2f} {-w*0.8:.2f},{-r*0.08:.2f} 0,0 Z")

def petal_ring(n, r, wf, offset, color=None, alpha='0.18', sw=None):
    if color is None: color = G
    if sw is None: sw = SW
    step = 360 / n
    out = []
    for i in range(n):
        a = offset + step * i
        out.append(
            f'<path d="{petal_path(r,wf)}" '
            f'fill="{color}" fill-opacity="{alpha}" '
            f'stroke="{color}" stroke-width="{sw}" '
            f'transform="rotate({a:.1f})"/>'
        )
    return "\n".join(out)

# ─── Gold botanical symbols ────────────────────────────────────────────────────
WF5 = f"""<symbol id="wf5" viewBox="-12 -12 24 24" overflow="visible">
  {petal_ring(5, 10, 0.45, 0)}
  <circle r="2.2" fill="{G}"/>
  <circle r="1" fill="{G2}"/>
</symbol>"""

WF5B = f"""<symbol id="wf5b" viewBox="-12 -12 24 24" overflow="visible">
  {petal_ring(5, 10, 0.45, 0)}
  {petal_ring(5, 7, 0.40, 36)}
  <circle r="2" fill="{G}"/>
</symbol>"""

WF8 = f"""<symbol id="wf8" viewBox="-14 -14 28 28" overflow="visible">
  {petal_ring(8, 11, 0.38, 0)}
  {petal_ring(8, 7,  0.35, 22.5)}
  <circle r="2.8" fill="{G}" stroke="{G3}" stroke-width="0.4"/>
  <circle r="1.2" fill="{G2}"/>
</symbol>"""

BUD = f"""<symbol id="bud" viewBox="-5 -14 10 16" overflow="visible">
  <line x1="0" y1="2" x2="0" y2="-6" stroke="{G}" stroke-width="0.6"/>
  <path d="M 0,-6 C 3,-8 4,-12 0,-13 C -4,-12 -3,-8 0,-6 Z"
        fill="{G}" fill-opacity="0.25" stroke="{G}" stroke-width="0.6"/>
  <path d="M -1,-7 Q -4,-8 -3,-6" stroke="{G}" stroke-width="0.4" fill="none"/>
  <path d="M  1,-7 Q  4,-8  3,-6" stroke="{G}" stroke-width="0.4" fill="none"/>
</symbol>"""

BERRIES = f"""<symbol id="berries" viewBox="-14 -20 28 22" overflow="visible">
  <path d="M 0,2 Q 0,-4, 0,-10" stroke="{G}" stroke-width="0.65" fill="none"/>
  <path d="M 0,-7 Q -5,-8, -8,-12" stroke="{G}" stroke-width="0.55" fill="none"/>
  <path d="M 0,-7 Q  5,-8,  8,-12" stroke="{G}" stroke-width="0.55" fill="none"/>
  <circle cx="0"  cy="-13" r="2.8" fill="{G}" fill-opacity="0.7" stroke="{G}" stroke-width="0.5"/>
  <circle cx="-8" cy="-13" r="2.2" fill="{G}" fill-opacity="0.6" stroke="{G}" stroke-width="0.5"/>
  <circle cx="8"  cy="-13" r="2.2" fill="{G}" fill-opacity="0.6" stroke="{G}" stroke-width="0.5"/>
  <circle cx="-0.8" cy="-14.2" r="0.6" fill="{G2}" opacity="0.8"/>
  <circle cx="-8.8" cy="-14"   r="0.5" fill="{G2}" opacity="0.7"/>
  <circle cx="7.2"  cy="-14"   r="0.5" fill="{G2}" opacity="0.7"/>
</symbol>"""

BRANCH = f"""<symbol id="branch" viewBox="-16 -26 32 28" overflow="visible">
  <path d="M 0,2 Q 2,-8, 0,-24" stroke="{G}" stroke-width="0.65" fill="none"/>
  <path d="M 0,-5  Q -9,-7, -11,-13 Q -5,-9, 0,-5"
        fill="{G}" fill-opacity="0.18" stroke="{G}" stroke-width="0.55"/>
  <path d="M 0,-5  Q  9,-7,  11,-13 Q  5,-9, 0,-5"
        fill="{G}" fill-opacity="0.15" stroke="{G}" stroke-width="0.50"/>
  <path d="M 0,-12 Q -10,-14, -12,-20 Q -5,-15, 0,-12"
        fill="{G}" fill-opacity="0.18" stroke="{G}" stroke-width="0.55"/>
  <path d="M 0,-12 Q  10,-14,  12,-20 Q  5,-15, 0,-12"
        fill="{G}" fill-opacity="0.15" stroke="{G}" stroke-width="0.50"/>
  <path d="M 0,-20 Q 4,-22, 2,-26 Q -2,-22, 0,-20"
        fill="{G}" fill-opacity="0.20" stroke="{G}" stroke-width="0.55"/>
</symbol>"""

HERB = f"""<symbol id="herb" viewBox="-8 -22 16 24" overflow="visible">
  <path d="M 0,2 L 0,-20" stroke="{G}" stroke-width="0.60" fill="none"/>
  <path d="M 0,-5  Q -6,-6, -7,-9  Q -3,-7, 0,-5"  fill="{G}" fill-opacity="0.2" stroke="{G}" stroke-width="0.45"/>
  <path d="M 0,-5  Q  6,-6,  7,-9  Q  3,-7, 0,-5"  fill="{G}" fill-opacity="0.15" stroke="{G}" stroke-width="0.40"/>
  <path d="M 0,-10 Q -5,-11,-6,-14 Q -2,-12, 0,-10" fill="{G}" fill-opacity="0.2" stroke="{G}" stroke-width="0.45"/>
  <path d="M 0,-10 Q  5,-11, 6,-14 Q  2,-12, 0,-10" fill="{G}" fill-opacity="0.15" stroke="{G}" stroke-width="0.40"/>
  <path d="M 0,-15 Q -4,-16,-5,-19 Q -1,-17, 0,-15" fill="{G}" fill-opacity="0.2" stroke="{G}" stroke-width="0.40"/>
  <path d="M 0,-15 Q  4,-16, 5,-19 Q  1,-17, 0,-15" fill="{G}" fill-opacity="0.15" stroke="{G}" stroke-width="0.35"/>
  <circle cx="0" cy="-20" r="1.5" fill="{G}"/>
</symbol>"""

TINY = f"""<symbol id="tiny" viewBox="-7 -7 14 14" overflow="visible">
  {petal_ring(5, 5.5, 0.42, 0)}
  <circle r="1.4" fill="{G}"/>
</symbol>"""

TENDRIL = f"""<symbol id="tendril" viewBox="-10 -20 20 22" overflow="visible">
  <path d="M 0,2 Q -8,0, -6,-6 Q -4,-12, 0,-14 Q 4,-16, 2,-20"
        stroke="{G}" stroke-width="0.55" fill="none" stroke-linecap="round"/>
  <path d="M -5,-3 Q -10,-2, -10,-6 Q -7,-4, -5,-3" fill="{G}" fill-opacity="0.18" stroke="{G}" stroke-width="0.40"/>
  <path d="M -4,-10 Q -9,-11,-8,-15 Q -5,-12,-4,-10" fill="{G}" fill-opacity="0.18" stroke="{G}" stroke-width="0.40"/>
</symbol>"""

# ─── Pink botanical symbols ────────────────────────────────────────────────────
PINK_WF5 = f"""<symbol id="pink-wf5" viewBox="-12 -12 24 24" overflow="visible">
  {petal_ring(5, 9, 0.45, 0, P, '0.50', '0.60')}
  <circle r="2" fill="{P}"/>
  <circle r="0.9" fill="{P2}"/>
</symbol>"""

PINK_TINY = f"""<symbol id="pink-tiny" viewBox="-7 -7 14 14" overflow="visible">
  {petal_ring(5, 5.5, 0.42, 0, P, '0.55', '0.55')}
  <circle r="1.3" fill="{P}"/>
</symbol>"""

PINK_BLOOM = f"""<symbol id="pink-bloom" viewBox="-9 -22 18 24" overflow="visible">
  <path d="M 0,2 Q 1,-3 0,-8" stroke="{P}" stroke-width="0.50" fill="none"/>
  <path d="M 0,-5 Q -4,-5 -4.5,-8 Q -1,-6 0,-5" fill="{P}" fill-opacity="0.20" stroke="{P}" stroke-width="0.35"/>
  <path d="M 0,-5 Q  4,-5  4.5,-8 Q  1,-6 0,-5" fill="{P}" fill-opacity="0.15" stroke="{P}" stroke-width="0.30"/>
  <g transform="translate(0,-11)">
    {petal_ring(5, 7, 0.45, 0, P, '0.50', '0.58')}
    <circle r="1.8" fill="{P}"/>
    <circle r="0.7" fill="{P2}"/>
  </g>
</symbol>"""

PINK_HEART = f"""<symbol id="pink-heart" viewBox="-5 -6 10 11" overflow="visible">
  <path d="M 0,4 C -0.5,2 -4.5,0.5 -4.5,-1.5
           C -4.5,-4.2 -2,-5.5 0,-3.2
           C 2,-5.5 4.5,-4.2 4.5,-1.5
           C 4.5,0.5 0.5,2 0,4 Z"
        fill="{P}" fill-opacity="0.72" stroke="{P2}" stroke-width="0.28"/>
</symbol>"""

# ─── Sketch filters ────────────────────────────────────────────────────────────
FILTERS = f"""
  <filter id="sketch" x="-30%" y="-30%" width="160%" height="160%">
    <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="7" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="2.3" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="sketch-b" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="0.9" xChannelSelector="R" yChannelSelector="G"/>
  </filter>"""

# ─── Glassware ─────────────────────────────────────────────────────────────────
SK  = G
SKW = '0.80'

MARTINI = f"""<symbol id="martini" viewBox="-17 -40 34 44" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <line x1="-14" y1="-36" x2="14" y2="-36"/>
    <line x1="-14" y1="-36" x2="0"  y2="-20"/>
    <line x1="14"  y1="-36" x2="0"  y2="-20"/>
    <line x1="0"   y1="-20" x2="0"  y2="-3"/>
    <line x1="-10" y1="-3"  x2="10" y2="-3"/>
    <circle cx="0" cy="-30" r="2.2" stroke="{G3}" stroke-width="0.55"/>
    <line x1="0" y1="-27.8" x2="0" y2="-34" stroke="{G3}" stroke-width="0.45"/>
  </g>
</symbol>"""

COUPE = f"""<symbol id="coupe" viewBox="-17 -36 34 40" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -15,-32 Q -10,-24 0,-22 Q 10,-24 15,-32"/>
    <line x1="-15" y1="-32" x2="15" y2="-32"/>
    <line x1="0" y1="-22" x2="0" y2="-4"/>
    <line x1="-9" y1="-4" x2="9" y2="-4"/>
  </g>
</symbol>"""

WINE_GLASS = f"""<symbol id="wine-glass" viewBox="-13 -44 26 48" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -10,-40 Q -12,-28 -6,-23 Q -3,-20 0,-20 Q 3,-20 6,-23 Q 12,-28 10,-40"/>
    <line x1="-10" y1="-40" x2="10" y2="-40"/>
    <path d="M -7.5,-30 Q 0,-28.5 7.5,-30" stroke="{G3}" stroke-width="0.45" opacity="0.8"/>
    <line x1="0" y1="-20" x2="0" y2="-4"/>
    <line x1="-8" y1="-4" x2="8" y2="-4"/>
  </g>
</symbol>"""

NICK_NORA = f"""<symbol id="nick-nora" viewBox="-14 -40 28 44" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -10,-36 Q -12,-28 -7,-23 Q -3,-20 0,-20 Q 3,-20 7,-23 Q 12,-28 10,-36"/>
    <line x1="-10" y1="-36" x2="10" y2="-36"/>
    <line x1="0" y1="-20" x2="0" y2="-4"/>
    <line x1="-8" y1="-4" x2="8" y2="-4"/>
  </g>
</symbol>"""

HIGHBALL = f"""<symbol id="highball" viewBox="-11 -42 32 46" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -8,-38 L -9,2 L 9,2 L 8,-38 Z"/>
    <line x1="4" y1="-40" x2="2" y2="2" stroke="{SK}" stroke-width="0.75" opacity="0.9"/>
    <circle cx="-2" cy="-36" r="4" stroke="{G3}" stroke-width="0.55" opacity="0.85"/>
    <line x1="-2" y1="-40" x2="-2" y2="-32" stroke="{G3}" stroke-width="0.40" opacity="0.65"/>
    <line x1="-6" y1="-36" x2="2"  y2="-36" stroke="{G3}" stroke-width="0.40" opacity="0.65"/>
    <line x1="-5" y1="-39" x2="1"  y2="-33" stroke="{G3}" stroke-width="0.30" opacity="0.55"/>
    <line x1="-5" y1="-33" x2="1"  y2="-39" stroke="{G3}" stroke-width="0.30" opacity="0.55"/>
  </g>
</symbol>"""

ROCKS = f"""<symbol id="rocks" viewBox="-12 -28 24 32" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -10,-24 L -11,2 L 11,2 L 10,-24 Z"/>
    <rect x="-7" y="-20" width="6" height="5" rx="0.5" stroke="{G3}" stroke-width="0.50" opacity="0.75"/>
    <rect x="1"  y="-18" width="6" height="5" rx="0.5" stroke="{G3}" stroke-width="0.50" opacity="0.75"/>
    <rect x="-4" y="-13" width="5" height="4" rx="0.5" stroke="{G3}" stroke-width="0.40" opacity="0.65"/>
    <path d="M -9,-9 Q 0,-8 9,-9" stroke="{G3}" stroke-width="0.40" opacity="0.65"/>
  </g>
</symbol>"""

FLUTE = f"""<symbol id="flute" viewBox="-8 -48 16 52" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -5,-44 Q -7,-24 -4,-18 Q -2,-14 0,-14 Q 2,-14 4,-18 Q 7,-24 5,-44 Z"/>
    <line x1="-5" y1="-44" x2="5" y2="-44"/>
    <line x1="0" y1="-14" x2="0" y2="-2"/>
    <line x1="-6" y1="-2" x2="6" y2="-2"/>
    <circle cx="-2" cy="-30" r="0.8" stroke="{G3}" stroke-width="0.40" opacity="0.85"/>
    <circle cx="2"  cy="-36" r="0.8" stroke="{G3}" stroke-width="0.40" opacity="0.85"/>
    <circle cx="0"  cy="-24" r="0.6" stroke="{G3}" stroke-width="0.30" opacity="0.75"/>
    <circle cx="-1" cy="-42" r="0.6" stroke="{G3}" stroke-width="0.30" opacity="0.75"/>
  </g>
</symbol>"""

SHAKER = f"""<symbol id="shaker" viewBox="-12 -44 24 48" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -9,-14 Q -10,-4 -8,2 L 8,2 Q 10,-4 9,-14 Z"/>
    <path d="M -9,-14 Q -8,-24 -5,-32 L 5,-32 Q 8,-24 9,-14 Z"/>
    <path d="M -5,-32 Q -3,-40 0,-42 Q 3,-40 5,-32 Z"/>
    <line x1="-9" y1="-14" x2="9" y2="-14" stroke-width="1.1"/>
    <path d="M -6,-16 Q 0,-17 6,-16" stroke="{G3}" stroke-width="0.40" opacity="0.75"/>
  </g>
</symbol>"""

JIGGER = f"""<symbol id="jigger" viewBox="-10 -28 20 30" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -8,-24 L -1.5,-12 L 1.5,-12 L 8,-24 Z"/>
    <line x1="-8" y1="-24" x2="8" y2="-24"/>
    <path d="M -1.5,-12 L -5,0 L 5,0 L 1.5,-12 Z"/>
    <line x1="-5" y1="0" x2="5" y2="0"/>
  </g>
</symbol>"""

STRAINER = f"""<symbol id="strainer" viewBox="-22 -12 44 14" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="-5" cy="0" r="9"/>
    <path d="M -14,0 Q -12,-4 -10,0 Q -8,4 -6,0 Q -4,-4 -2,0 Q 0,4 2,0 Q 4,-4 6,0"
          stroke="{G3}" stroke-width="0.65" opacity="0.85"/>
    <line x1="4"  y1="0"  x2="21" y2="-3"/>
    <line x1="4"  y1="0"  x2="21" y2="3"/>
    <line x1="21" y1="-3" x2="21" y2="3" stroke-linecap="round"/>
  </g>
</symbol>"""

CITRUS = f"""<symbol id="citrus" viewBox="-10 -10 20 20" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round">
    <circle cx="0" cy="0" r="8"/>
    <circle cx="0" cy="0" r="3"/>
    <line x1="0"    y1="-8"   x2="0"   y2="8"   stroke-width="0.45"/>
    <line x1="-8"   y1="0"    x2="8"   y2="0"   stroke-width="0.45"/>
    <line x1="-5.6" y1="-5.6" x2="5.6" y2="5.6" stroke-width="0.35"/>
    <line x1="5.6"  y1="-5.6" x2="-5.6" y2="5.6" stroke-width="0.35"/>
  </g>
</symbol>"""

HIGHBALL_ICON = HIGHBALL.replace('id="highball"', 'id="icon-hb"')
ROCKS_ICON    = ROCKS.replace('id="rocks"',    'id="icon-rk"')
FLUTE_ICON    = FLUTE.replace('id="flute"',    'id="icon-fl"')

# ─── Placement helpers ─────────────────────────────────────────────────────────
def use(sym, cx, cy, w, h=None, rot=0, extra=""):
    if h is None: h = w
    tr = f'transform="rotate({rot},{cx},{cy})"' if rot else ""
    return (f'<use href="#{sym}" x="{cx-w/2:.2f}" y="{cy-h/2:.2f}" '
            f'width="{w}" height="{h}" {tr} {extra}/>')

def useb(sym, cx, cy, w, h=None, rot=0):
    if h is None: h = w
    tr = f'transform="rotate({rot},{cx},{cy})"' if rot else ""
    return (f'<g filter="url(#sketch-b)" {tr}>'
            f'<use href="#{sym}" x="{cx-w/2:.2f}" y="{cy-h/2:.2f}" width="{w}" height="{h}"/>'
            f'</g>')

def usep(sym, cx, cy, w, h=None, rot=0):
    if h is None: h = w
    tr = f'transform="rotate({rot},{cx},{cy})"' if rot else ""
    return (f'<use href="#{sym}" x="{cx-w/2:.2f}" y="{cy-h/2:.2f}" '
            f'width="{w}" height="{h}" {tr}/>')

# ─── Full decoration SVG ───────────────────────────────────────────────────────
DECO = f"""<svg class="deco" viewBox="0 0 148 210" xmlns="http://www.w3.org/2000/svg">
<defs>
  {FILTERS}
  {WF5} {WF5B} {WF8} {BUD} {BERRIES} {BRANCH} {HERB} {TINY} {TENDRIL}
  {PINK_WF5} {PINK_TINY} {PINK_BLOOM} {PINK_HEART}
  {MARTINI} {COUPE} {WINE_GLASS} {NICK_NORA} {HIGHBALL} {ROCKS} {FLUTE}
  {SHAKER} {JIGGER} {STRAINER} {CITRUS}
  {HIGHBALL_ICON} {ROCKS_ICON} {FLUTE_ICON}
</defs>

<!-- Art Deco frame -->
<rect x="6.5" y="6.5" width="135" height="197" fill="none" stroke="{G}" stroke-width="0.75" opacity="0.65"/>
<rect x="8.0" y="8.0" width="132" height="194" fill="none" stroke="{G}" stroke-width="0.28" opacity="0.40"/>

<!-- Corner ornaments -->
<g stroke="{G}" fill="none" opacity="0.80">
  <!-- TL -->
  <polyline points="6.5,20 6.5,14 10,14 10,10 14,10 14,6.5 20,6.5" stroke-width="0.5"/>
  <path d="M 6.5,17 Q 11.5,11.5 17,6.5" stroke-width="0.28" opacity="0.6"/>
  <polygon points="10,14 11.2,12 12.4,14 11.2,16" fill="{G}" opacity="0.85"/>
  <polygon points="14,10 15.2,8  16.4,10 15.2,12" fill="{G}" opacity="0.85"/>
  <!-- TR -->
  <polyline points="141.5,20 141.5,14 138,14 138,10 134,10 134,6.5 128,6.5" stroke-width="0.5"/>
  <path d="M 141.5,17 Q 136.5,11.5 131,6.5" stroke-width="0.28" opacity="0.6"/>
  <polygon points="138,14 136.8,12 135.6,14 136.8,16" fill="{G}" opacity="0.85"/>
  <polygon points="134,10 132.8,8  131.6,10 132.8,12" fill="{G}" opacity="0.85"/>
  <!-- BL -->
  <polyline points="6.5,190 6.5,196 10,196 10,200 14,200 14,203.5 20,203.5" stroke-width="0.5"/>
  <path d="M 6.5,193 Q 11.5,198.5 17,203.5" stroke-width="0.28" opacity="0.6"/>
  <polygon points="10,196 11.2,198 12.4,196 11.2,194" fill="{G}" opacity="0.85"/>
  <polygon points="14,200 15.2,202 16.4,200 15.2,198" fill="{G}" opacity="0.85"/>
  <!-- BR -->
  <polyline points="141.5,190 141.5,196 138,196 138,200 134,200 134,203.5 128,203.5" stroke-width="0.5"/>
  <path d="M 141.5,193 Q 136.5,198.5 131,203.5" stroke-width="0.28" opacity="0.6"/>
  <polygon points="138,196 136.8,198 135.6,196 136.8,194" fill="{G}" opacity="0.85"/>
  <polygon points="134,200 132.8,202 131.6,200 132.8,198" fill="{G}" opacity="0.85"/>
</g>

<!-- ═══════════════════════════════
     TOP-LEFT cluster
     ═══════════════════════════════ -->
{useb('wf8',  14, 18, 24)}
{useb('wf5b', 28, 10, 18)}
{useb('tiny',  8,  9, 12)}
{useb('bud',  32, 28, 12)}
{useb('branch',  10, 28, 20, 28, -15)}
{useb('berries', 30, 26, 18, 20,  10)}
{useb('herb',    22,  8, 12, 20,  20)}
{useb('tendril',  8, 20, 16, 22,   5)}
<g transform="translate(12,14) rotate(-12) scale(0.52)">
  <use href="#martini" x="-17" y="-40" width="34" height="44"/>
</g>
<g transform="translate(34,18) rotate(6) scale(0.48)">
  <use href="#jigger" x="-10" y="-28" width="20" height="30"/>
</g>
{usep('pink-wf5',  20,  7, 13)}
{usep('pink-bloom', 30, 32, 13, 19, -8)}
{usep('pink-tiny',  7, 31,  9)}
{usep('pink-heart', 36, 13,  7)}

<!-- ═══════════════════════════════
     TOP-RIGHT cluster
     ═══════════════════════════════ -->
{useb('wf5',  134, 18, 22)}
{useb('wf8',  120, 10, 24)}
{useb('tiny', 140,  9, 12)}
{useb('bud',  116, 28, 12)}
{useb('branch',  138, 28, 20, 28, 15)}
{useb('berries', 118, 26, 18, 20,-10)}
{useb('herb',    126,  8, 12, 20,-20)}
{useb('tendril', 140, 20, 16, 22, -5)}
<g transform="translate(136,14) rotate(12) scale(0.52)">
  <use href="#coupe" x="-17" y="-36" width="34" height="40"/>
</g>
<g transform="translate(116,24) rotate(-5) scale(0.62)">
  <use href="#citrus" x="-10" y="-10" width="20" height="20"/>
</g>
{usep('pink-wf5',  128,  7, 13)}
{usep('pink-bloom', 118, 32, 13, 19, 8)}
{usep('pink-tiny',  141, 31,  9)}
{usep('pink-heart', 112, 13,  7)}

<!-- ═══════════════════════════════
     BOTTOM-LEFT cluster
     ═══════════════════════════════ -->
{useb('wf5b', 14, 194, 22)}
{useb('wf8',  28, 186, 24)}
{useb('tiny',  8, 202, 12)}
{useb('bud',  32, 183, 12)}
{useb('branch',  10, 184, 20, 28, 10)}
{useb('berries', 30, 199, 18, 20, -8)}
{useb('herb',    22, 204, 12, 20,-20)}
{useb('tendril',  8, 190, 16, 22, 10)}
<g transform="translate(18,185) rotate(-8) scale(0.50)">
  <use href="#wine-glass" x="-13" y="-44" width="26" height="48"/>
</g>
<g transform="translate(34,198) rotate(14) scale(0.52)">
  <use href="#strainer" x="-22" y="-12" width="44" height="14"/>
</g>
{usep('pink-wf5',  20, 205, 13)}
{usep('pink-bloom', 30, 179, 13, 19, 5)}
{usep('pink-tiny',  7, 181,  9)}
{usep('pink-heart', 36, 198,  7)}

<!-- ═══════════════════════════════
     BOTTOM-RIGHT cluster
     ═══════════════════════════════ -->
{useb('wf8',  134, 194, 24)}
{useb('wf5',  119, 186, 22)}
{useb('tiny', 140, 202, 12)}
{useb('bud',  116, 183, 12)}
{useb('branch',  138, 184, 20, 28,-10)}
{useb('berries', 118, 199, 18, 20,  8)}
{useb('herb',    126, 204, 12, 20, 20)}
{useb('tendril', 140, 190, 16, 22,-10)}
<g transform="translate(122,184) rotate(6) scale(0.48)">
  <use href="#shaker" x="-12" y="-44" width="24" height="48"/>
</g>
<g transform="translate(138,197) rotate(-10) scale(0.50)">
  <use href="#nick-nora" x="-14" y="-40" width="28" height="44"/>
</g>
{usep('pink-wf5',  128, 205, 13)}
{usep('pink-bloom', 118, 179, 13, 19, -5)}
{usep('pink-tiny',  141, 181,  9)}
{usep('pink-heart', 112, 198,  7)}

<!-- ═══════════════════════════════
     LEFT garland
     ═══════════════════════════════ -->
{useb('branch',   10,  46, 16, 24,  8)}
{usep('pink-tiny', 12,  60, 10)}
{useb('berries',  10,  72, 14, 18, -5)}
{usep('pink-wf5', 12,  85, 13)}
{useb('herb',      9,  98, 11, 18, 10)}
{usep('pink-tiny', 13, 110, 10)}
{useb('branch',   10, 122, 16, 24, -8)}
{usep('pink-bloom', 12, 133, 12, 17, 5)}
{useb('tendril',   9, 147, 14, 20,  5)}
{usep('pink-heart',13, 158,  7)}
{useb('berries',  10, 170, 14, 18, 10)}
{usep('pink-tiny', 12, 182, 10)}

<!-- ═══════════════════════════════
     RIGHT garland
     ═══════════════════════════════ -->
{useb('branch',  138,  46, 16, 24, -8)}
{usep('pink-tiny',136,  60, 10)}
{useb('berries', 138,  72, 14, 18,  5)}
{usep('pink-wf5',136,  85, 13)}
{useb('herb',    139,  98, 11, 18,-10)}
{usep('pink-tiny',135, 110, 10)}
{useb('branch',  138, 122, 16, 24,  8)}
{usep('pink-bloom',136,133, 12, 17, -5)}
{useb('tendril', 139, 147, 14, 20, -5)}
{usep('pink-heart',135,158,  7)}
{useb('berries', 138, 170, 14, 18,-10)}
{usep('pink-tiny',136, 182, 10)}
</svg>"""

# ─── Per-cocktail icon SVGs ────────────────────────────────────────────────────
def drink_icon(sym_id, vx, vy, vw, vh, dw=10, dh=13):
    return (f'<svg width="{dw}mm" height="{dh}mm" viewBox="{vx} {vy} {vw} {vh}" '
            f'xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto 2mm;">'
            f'<use href="#{sym_id}" x="{vx}" y="{vy}" width="{vw}" height="{vh}"/>'
            f'</svg>')

icon_hb = drink_icon('icon-hb', -11, -42, 32, 46,  9, 13)
icon_rk = drink_icon('icon-rk', -12, -28, 24, 32,  9, 11)
icon_fl = drink_icon('icon-fl',  -8, -48, 16, 52,  7, 14)

# ─── HTML ──────────────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<style>
@page {{ size: 148mm 210mm; margin: 0; }}
*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}

@font-face {{
  font-family: 'Lora';
  src: url('data:font/truetype;base64,{lr}') format('truetype');
  font-weight: 400; font-style: normal;
}}
@font-face {{
  font-family: 'Lora';
  src: url('data:font/truetype;base64,{lb}') format('truetype');
  font-weight: 700; font-style: normal;
}}
@font-face {{
  font-family: 'Lora';
  src: url('data:font/truetype;base64,{li}') format('truetype');
  font-weight: 400; font-style: italic;
}}
@font-face {{
  font-family: 'Poppins';
  src: url('data:font/truetype;base64,{pl}') format('truetype');
  font-weight: 300; font-style: normal;
}}

html, body {{ width: 148mm; height: 210mm; overflow: hidden; }}

.page {{
  position: relative;
  width: 148mm; height: 210mm;
  background: radial-gradient(ellipse 85% 90% at 50% 38%,
    #1E1C22 0%, #141318 42%, #0D0C10 72%, #080709 100%);
}}

.deco {{
  position: absolute; top: 0; left: 0;
  width: 148mm; height: 210mm;
  pointer-events: none;
}}

.content {{
  position: absolute; top: 0; left: 0;
  width: 148mm; height: 210mm;
  display: flex; flex-direction: column; align-items: center;
  padding: 18mm 16mm 13mm;
}}

/* ── Masthead ── */
.monogram {{
  font-family: 'Poppins', sans-serif; font-weight: 300;
  font-size: 5.5px; letter-spacing: 0.38em; color: {G};
  text-transform: uppercase; margin-bottom: 1.2mm; text-align: center;
}}
.brand-name {{
  font-family: 'Lora', serif; font-weight: 700; font-size: 38px;
  color: #EEEAE0; text-align: center; line-height: 1.0;
  margin-bottom: 1.5mm; letter-spacing: 0.14em;
}}
.est-rule {{
  display: flex; align-items: center; gap: 0; width: 75%; margin-bottom: 1.5mm;
}}
.est-line {{ flex: 1; height: 0.35px; background: {G}; opacity: 0.55; }}
.est-text {{
  font-family: 'Poppins', sans-serif; font-weight: 300;
  font-size: 4.5px; letter-spacing: 0.32em; color: {G3};
  padding: 0 6px; white-space: nowrap;
}}
.menu-script {{
  font-family: 'Lora', serif; font-weight: 400; font-style: italic;
  font-size: 13.5px; color: {G}; text-align: center;
  margin-bottom: 4.5mm; letter-spacing: 0.02em;
}}
.sig-row {{
  display: flex; align-items: center; width: 100%; margin-bottom: 4mm;
}}
.sig-line {{ flex: 1; height: 0.35px; background: {G}; opacity: 0.55; }}
.sig-dot {{
  width: 3px; height: 3px; background: {G};
  border-radius: 50%; margin: 0 7px; opacity: 0.75;
}}

/* ── Cocktail cards ── */
.cocktails {{
  flex: 1; display: flex; flex-direction: column;
  justify-content: space-evenly; align-items: center; width: 100%;
}}
.cocktail {{ text-align: center; width: 100%; }}
.drink-name {{
  font-family: 'Lora', serif; font-weight: 700; font-size: 16px;
  color: #ECEAE0; margin-bottom: 2mm; letter-spacing: 0.03em;
}}
.tasting-note {{
  font-family: 'Lora', serif; font-weight: 400; font-style: italic;
  font-size: 9px; color: #B8B0A0; line-height: 1.5;
  margin-bottom: 2mm; padding: 0 2mm;
}}
.ingredients {{
  font-family: 'Poppins', sans-serif; font-weight: 300;
  font-size: 5.5px; letter-spacing: 0.18em; color: #968C6C;
  text-transform: uppercase; line-height: 1.65;
}}
.diamond {{ color: {G}; }}

/* ── Dividers ── */
.divider {{
  display: flex; align-items: center; width: 84%;
}}
.div-line {{ flex: 1; height: 0.3px; background: {G}; opacity: 0.50; }}
.div-center {{
  display: flex; gap: 4px; padding: 0 5px;
  font-size: 5px; color: {G}; line-height: 1; opacity: 0.75;
}}

/* ── Footer ── */
.footer {{ text-align: center; margin-top: 2mm; }}
.footer-rule {{
  display: flex; align-items: center; margin-bottom: 1.5mm;
}}
.footer-line {{ flex: 1; height: 0.3px; background: {G}; opacity: 0.45; }}
.footer-diamond {{ font-size: 5px; color: {G3}; padding: 0 5px; opacity: 0.8; }}
.footer-text {{
  font-family: 'Poppins', sans-serif; font-weight: 300;
  font-size: 4.5px; letter-spacing: 0.35em; color: {G3};
  text-transform: uppercase; opacity: 0.85;
}}
</style>
</head>
<body>
<div class="page">

  {DECO}

  <div class="content">

    <div class="monogram">A &nbsp;·&nbsp; EST · 2023</div>
    <h1 class="brand-name">TADOW</h1>
    <div class="est-rule">
      <div class="est-line"></div>
      <span class="est-text">Signature Cocktails</span>
      <div class="est-line"></div>
    </div>
    <div class="menu-script">Cocktails Menu</div>
    <div class="sig-row">
      <div class="sig-line"></div>
      <div class="sig-dot"></div>
      <div class="sig-line"></div>
    </div>

    <div class="cocktails">

      <div class="cocktail">
        {icon_hb}
        <h2 class="drink-name">Hibiscus Veil</h2>
        <p class="tasting-note">A blush-pink long drink — floral and bittersweet,<br>veiled in cool botanical effervescence.</p>
        <p class="ingredients">
          Vodka <span class="diamond">◆</span> Rosato Aperitivo <span class="diamond">◆</span>
          Fresh Lime <span class="diamond">◆</span> Botanical Tonic
        </p>
      </div>

      <div class="divider">
        <div class="div-line"></div>
        <div class="div-center"><span>◆</span><span>◆</span><span>◆</span></div>
        <div class="div-line"></div>
      </div>

      <div class="cocktail">
        {icon_rk}
        <h2 class="drink-name">Golden Sour</h2>
        <p class="tasting-note">Silken and amber-warm, where ripe pear softens<br>the whiskey's edge over a whisper of spice.</p>
        <p class="ingredients">
          Whiskey <span class="diamond">◆</span> Pear Syrup <span class="diamond">◆</span>
          Fresh Lemon <span class="diamond">◆</span> Angostura Bitters
        </p>
      </div>

      <div class="divider">
        <div class="div-line"></div>
        <div class="div-center"><span>◆</span><span>◆</span><span>◆</span></div>
        <div class="div-line"></div>
      </div>

      <div class="cocktail">
        {icon_fl}
        <h2 class="drink-name">Elderbloom Spritz</h2>
        <p class="tasting-note">Effervescent and garden-fresh — elderflower and mint<br>lifted by chilled Prosecco and a ribbon of cucumber.</p>
        <p class="ingredients">
          Prosecco <span class="diamond">◆</span> Elderflower <span class="diamond">◆</span>
          Fresh Mint <span class="diamond">◆</span> Cucumber <span class="diamond">◆</span> Lime
        </p>
      </div>

    </div>

    <div class="footer">
      <div class="footer-rule">
        <div class="footer-line"></div>
        <span class="footer-diamond">◆</span>
        <div class="footer-line"></div>
      </div>
      <p class="footer-text">Crafted to Order</p>
    </div>

  </div>
</div>
</body>
</html>"""

out = '/home/user/Tadow/cocktail-menu.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"Written: {out}  ({os.path.getsize(out)//1024} KB)")
