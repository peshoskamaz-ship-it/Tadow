#!/usr/bin/env python3
"""Generate A5 cocktail menu HTML — mint green & gold, hand-drawn botanical style."""
import base64, os, math

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

lr = b64('/tmp/fonts/lora-regular.ttf')
lb = b64('/tmp/fonts/lora-bold.ttf')
li = b64('/tmp/fonts/lora-italic.ttf')
pl = b64('/tmp/fonts/poppins-light.ttf')

# ─── Colour tokens ─────────────────────────────────────────────────────────────
G  = '#D4C890'   # main gold
G2 = '#E8D8A8'   # gold highlight
G3 = '#B8A260'   # gold shadow
M  = '#7BC4A8'   # main mint green
M2 = '#A4D8C4'   # mint highlight
M3 = '#5AA888'   # mint shadow
SW = '0.70'

# ─── Petal helper ──────────────────────────────────────────────────────────────
def petal_path(r, wf=0.42, asym=0.0):
    """Slightly asymmetric petal for hand-drawn feel."""
    w  = r * wf
    wa = w * (1 + asym)
    return (f"M 0,0 C {wa*0.8:.2f},{-r*0.09:.2f} {wa:.2f},{-r*0.56:.2f} {asym*r*0.15:.2f},{-r:.2f} "
            f"C {-w:.2f},{-r*0.60:.2f} {-w*0.82:.2f},{-r*0.07:.2f} 0,0 Z")

def petal_ring(n, r, wf, offset, color=None, alpha='0.18', sw=None):
    if color is None: color = G
    if sw is None: sw = SW
    step = 360 / n
    out = []
    for i in range(n):
        a = offset + step * i
        # Vary opacity slightly per petal for a hand-inked feel
        op = float(alpha) * (0.85 + 0.30 * ((i * 1.618) % 1))
        asym = 0.05 * math.sin(i * 2.3)
        out.append(
            f'<path d="{petal_path(r, wf, asym)}" '
            f'fill="{color}" fill-opacity="{op:.2f}" '
            f'stroke="{color}" stroke-width="{sw}" '
            f'transform="rotate({a:.1f})"/>'
        )
    return "\n".join(out)

# ─── Mint botanical symbols ────────────────────────────────────────────────────

WF5 = f"""<symbol id="wf5" viewBox="-13 -13 26 26" overflow="visible">
  {petal_ring(5, 10, 0.46, 2)}
  <circle r="2.4" fill="{M}" stroke="{M3}" stroke-width="0.45"/>
  <circle r="1.1" fill="{M2}"/>
</symbol>"""

WF5B = f"""<symbol id="wf5b" viewBox="-13 -13 26 26" overflow="visible">
  {petal_ring(5, 10, 0.46, 2)}
  {petal_ring(5, 7,  0.40, 38)}
  <circle r="2.1" fill="{M}" stroke="{M3}" stroke-width="0.40"/>
  <circle r="0.9" fill="{M2}"/>
</symbol>"""

WF8 = f"""<symbol id="wf8" viewBox="-15 -15 30 30" overflow="visible">
  {petal_ring(8, 11, 0.38, 1)}
  {petal_ring(8, 7,  0.35, 23.5)}
  <circle r="3.0" fill="{M}" stroke="{M3}" stroke-width="0.40"/>
  <circle r="1.3" fill="{M2}"/>
</symbol>"""

# 6-petal loose flower — more organic than the 5-petal
WF6 = f"""<symbol id="wf6" viewBox="-13 -13 26 26" overflow="visible">
  {petal_ring(6, 9, 0.42, 8)}
  <circle r="2.2" fill="{M}" stroke="{M3}" stroke-width="0.40"/>
  <circle r="0.9" fill="{M2}"/>
</symbol>"""

BUD = f"""<symbol id="bud" viewBox="-6 -15 12 17" overflow="visible">
  <path d="M 0.3,1.5 Q 0.5,-2 0,-6" stroke="{M}" stroke-width="0.65" fill="none" stroke-linecap="round"/>
  <path d="M 0,-6 C 3.2,-8.5 4.5,-12.5 0.2,-13.5 C -3.8,-12.8 -3.2,-8.2 0,-6 Z"
        fill="{M}" fill-opacity="0.28" stroke="{M}" stroke-width="0.65"/>
  <!-- natural-looking sepals -->
  <path d="M -0.8,-7.5 Q -4.5,-9 -3.2,-6.5" stroke="{M3}" stroke-width="0.45" fill="none" stroke-linecap="round"/>
  <path d="M  0.9,-7.2 Q  4.2,-9  3.0,-6.3" stroke="{M3}" stroke-width="0.40" fill="none" stroke-linecap="round"/>
</symbol>"""

BERRIES = f"""<symbol id="berries" viewBox="-15 -22 30 24" overflow="visible">
  <path d="M 0.2,2 Q -0.3,-3 0,-10.5" stroke="{M3}" stroke-width="0.70" fill="none" stroke-linecap="round"/>
  <path d="M 0,-7.5 Q -5.5,-9,-8.5,-13.5" stroke="{M3}" stroke-width="0.55" fill="none" stroke-linecap="round"/>
  <path d="M 0.2,-7 Q  5.2,-8.5, 8.8,-12.8" stroke="{M3}" stroke-width="0.55" fill="none" stroke-linecap="round"/>
  <!-- berries - slightly imperfect circles -->
  <ellipse cx="0.3"  cy="-14.5" rx="3.0" ry="2.8" fill="{M}" fill-opacity="0.75" stroke="{M3}" stroke-width="0.50"/>
  <ellipse cx="-8.5" cy="-14.2" rx="2.4" ry="2.2" fill="{M}" fill-opacity="0.65" stroke="{M3}" stroke-width="0.45"/>
  <ellipse cx="8.8"  cy="-13.8" rx="2.2" ry="2.4" fill="{M}" fill-opacity="0.65" stroke="{M3}" stroke-width="0.45"/>
  <circle cx="-0.5" cy="-15.5" r="0.65" fill="{M2}" opacity="0.85"/>
  <circle cx="-9.2" cy="-15.2" r="0.55" fill="{M2}" opacity="0.75"/>
  <circle cx="8.2"  cy="-14.8" r="0.55" fill="{M2}" opacity="0.75"/>
</symbol>"""

BRANCH = f"""<symbol id="branch" viewBox="-17 -27 34 29" overflow="visible">
  <path d="M -0.3,2 Q 1.8,-7 0.2,-24.5" stroke="{M3}" stroke-width="0.70" fill="none" stroke-linecap="round"/>
  <!-- leaf pairs with organic shapes -->
  <path d="M 0,-5.5 Q -9.5,-7.5,-12,-14 Q -5.5,-9.5, 0,-5.5"
        fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.58"/>
  <path d="M 0,-5.5 Q  9,-7,  11.5,-13.5 Q  5.5,-9, 0,-5.5"
        fill="{M}" fill-opacity="0.16" stroke="{M}" stroke-width="0.52"/>
  <path d="M 0,-12.5 Q -10.5,-15,-12.5,-21 Q -5,-15.5, 0,-12.5"
        fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.58"/>
  <path d="M 0,-12.5 Q  10,-14.5, 12,-20.5 Q  5,-15, 0,-12.5"
        fill="{M}" fill-opacity="0.16" stroke="{M}" stroke-width="0.52"/>
  <path d="M 0.3,-20.5 Q 4.5,-22.5, 2.5,-26.5 Q -2,-22.5, 0.3,-20.5"
        fill="{M}" fill-opacity="0.24" stroke="{M}" stroke-width="0.55"/>
  <!-- leaf veins -->
  <path d="M 0,-5.5 Q -6,-8,-9,-11" stroke="{M3}" stroke-width="0.28" fill="none" opacity="0.6"/>
  <path d="M 0,-12.5 Q -6,-15,-9.5,-18" stroke="{M3}" stroke-width="0.28" fill="none" opacity="0.6"/>
</symbol>"""

HERB = f"""<symbol id="herb" viewBox="-9 -23 18 25" overflow="visible">
  <path d="M 0.2,2 Q 0.5,-4 0,-20.5" stroke="{M3}" stroke-width="0.65" fill="none" stroke-linecap="round"/>
  <!-- paired leaves with vein lines -->
  <path d="M 0,-5  Q -6.5,-6.5,-7.5,-9.5 Q -3,-7.5, 0,-5"  fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.48"/>
  <path d="M -0.5,-4.5 Q -5,-5.5,-5.5,-7.5" stroke="{M3}" stroke-width="0.25" fill="none" opacity="0.55"/>
  <path d="M 0,-5  Q  6,-6.5,  7,-9.5 Q  3,-7, 0,-5"  fill="{M}" fill-opacity="0.16" stroke="{M}" stroke-width="0.42"/>
  <path d="M 0,-10 Q -5.5,-11.5,-6.5,-14.5 Q -2,-12.5, 0,-10" fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.48"/>
  <path d="M -0.4,-9.5 Q -4,-10.5,-5,-13" stroke="{M3}" stroke-width="0.25" fill="none" opacity="0.55"/>
  <path d="M 0,-10 Q  5.5,-11, 6.5,-14 Q  2,-12, 0,-10" fill="{M}" fill-opacity="0.16" stroke="{M}" stroke-width="0.42"/>
  <path d="M 0,-15 Q -4.5,-16.5,-5.5,-19.5 Q -1,-17.5, 0,-15" fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.42"/>
  <path d="M 0,-15 Q  4,-16.5, 5,-19 Q  1,-17, 0,-15" fill="{M}" fill-opacity="0.16" stroke="{M}" stroke-width="0.36"/>
  <ellipse cx="0" cy="-20.5" rx="1.8" ry="1.5" fill="{M}" fill-opacity="0.9"/>
</symbol>"""

TINY = f"""<symbol id="tiny" viewBox="-8 -8 16 16" overflow="visible">
  {petal_ring(5, 6, 0.42, 3)}
  <circle r="1.6" fill="{M}"/>
</symbol>"""

TENDRIL = f"""<symbol id="tendril" viewBox="-11 -22 22 24" overflow="visible">
  <!-- organic curling vine -->
  <path d="M 0.3,2 Q -8.5,0.5,-6.5,-6 Q -4,-12.5, 0.5,-14.5 Q 5,-17, 2.5,-21"
        stroke="{M3}" stroke-width="0.58" fill="none" stroke-linecap="round"/>
  <!-- small organic leaves -->
  <path d="M -5.5,-3.5 Q -10.5,-2.5,-10.8,-7 Q -7,-4.5,-5.5,-3.5" fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.42"/>
  <path d="M -4.5,-10.5 Q -9.8,-11.5,-9,-16 Q -5.5,-12.5,-4.5,-10.5" fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.42"/>
  <!-- tiny spiral curls at tip -->
  <path d="M 2.5,-21 Q 5,-22.5, 4.5,-20 Q 4,-18 2.5,-19" stroke="{M3}" stroke-width="0.38" fill="none" stroke-linecap="round"/>
</symbol>"""

# New: loose stem with multiple small blossoms — evokes the scattered flowers in the reference
SPRIG = f"""<symbol id="sprig" viewBox="-14 -26 28 28" overflow="visible">
  <!-- main curving stem -->
  <path d="M 0,2 Q -3,-5 -1,-12 Q 1,-18 0,-24"
        stroke="{M3}" stroke-width="0.60" fill="none" stroke-linecap="round"/>
  <!-- branch stems -->
  <path d="M -1,-8 Q -8,-10,-11,-14" stroke="{M3}" stroke-width="0.48" fill="none" stroke-linecap="round"/>
  <path d="M -0.5,-14 Q  6,-16, 9,-19" stroke="{M3}" stroke-width="0.45" fill="none" stroke-linecap="round"/>
  <path d="M -0.2,-20 Q -5,-22,-7,-25" stroke="{M3}" stroke-width="0.42" fill="none" stroke-linecap="round"/>
  <!-- small blossoms at tips -->
  <g transform="translate(-11,-14)">
    {petal_ring(5, 4.5, 0.44, 5, M, '0.52', '0.55')}
    <circle r="1.1" fill="{M}"/>
  </g>
  <g transform="translate(9,-19)">
    {petal_ring(5, 4, 0.44, 12, M, '0.48', '0.52')}
    <circle r="1.0" fill="{M}"/>
  </g>
  <g transform="translate(-7,-25)">
    {petal_ring(5, 3.5, 0.44, 0, M, '0.55', '0.50')}
    <circle r="0.9" fill="{M}"/>
  </g>
</symbol>"""

# Mint large bloom on stem
BLOOM = f"""<symbol id="bloom" viewBox="-10 -25 20 27" overflow="visible">
  <path d="M 0.2,2 Q 0.8,-3 0,-9.5" stroke="{M3}" stroke-width="0.55" fill="none" stroke-linecap="round"/>
  <!-- pair of leaves on stem -->
  <path d="M 0,-6 Q -4.5,-5.5 -5,-9 Q -1.5,-6.5 0,-6" fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.38"/>
  <path d="M 0,-6 Q  4.5,-5  5,-8.5 Q  1.5,-6 0,-6" fill="{M}" fill-opacity="0.16" stroke="{M}" stroke-width="0.35"/>
  <!-- bloom head -->
  <g transform="translate(0,-12)">
    {petal_ring(5, 8, 0.46, 5, M, '0.52', '0.62')}
    <circle r="2.2" fill="{M}" stroke="{M3}" stroke-width="0.40"/>
    <circle r="1.0" fill="{M2}"/>
  </g>
</symbol>"""

# ─── Improved hand-drawn sketch filters ────────────────────────────────────────
FILTERS = f"""
  <!-- Pen-sketch: glassware — higher displacement, irregular wobble -->
  <filter id="sketch" x="-35%" y="-35%" width="170%" height="170%">
    <feTurbulence type="fractalNoise" baseFrequency="0.042 0.058" numOctaves="3" seed="7" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <!-- Pencil-sketch: botanicals — medium wobble, softer -->
  <filter id="sketch-b" x="-25%" y="-25%" width="150%" height="150%">
    <feTurbulence type="fractalNoise" baseFrequency="0.038 0.048" numOctaves="3" seed="3" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="1.9" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <!-- Light hand-drawn: tiny scatter elements -->
  <filter id="sketch-s" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.05 0.04" numOctaves="3" seed="11" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="1.2" xChannelSelector="R" yChannelSelector="G"/>
  </filter>"""

# ─── Glassware symbols (gold pen-sketch) ──────────────────────────────────────
SK  = G
SKW = '0.85'

MARTINI = f"""<symbol id="martini" viewBox="-18 -42 36 46" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <line x1="-15" y1="-38" x2="15" y2="-38"/>
    <line x1="-15" y1="-38" x2="0"  y2="-21"/>
    <line x1="15"  y1="-38" x2="0"  y2="-21"/>
    <line x1="0"   y1="-21" x2="0"  y2="-3.5"/>
    <line x1="-10" y1="-3.5" x2="10" y2="-3.5"/>
    <!-- olive on pick -->
    <circle cx="0" cy="-31" r="2.4" stroke="{G3}" stroke-width="0.55"/>
    <line x1="0" y1="-28.6" x2="0" y2="-35.5" stroke="{G3}" stroke-width="0.45"/>
  </g>
</symbol>"""

COUPE = f"""<symbol id="coupe" viewBox="-18 -37 36 41" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -16,-33 Q -11,-25 0,-23 Q 11,-25 16,-33"/>
    <line x1="-16" y1="-33" x2="16" y2="-33"/>
    <line x1="0" y1="-23" x2="0" y2="-4.5"/>
    <line x1="-10" y1="-4.5" x2="10" y2="-4.5"/>
  </g>
</symbol>"""

WINE_GLASS = f"""<symbol id="wine-glass" viewBox="-14 -46 28 50" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -11,-42 Q -13,-30 -7,-24 Q -3.5,-21 0,-21 Q 3.5,-21 7,-24 Q 13,-30 11,-42"/>
    <line x1="-11" y1="-42" x2="11" y2="-42"/>
    <path d="M -8,-32 Q 0,-30 8,-32" stroke="{G3}" stroke-width="0.45" opacity="0.75"/>
    <line x1="0" y1="-21" x2="0" y2="-4.5"/>
    <line x1="-9" y1="-4.5" x2="9" y2="-4.5"/>
  </g>
</symbol>"""

NICK_NORA = f"""<symbol id="nick-nora" viewBox="-15 -42 30 46" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -11,-38 Q -13,-29 -7.5,-24 Q -3.5,-21 0,-21 Q 3.5,-21 7.5,-24 Q 13,-29 11,-38"/>
    <line x1="-11" y1="-38" x2="11" y2="-38"/>
    <line x1="0" y1="-21" x2="0" y2="-4.5"/>
    <line x1="-9" y1="-4.5" x2="9" y2="-4.5"/>
  </g>
</symbol>"""

HIGHBALL = f"""<symbol id="highball" viewBox="-12 -44 34 48" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -9,-40 L -10,2 L 10,2 L 9,-40 Z"/>
    <!-- straw -->
    <line x1="4.5" y1="-42" x2="2.5" y2="2" stroke="{SK}" stroke-width="0.80" opacity="0.9"/>
    <!-- citrus wheel -->
    <circle cx="-2" cy="-38" r="4.5" stroke="{G3}" stroke-width="0.55" opacity="0.80"/>
    <line x1="-2" y1="-42.5" x2="-2" y2="-33.5" stroke="{G3}" stroke-width="0.38" opacity="0.60"/>
    <line x1="-6.5" y1="-38" x2="2.5" y2="-38" stroke="{G3}" stroke-width="0.38" opacity="0.60"/>
    <line x1="-5.2" y1="-41" x2="1.2" y2="-35" stroke="{G3}" stroke-width="0.28" opacity="0.50"/>
    <line x1="-5.2" y1="-35" x2="1.2" y2="-41" stroke="{G3}" stroke-width="0.28" opacity="0.50"/>
  </g>
</symbol>"""

ROCKS = f"""<symbol id="rocks" viewBox="-13 -30 26 34" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -11,-26 L -12,2 L 12,2 L 11,-26 Z"/>
    <rect x="-8" y="-22" width="6.5" height="5.5" rx="0.6" stroke="{G3}" stroke-width="0.50" opacity="0.72"/>
    <rect x="1.5" y="-20" width="6.5" height="5.5" rx="0.6" stroke="{G3}" stroke-width="0.50" opacity="0.72"/>
    <rect x="-4.5" y="-14" width="5.5" height="4.5" rx="0.5" stroke="{G3}" stroke-width="0.40" opacity="0.62"/>
    <path d="M -10,-10 Q 0,-9 10,-10" stroke="{G3}" stroke-width="0.40" opacity="0.62"/>
  </g>
</symbol>"""

FLUTE = f"""<symbol id="flute" viewBox="-9 -50 18 54" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -5.5,-46 Q -7.5,-26 -4.5,-19.5 Q -2,-15 0,-15 Q 2,-15 4.5,-19.5 Q 7.5,-26 5.5,-46 Z"/>
    <line x1="-5.5" y1="-46" x2="5.5" y2="-46"/>
    <line x1="0" y1="-15" x2="0" y2="-2.5"/>
    <line x1="-7" y1="-2.5" x2="7" y2="-2.5"/>
    <!-- bubbles -->
    <circle cx="-2.5" cy="-31" r="0.9" stroke="{G3}" stroke-width="0.40" opacity="0.80"/>
    <circle cx="2.5"  cy="-37" r="0.9" stroke="{G3}" stroke-width="0.40" opacity="0.80"/>
    <circle cx="0.5"  cy="-25" r="0.7" stroke="{G3}" stroke-width="0.30" opacity="0.70"/>
    <circle cx="-1.5" cy="-43" r="0.7" stroke="{G3}" stroke-width="0.30" opacity="0.70"/>
    <circle cx="1.5"  cy="-44" r="0.5" stroke="{G3}" stroke-width="0.25" opacity="0.60"/>
  </g>
</symbol>"""

SHAKER = f"""<symbol id="shaker" viewBox="-13 -46 26 50" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -9.5,-15 Q -10.5,-4.5 -8.5,2 L 8.5,2 Q 10.5,-4.5 9.5,-15 Z"/>
    <path d="M -9.5,-15 Q -8.5,-25 -5.5,-33.5 L 5.5,-33.5 Q 8.5,-25 9.5,-15 Z"/>
    <path d="M -5.5,-33.5 Q -3.5,-41.5 0,-44 Q 3.5,-41.5 5.5,-33.5 Z"/>
    <line x1="-9.5" y1="-15" x2="9.5" y2="-15" stroke-width="1.15"/>
    <path d="M -6.5,-17 Q 0,-18 6.5,-17" stroke="{G3}" stroke-width="0.40" opacity="0.72"/>
  </g>
</symbol>"""

JIGGER = f"""<symbol id="jigger" viewBox="-11 -30 22 32" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -8.5,-26 L -1.8,-13 L 1.8,-13 L 8.5,-26 Z"/>
    <line x1="-8.5" y1="-26" x2="8.5" y2="-26"/>
    <path d="M -1.8,-13 L -5.5,1 L 5.5,1 L 1.8,-13 Z"/>
    <line x1="-5.5" y1="1" x2="5.5" y2="1"/>
  </g>
</symbol>"""

STRAINER = f"""<symbol id="strainer" viewBox="-23 -13 46 15" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="-5.5" cy="0" r="9.5"/>
    <path d="M -15,0 Q -13,-4.5,-11,0 Q -9,4.5,-7,0 Q -5,-4.5,-3,0 Q -1,4.5,1,0 Q 3,-4.5,5.5,0"
          stroke="{G3}" stroke-width="0.65" opacity="0.82"/>
    <line x1="4"  y1="0"  x2="22" y2="-3.5"/>
    <line x1="4"  y1="0"  x2="22" y2="3.5"/>
    <line x1="22" y1="-3.5" x2="22" y2="3.5"/>
  </g>
</symbol>"""

CITRUS = f"""<symbol id="citrus" viewBox="-11 -11 22 22" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round">
    <circle cx="0" cy="0" r="8.5"/>
    <circle cx="0" cy="0" r="3.2"/>
    <line x1="0"    y1="-8.5" x2="0"   y2="8.5"  stroke-width="0.45"/>
    <line x1="-8.5" y1="0"    x2="8.5" y2="0"    stroke-width="0.45"/>
    <line x1="-6"   y1="-6"   x2="6"   y2="6"    stroke-width="0.35"/>
    <line x1="6"    y1="-6"   x2="-6"  y2="6"    stroke-width="0.35"/>
  </g>
</symbol>"""

# Per-cocktail icons
HIGHBALL_ICON = HIGHBALL.replace('id="highball"', 'id="icon-hb"')
ROCKS_ICON    = ROCKS.replace('id="rocks"',    'id="icon-rk"')
FLUTE_ICON    = FLUTE.replace('id="flute"',    'id="icon-fl"')

# ─── Placement helpers ─────────────────────────────────────────────────────────
def use(sym, cx, cy, w, h=None, rot=0):
    if h is None: h = w
    tr = f'transform="rotate({rot},{cx},{cy})"' if rot else ""
    return (f'<use href="#{sym}" x="{cx-w/2:.2f}" y="{cy-h/2:.2f}" '
            f'width="{w}" height="{h}" {tr}/>')

def useb(sym, cx, cy, w, h=None, rot=0):
    if h is None: h = w
    tr = f'transform="rotate({rot},{cx},{cy})"' if rot else ""
    return (f'<g filter="url(#sketch-b)" {tr}>'
            f'<use href="#{sym}" x="{cx-w/2:.2f}" y="{cy-h/2:.2f}" width="{w}" height="{h}"/>'
            f'</g>')

def uses(sym, cx, cy, w, h=None, rot=0):
    """Small scatter elements — lightest sketch filter."""
    if h is None: h = w
    tr = f'transform="rotate({rot},{cx},{cy})"' if rot else ""
    return (f'<g filter="url(#sketch-s)" {tr}>'
            f'<use href="#{sym}" x="{cx-w/2:.2f}" y="{cy-h/2:.2f}" width="{w}" height="{h}"/>'
            f'</g>')

# ─── Full decoration SVG ───────────────────────────────────────────────────────
DECO = f"""<svg class="deco" viewBox="0 0 148 210" xmlns="http://www.w3.org/2000/svg">
<defs>
  {FILTERS}
  {WF5} {WF5B} {WF8} {WF6} {BUD} {BERRIES} {BRANCH} {HERB} {TINY} {TENDRIL} {SPRIG} {BLOOM}
  {MARTINI} {COUPE} {WINE_GLASS} {NICK_NORA} {HIGHBALL} {ROCKS} {FLUTE}
  {SHAKER} {JIGGER} {STRAINER} {CITRUS}
  {HIGHBALL_ICON} {ROCKS_ICON} {FLUTE_ICON}
</defs>

<!-- Art Deco double frame — gold -->
<rect x="6.5" y="6.5" width="135" height="197" fill="none" stroke="{G}" stroke-width="0.80" opacity="0.70"/>
<rect x="8.2" y="8.2" width="131.6" height="193.6" fill="none" stroke="{G}" stroke-width="0.30" opacity="0.42"/>

<!-- Corner ornaments (gold) -->
<g stroke="{G}" fill="none" opacity="0.82">
  <!-- TL -->
  <polyline points="6.5,21 6.5,14 10,14 10,10 14,10 14,6.5 21,6.5" stroke-width="0.55"/>
  <path d="M 6.5,17.5 Q 12,12 17.5,6.5" stroke-width="0.30" opacity="0.65"/>
  <polygon points="10,14 11.3,12 12.6,14 11.3,16" fill="{G}" opacity="0.90"/>
  <polygon points="14,10 15.3,8  16.6,10 15.3,12" fill="{G}" opacity="0.90"/>
  <!-- TR -->
  <polyline points="141.5,21 141.5,14 138,14 138,10 134,10 134,6.5 127,6.5" stroke-width="0.55"/>
  <path d="M 141.5,17.5 Q 136,12 130.5,6.5" stroke-width="0.30" opacity="0.65"/>
  <polygon points="138,14 136.7,12 135.4,14 136.7,16" fill="{G}" opacity="0.90"/>
  <polygon points="134,10 132.7,8  131.4,10 132.7,12" fill="{G}" opacity="0.90"/>
  <!-- BL -->
  <polyline points="6.5,189 6.5,196 10,196 10,200 14,200 14,203.5 21,203.5" stroke-width="0.55"/>
  <path d="M 6.5,192.5 Q 12,198 17.5,203.5" stroke-width="0.30" opacity="0.65"/>
  <polygon points="10,196 11.3,198 12.6,196 11.3,194" fill="{G}" opacity="0.90"/>
  <polygon points="14,200 15.3,202 16.6,200 15.3,198" fill="{G}" opacity="0.90"/>
  <!-- BR -->
  <polyline points="141.5,189 141.5,196 138,196 138,200 134,200 134,203.5 127,203.5" stroke-width="0.55"/>
  <path d="M 141.5,192.5 Q 136,198 130.5,203.5" stroke-width="0.30" opacity="0.65"/>
  <polygon points="138,196 136.7,198 135.4,196 136.7,194" fill="{G}" opacity="0.90"/>
  <polygon points="134,200 132.7,202 131.4,200 132.7,198" fill="{G}" opacity="0.90"/>
</g>

<!-- ═══════════════════════════════════════
     TOP-LEFT cluster
     ═══════════════════════════════════════ -->
{useb('wf8',   14,  18, 24)}
{useb('wf5b',  27,   9, 19)}
{useb('sprig',  9,  10, 18, 25,  8)}
{useb('bud',   32,  27, 13)}
{useb('branch', 10, 28, 21, 29,-14)}
{useb('berries',30, 25, 19, 21, 10)}
{useb('tendril', 8, 20, 17, 23,  5)}
<g transform="translate(13,14) rotate(-10) scale(0.54)">
  <use href="#martini" x="-18" y="-42" width="36" height="46"/>
</g>
<g transform="translate(33,17) rotate(8) scale(0.50)">
  <use href="#jigger" x="-11" y="-30" width="22" height="32"/>
</g>
{uses('wf6',  20,  6, 13)}
{uses('bloom', 29, 32, 14, 20, -6)}
{uses('tiny',   7, 32,  9)}

<!-- ═══════════════════════════════════════
     TOP-RIGHT cluster
     ═══════════════════════════════════════ -->
{useb('wf5',  134,  18, 22)}
{useb('wf8',  121,   9, 25)}
{useb('sprig',139,  10, 18, 25, -8)}
{useb('bud',  116,  27, 13)}
{useb('branch',138, 28, 21, 29, 14)}
{useb('berries',118,25, 19, 21,-10)}
{useb('tendril',140,20, 17, 23, -5)}
<g transform="translate(135,14) rotate(10) scale(0.54)">
  <use href="#coupe" x="-18" y="-37" width="36" height="41"/>
</g>
<g transform="translate(117,23) rotate(-5) scale(0.64)">
  <use href="#citrus" x="-11" y="-11" width="22" height="22"/>
</g>
{uses('wf6',  128,  6, 13)}
{uses('bloom', 119, 32, 14, 20, 6)}
{uses('tiny',  141, 32,  9)}

<!-- ═══════════════════════════════════════
     BOTTOM-LEFT cluster
     ═══════════════════════════════════════ -->
{useb('wf5b',  14, 194, 23)}
{useb('wf8',   28, 186, 25)}
{useb('sprig',  8, 202, 18, 25, 12)}
{useb('bud',   32, 183, 13)}
{useb('branch', 10,184, 21, 29, 10)}
{useb('berries',30,200, 19, 21, -7)}
{useb('tendril', 8,190, 17, 23, 10)}
<g transform="translate(18,185) rotate(-7) scale(0.52)">
  <use href="#wine-glass" x="-14" y="-46" width="28" height="50"/>
</g>
<g transform="translate(33,198) rotate(12) scale(0.54)">
  <use href="#strainer" x="-23" y="-13" width="46" height="15"/>
</g>
{uses('wf6',   20, 206, 13)}
{uses('bloom',  29,179, 14, 20,  5)}
{uses('tiny',    7,180,  9)}

<!-- ═══════════════════════════════════════
     BOTTOM-RIGHT cluster
     ═══════════════════════════════════════ -->
{useb('wf8',  134, 194, 25)}
{useb('wf5',  119, 186, 22)}
{useb('sprig',140, 202, 18, 25,-12)}
{useb('bud',  116, 183, 13)}
{useb('branch',138,184, 21, 29,-10)}
{useb('berries',118,200,19, 21,  8)}
{useb('tendril',140,190,17, 23,-10)}
<g transform="translate(122,184) rotate(5) scale(0.50)">
  <use href="#shaker" x="-13" y="-46" width="26" height="50"/>
</g>
<g transform="translate(137,198) rotate(-9) scale(0.52)">
  <use href="#nick-nora" x="-15" y="-42" width="30" height="46"/>
</g>
{uses('wf6',  128, 206, 13)}
{uses('bloom', 119,179, 14, 20, -5)}
{uses('tiny',  141, 180,  9)}

<!-- ═══════════════════════════════════════
     LEFT garland (organic, varied spacing)
     ═══════════════════════════════════════ -->
{useb('branch',  10,  48, 17, 25,  8)}
{uses('tiny',    13,  61, 10)}
{useb('berries', 10,  73, 15, 19, -5)}
{useb('sprig',   11,  88, 16, 23,  6)}
{uses('wf6',     13,  88,  0)}
{useb('herb',     9,  99, 12, 19, 10)}
{uses('tiny',    13, 111, 10)}
{useb('branch',  10, 123, 17, 25, -8)}
{useb('bloom',   12, 135, 14, 20,  5)}
{useb('tendril',  9, 149, 15, 21,  5)}
{uses('tiny',    13, 161, 10)}
{useb('berries', 10, 172, 15, 19, 10)}
{uses('wf5',     13, 183, 14)}

<!-- ═══════════════════════════════════════
     RIGHT garland (mirrored, slightly offset)
     ═══════════════════════════════════════ -->
{useb('branch', 138,  48, 17, 25, -8)}
{uses('tiny',   135,  61, 10)}
{useb('berries',138,  73, 15, 19,  5)}
{useb('sprig',  137,  88, 16, 23, -6)}
{useb('herb',   139,  99, 12, 19,-10)}
{uses('tiny',   135, 111, 10)}
{useb('branch', 138, 123, 17, 25,  8)}
{useb('bloom',  136, 135, 14, 20, -5)}
{useb('tendril',139, 149, 15, 21, -5)}
{uses('tiny',   135, 161, 10)}
{useb('berries',138, 172, 15, 19,-10)}
{uses('wf5',    135, 183, 14)}
</svg>"""

# ─── Per-cocktail icon SVGs ────────────────────────────────────────────────────
def drink_icon(sym_id, vx, vy, vw, vh, dw=10, dh=13):
    return (f'<svg width="{dw}mm" height="{dh}mm" viewBox="{vx} {vy} {vw} {vh}" '
            f'xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto 2mm;">'
            f'<use href="#{sym_id}" x="{vx}" y="{vy}" width="{vw}" height="{vh}"/>'
            f'</svg>')

icon_hb = drink_icon('icon-hb', -12, -44, 34, 48,  9, 13)
icon_rk = drink_icon('icon-rk', -13, -30, 26, 34,  9, 11)
icon_fl = drink_icon('icon-fl',  -9, -50, 18, 54,  7, 14)

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
    #141C18 0%, #0E1512 42%, #090E0C 72%, #060908 100%);
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
  display: flex; align-items: center; gap: 0; width: 78%; margin-bottom: 1.5mm;
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
.sig-line {{ flex: 1; height: 0.35px; background: {G}; opacity: 0.50; }}
.sig-dot {{
  width: 3px; height: 3px; background: {G};
  border-radius: 50%; margin: 0 7px; opacity: 0.72;
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
  font-size: 9px; color: #AEB8A8; line-height: 1.5;
  margin-bottom: 2mm; padding: 0 2mm;
}}
.ingredients {{
  font-family: 'Poppins', sans-serif; font-weight: 300;
  font-size: 5.5px; letter-spacing: 0.18em; color: {M3};
  text-transform: uppercase; line-height: 1.65;
}}
.diamond {{ color: {G}; }}

/* ── Dividers ── */
.divider {{
  display: flex; align-items: center; width: 84%;
}}
.div-line {{ flex: 1; height: 0.3px; background: {G}; opacity: 0.48; }}
.div-center {{
  display: flex; gap: 4px; padding: 0 5px;
  font-size: 5px; color: {G}; line-height: 1; opacity: 0.72;
}}

/* ── Footer ── */
.footer {{ text-align: center; margin-top: 2mm; }}
.footer-rule {{
  display: flex; align-items: center; margin-bottom: 1.5mm;
}}
.footer-line {{ flex: 1; height: 0.3px; background: {G}; opacity: 0.42; }}
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
