#!/usr/bin/env python3
"""Generate A5 cocktail menu HTML — botanical border full-height, garnished glasses."""
import base64, os, math

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

lr = b64('/tmp/fonts/lora-regular.ttf')
lb = b64('/tmp/fonts/lora-bold.ttf')
li = b64('/tmp/fonts/lora-italic.ttf')
pl = b64('/tmp/fonts/poppins-light.ttf')

# ─── Colour tokens ─────────────────────────────────────────────────────────────
G  = '#D4C890'
G2 = '#E8D8A8'
G3 = '#B8A260'
M  = '#7BC4A8'
M2 = '#A4D8C4'
M3 = '#5AA888'
SW = '0.70'

# ─── Petal helper — slight asymmetry per petal for hand-inked feel ─────────────
def petal_path(r, wf=0.42, asym=0.0):
    w  = r * wf
    wa = w * (1 + asym)
    return (f"M 0,0 C {wa*0.8:.2f},{-r*0.09:.2f} {wa:.2f},{-r*0.56:.2f} {asym*r*0.14:.2f},{-r:.2f} "
            f"C {-w:.2f},{-r*0.60:.2f} {-w*0.82:.2f},{-r*0.07:.2f} 0,0 Z")

def petal_ring(n, r, wf, offset, color=None, alpha='0.18', sw=None):
    if color is None: color = G
    if sw is None: sw = SW
    step = 360 / n
    out = []
    for i in range(n):
        a = offset + step * i
        op  = float(alpha) * (0.82 + 0.32 * ((i * 1.618) % 1))
        asym = 0.06 * math.sin(i * 2.1)
        out.append(
            f'<path d="{petal_path(r, wf, asym)}" '
            f'fill="{color}" fill-opacity="{op:.2f}" '
            f'stroke="{color}" stroke-width="{sw}" '
            f'transform="rotate({a:.1f})"/>'
        )
    return "\n".join(out)

# ─── Botanical symbols (mint green) ────────────────────────────────────────────
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

WF6 = f"""<symbol id="wf6" viewBox="-13 -13 26 26" overflow="visible">
  {petal_ring(6, 9, 0.42, 8)}
  <circle r="2.2" fill="{M}" stroke="{M3}" stroke-width="0.40"/>
  <circle r="0.9" fill="{M2}"/>
</symbol>"""

BUD = f"""<symbol id="bud" viewBox="-6 -15 12 17" overflow="visible">
  <path d="M 0.3,1.5 Q 0.5,-2 0,-6" stroke="{M3}" stroke-width="0.65" fill="none" stroke-linecap="round"/>
  <path d="M 0,-6 C 3.2,-8.5 4.5,-12.5 0.2,-13.5 C -3.8,-12.8 -3.2,-8.2 0,-6 Z"
        fill="{M}" fill-opacity="0.28" stroke="{M}" stroke-width="0.65"/>
  <path d="M -0.8,-7.5 Q -4.5,-9 -3.2,-6.5" stroke="{M3}" stroke-width="0.45" fill="none" stroke-linecap="round"/>
  <path d="M  0.9,-7.2 Q  4.2,-9  3.0,-6.3" stroke="{M3}" stroke-width="0.40" fill="none" stroke-linecap="round"/>
</symbol>"""

BERRIES = f"""<symbol id="berries" viewBox="-15 -22 30 24" overflow="visible">
  <path d="M 0.2,2 Q -0.3,-3 0,-10.5" stroke="{M3}" stroke-width="0.70" fill="none" stroke-linecap="round"/>
  <path d="M 0,-7.5 Q -5.5,-9,-8.5,-13.5" stroke="{M3}" stroke-width="0.55" fill="none" stroke-linecap="round"/>
  <path d="M 0.2,-7 Q  5.2,-8.5, 8.8,-12.8" stroke="{M3}" stroke-width="0.55" fill="none" stroke-linecap="round"/>
  <ellipse cx="0.3"  cy="-14.5" rx="3.0" ry="2.8" fill="{M}" fill-opacity="0.75" stroke="{M3}" stroke-width="0.50"/>
  <ellipse cx="-8.5" cy="-14.2" rx="2.4" ry="2.2" fill="{M}" fill-opacity="0.65" stroke="{M3}" stroke-width="0.45"/>
  <ellipse cx="8.8"  cy="-13.8" rx="2.2" ry="2.4" fill="{M}" fill-opacity="0.65" stroke="{M3}" stroke-width="0.45"/>
  <circle cx="-0.5" cy="-15.5" r="0.65" fill="{M2}" opacity="0.85"/>
  <circle cx="-9.2" cy="-15.2" r="0.55" fill="{M2}" opacity="0.75"/>
  <circle cx="8.2"  cy="-14.8" r="0.55" fill="{M2}" opacity="0.75"/>
</symbol>"""

BRANCH = f"""<symbol id="branch" viewBox="-18 -28 36 30" overflow="visible">
  <path d="M -0.3,2 Q 1.8,-7 0.2,-24.5" stroke="{M3}" stroke-width="0.70" fill="none" stroke-linecap="round"/>
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
  <path d="M 0,-5.5 Q -6,-8,-9,-11" stroke="{M3}" stroke-width="0.28" fill="none" opacity="0.55"/>
  <path d="M 0,-12.5 Q -6,-15,-9.5,-18" stroke="{M3}" stroke-width="0.28" fill="none" opacity="0.55"/>
</symbol>"""

HERB = f"""<symbol id="herb" viewBox="-9 -23 18 25" overflow="visible">
  <path d="M 0.2,2 Q 0.5,-4 0,-20.5" stroke="{M3}" stroke-width="0.65" fill="none" stroke-linecap="round"/>
  <path d="M 0,-5  Q -6.5,-6.5,-7.5,-9.5 Q -3,-7.5, 0,-5"  fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.48"/>
  <path d="M -0.5,-4.5 Q -5,-5.5,-5.5,-7.5" stroke="{M3}" stroke-width="0.25" fill="none" opacity="0.52"/>
  <path d="M 0,-5  Q  6,-6.5,  7,-9.5 Q  3,-7, 0,-5"  fill="{M}" fill-opacity="0.16" stroke="{M}" stroke-width="0.42"/>
  <path d="M 0,-10 Q -5.5,-11.5,-6.5,-14.5 Q -2,-12.5, 0,-10" fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.48"/>
  <path d="M -0.4,-9.5 Q -4,-10.5,-5,-13" stroke="{M3}" stroke-width="0.25" fill="none" opacity="0.52"/>
  <path d="M 0,-10 Q  5.5,-11, 6.5,-14 Q  2,-12, 0,-10" fill="{M}" fill-opacity="0.16" stroke="{M}" stroke-width="0.42"/>
  <path d="M 0,-15 Q -4.5,-16.5,-5.5,-19.5 Q -1,-17.5, 0,-15" fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.42"/>
  <path d="M 0,-15 Q  4,-16.5, 5,-19 Q  1,-17, 0,-15" fill="{M}" fill-opacity="0.16" stroke="{M}" stroke-width="0.36"/>
  <ellipse cx="0" cy="-20.5" rx="1.8" ry="1.5" fill="{M}" fill-opacity="0.9"/>
</symbol>"""

TINY = f"""<symbol id="tiny" viewBox="-8 -8 16 16" overflow="visible">
  {petal_ring(5, 6, 0.42, 3)}
  <circle r="1.6" fill="{M}"/>
</symbol>"""

TENDRIL = f"""<symbol id="tendril" viewBox="-12 -23 24 25" overflow="visible">
  <path d="M 0.3,2 Q -9,0.5,-7,-6.5 Q -4.5,-13, 0.5,-15 Q 5.5,-17.5, 3,-22"
        stroke="{M3}" stroke-width="0.58" fill="none" stroke-linecap="round"/>
  <path d="M -6,-4 Q -11.5,-2.5,-11.5,-7.5 Q -7.5,-5,-6,-4" fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.42"/>
  <path d="M -5,-11 Q -10.5,-12,-10,-17 Q -6,-13,-5,-11" fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.42"/>
  <path d="M 3,-22 Q 5.5,-24, 5,-21.5 Q 4.5,-19.5 3,-20.5" stroke="{M3}" stroke-width="0.38" fill="none" stroke-linecap="round"/>
</symbol>"""

SPRIG = f"""<symbol id="sprig" viewBox="-15 -27 30 29" overflow="visible">
  <path d="M 0,2 Q -3,-5 -1,-13 Q 1,-19 0,-25"
        stroke="{M3}" stroke-width="0.60" fill="none" stroke-linecap="round"/>
  <path d="M -1,-9 Q -8.5,-11,-12,-15" stroke="{M3}" stroke-width="0.48" fill="none" stroke-linecap="round"/>
  <path d="M -0.5,-15 Q  6.5,-17,  9.5,-20" stroke="{M3}" stroke-width="0.45" fill="none" stroke-linecap="round"/>
  <path d="M -0.2,-21 Q -5.5,-23,-8,-26" stroke="{M3}" stroke-width="0.42" fill="none" stroke-linecap="round"/>
  <g transform="translate(-12,-15)">
    {petal_ring(5, 4.5, 0.44, 5, M, '0.52', '0.55')}
    <circle r="1.1" fill="{M}"/>
  </g>
  <g transform="translate(9.5,-20)">
    {petal_ring(5, 4, 0.44, 12, M, '0.48', '0.52')}
    <circle r="1.0" fill="{M}"/>
  </g>
  <g transform="translate(-8,-26)">
    {petal_ring(5, 3.5, 0.44, 0, M, '0.55', '0.50')}
    <circle r="0.9" fill="{M}"/>
  </g>
</symbol>"""

BLOOM = f"""<symbol id="bloom" viewBox="-10 -25 20 27" overflow="visible">
  <path d="M 0.2,2 Q 0.8,-3 0,-9.5" stroke="{M3}" stroke-width="0.55" fill="none" stroke-linecap="round"/>
  <path d="M 0,-6 Q -4.5,-5.5 -5,-9 Q -1.5,-6.5 0,-6" fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.38"/>
  <path d="M 0,-6 Q  4.5,-5  5,-8.5 Q  1.5,-6 0,-6" fill="{M}" fill-opacity="0.16" stroke="{M}" stroke-width="0.35"/>
  <g transform="translate(0,-12)">
    {petal_ring(5, 8, 0.46, 5, M, '0.52', '0.62')}
    <circle r="2.2" fill="{M}" stroke="{M3}" stroke-width="0.40"/>
    <circle r="1.0" fill="{M2}"/>
  </g>
</symbol>"""

# ─── Improved sketch filters ────────────────────────────────────────────────────
FILTERS = f"""
  <filter id="sketch" x="-35%" y="-35%" width="170%" height="170%">
    <feTurbulence type="fractalNoise" baseFrequency="0.042 0.058" numOctaves="3" seed="7" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="sketch-b" x="-25%" y="-25%" width="150%" height="150%">
    <feTurbulence type="fractalNoise" baseFrequency="0.038 0.048" numOctaves="3" seed="3" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="1.9" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="sketch-s" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.05 0.04" numOctaves="3" seed="11" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="1.2" xChannelSelector="R" yChannelSelector="G"/>
  </filter>"""

# ─── Glassware — border decoration ─────────────────────────────────────────────
SK  = G
SKW = '0.85'

MARTINI = f"""<symbol id="martini" viewBox="-18 -42 36 46" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <line x1="-15" y1="-38" x2="15" y2="-38"/>
    <line x1="-15" y1="-38" x2="0"  y2="-21"/>
    <line x1="15"  y1="-38" x2="0"  y2="-21"/>
    <line x1="0"   y1="-21" x2="0"  y2="-3.5"/>
    <line x1="-10" y1="-3.5" x2="10" y2="-3.5"/>
    <circle cx="0" cy="-31" r="2.4" stroke="{G3}" stroke-width="0.55"/>
    <line x1="0" y1="-28.6" x2="0" y2="-35.5" stroke="{G3}" stroke-width="0.45"/>
  </g>
</symbol>"""

COUPE_D = f"""<symbol id="coupe-d" viewBox="-18 -37 36 41" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -16,-33 Q -11,-25 0,-23 Q 11,-25 16,-33"/>
    <line x1="-16" y1="-33" x2="16" y2="-33"/>
    <line x1="0" y1="-23" x2="0" y2="-4.5"/>
    <line x1="-10" y1="-4.5" x2="10" y2="-4.5"/>
  </g>
</symbol>"""

WINE_GLASS_D = f"""<symbol id="wine-glass-d" viewBox="-14 -46 28 50" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -11,-42 Q -13,-30 -7,-24 Q -3.5,-21 0,-21 Q 3.5,-21 7,-24 Q 13,-30 11,-42"/>
    <line x1="-11" y1="-42" x2="11" y2="-42"/>
    <line x1="0" y1="-21" x2="0" y2="-4.5"/>
    <line x1="-9" y1="-4.5" x2="9" y2="-4.5"/>
  </g>
</symbol>"""

SHAKER_D = f"""<symbol id="shaker-d" viewBox="-13 -46 26 50" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -9.5,-15 Q -10.5,-4.5 -8.5,2 L 8.5,2 Q 10.5,-4.5 9.5,-15 Z"/>
    <path d="M -9.5,-15 Q -8.5,-25 -5.5,-33.5 L 5.5,-33.5 Q 8.5,-25 9.5,-15 Z"/>
    <path d="M -5.5,-33.5 Q -3.5,-41.5 0,-44 Q 3.5,-41.5 5.5,-33.5 Z"/>
    <line x1="-9.5" y1="-15" x2="9.5" y2="-15" stroke-width="1.15"/>
  </g>
</symbol>"""

JIGGER_D = f"""<symbol id="jigger-d" viewBox="-11 -30 22 32" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -8.5,-26 L -1.8,-13 L 1.8,-13 L 8.5,-26 Z"/>
    <line x1="-8.5" y1="-26" x2="8.5" y2="-26"/>
    <path d="M -1.8,-13 L -5.5,1 L 5.5,1 L 1.8,-13 Z"/>
    <line x1="-5.5" y1="1" x2="5.5" y2="1"/>
  </g>
</symbol>"""

STRAINER_D = f"""<symbol id="strainer-d" viewBox="-23 -13 46 15" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="-5.5" cy="0" r="9.5"/>
    <path d="M -15,0 Q -13,-4.5,-11,0 Q -9,4.5,-7,0 Q -5,-4.5,-3,0 Q -1,4.5,1,0 Q 3,-4.5,5.5,0"
          stroke="{G3}" stroke-width="0.65" opacity="0.82"/>
    <line x1="4"  y1="0"  x2="22" y2="-3.5"/>
    <line x1="4"  y1="0"  x2="22" y2="3.5"/>
    <line x1="22" y1="-3.5" x2="22" y2="3.5"/>
  </g>
</symbol>"""

NICK_NORA_D = f"""<symbol id="nick-nora-d" viewBox="-15 -42 30 46" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -11,-38 Q -13,-29 -7.5,-24 Q -3.5,-21 0,-21 Q 3.5,-21 7.5,-24 Q 13,-29 11,-38"/>
    <line x1="-11" y1="-38" x2="11" y2="-38"/>
    <line x1="0" y1="-21" x2="0" y2="-4.5"/>
    <line x1="-9" y1="-4.5" x2="9" y2="-4.5"/>
  </g>
</symbol>"""

CITRUS_D = f"""<symbol id="citrus-d" viewBox="-11 -11 22 22" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SKW}" fill="none" stroke-linecap="round">
    <circle cx="0" cy="0" r="8.5"/>
    <circle cx="0" cy="0" r="3.2"/>
    <line x1="0"    y1="-8.5" x2="0"   y2="8.5"  stroke-width="0.45"/>
    <line x1="-8.5" y1="0"    x2="8.5" y2="0"    stroke-width="0.45"/>
    <line x1="-6"   y1="-6"   x2="6"   y2="6"    stroke-width="0.35"/>
    <line x1="6"    y1="-6"   x2="-6"  y2="6"    stroke-width="0.35"/>
  </g>
</symbol>"""

# ─── Per-cocktail garnished glasses (gold, hand-drawn, with mint garnishes) ────

# Hibiscus Veil — Highball with lime wheel + hibiscus flower
GLASS_HV = f"""<symbol id="glass-hv" viewBox="-14 -57 33 61" overflow="visible">
  <!-- Glass body -->
  <g filter="url(#sketch)" stroke="{G}" stroke-width="0.88" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -9,-46 L -10.5,2 L 10.5,2 L 9,-46 Z"/>
    <!-- straw -->
    <line x1="4.5" y1="-49" x2="2.5" y2="2" stroke-width="0.78" opacity="0.88"/>
    <!-- ice cubes -->
    <rect x="-7.5" y="-32" width="6.5" height="5.5" rx="0.6" stroke="{G3}" stroke-width="0.52" opacity="0.72"/>
    <rect x="1"    y="-30" width="6.5" height="5.5" rx="0.6" stroke="{G3}" stroke-width="0.52" opacity="0.72"/>
    <rect x="-4"   y="-24" width="6"   height="5"   rx="0.5" stroke="{G3}" stroke-width="0.42" opacity="0.62"/>
    <!-- liquid level -->
    <path d="M -9,-16 Q 0,-15 9,-16" stroke="{G3}" stroke-width="0.38" opacity="0.55"/>
  </g>
  <!-- Lime wheel on rim (gold) -->
  <g filter="url(#sketch-s)">
    <circle cx="-6" cy="-46" r="5.5" stroke="{G3}" stroke-width="0.60" fill="none" opacity="0.82"/>
    <circle cx="-6" cy="-46" r="2.1" stroke="{G3}" stroke-width="0.38" fill="none" opacity="0.65"/>
    <line x1="-6" y1="-51.5" x2="-6" y2="-40.5" stroke="{G3}" stroke-width="0.28" opacity="0.52"/>
    <line x1="-11.5" y1="-46" x2="-0.5" y2="-46" stroke="{G3}" stroke-width="0.28" opacity="0.52"/>
    <line x1="-9.8" y1="-49.5" x2="-2.2" y2="-42.5" stroke="{G3}" stroke-width="0.22" opacity="0.42"/>
    <line x1="-9.8" y1="-42.5" x2="-2.2" y2="-49.5" stroke="{G3}" stroke-width="0.22" opacity="0.42"/>
  </g>
  <!-- Hibiscus flower on rim (mint green, 5-petal open bloom) -->
  <g filter="url(#sketch-s)" transform="translate(7.5,-47) rotate(-18)">
    {petal_ring(5, 7, 0.50, 10, M, '0.54', '0.65')}
    <!-- golden centre -->
    <circle r="1.8" fill="{G}" stroke="{G3}" stroke-width="0.35"/>
    <!-- stamens -->
    <line x1="0" y1="-2.5" x2="0.5" y2="-4.5" stroke="{G2}" stroke-width="0.32"/>
    <line x1="1.2" y1="-2" x2="2.2" y2="-3.8" stroke="{G2}" stroke-width="0.30"/>
    <line x1="-1.2" y1="-2" x2="-2" y2="-3.8" stroke="{G2}" stroke-width="0.30"/>
    <circle cx="0.5"  cy="-4.5" r="0.5" fill="{G2}"/>
    <circle cx="2.2"  cy="-3.8" r="0.45" fill="{G2}"/>
    <circle cx="-2"   cy="-3.8" r="0.45" fill="{G2}"/>
  </g>
  <!-- Short stem for flower -->
  <path d="M 7.5,-40 Q 9,-43 7.5,-46" stroke="{M3}" stroke-width="0.42" fill="none"
        filter="url(#sketch-s)" stroke-linecap="round"/>
  <!-- tiny leaf on stem -->
  <path d="M 8.5,-43 Q 12,-43 11.5,-46 Q 9,-43.5 8.5,-43"
        fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.32"
        filter="url(#sketch-s)"/>
</symbol>"""

# Golden Sour — Rocks glass with lemon twist + dehydrated lemon wheel + mint
GLASS_GS = f"""<symbol id="glass-gs" viewBox="-18 -44 40 47" overflow="visible">
  <!-- Glass body -->
  <g filter="url(#sketch)" stroke="{G}" stroke-width="0.88" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -11,-28 L -12.5,2 L 12.5,2 L 11,-28 Z"/>
    <!-- ice cubes -->
    <rect x="-9.5" y="-24" width="7" height="6"   rx="0.6" stroke="{G3}" stroke-width="0.52" opacity="0.72"/>
    <rect x="1.5"  y="-22" width="7" height="6"   rx="0.6" stroke="{G3}" stroke-width="0.52" opacity="0.72"/>
    <rect x="-4.5" y="-16" width="6.5" height="5.5" rx="0.5" stroke="{G3}" stroke-width="0.42" opacity="0.62"/>
    <!-- liquid -->
    <path d="M -11,-11 Q 0,-10 11,-11" stroke="{G3}" stroke-width="0.38" opacity="0.55"/>
  </g>
  <!-- Dehydrated lemon wheel inside glass -->
  <g filter="url(#sketch-s)">
    <circle cx="3.5" cy="-19" r="4.8" stroke="{G3}" stroke-width="0.50" fill="none" opacity="0.68"/>
    <circle cx="3.5" cy="-19" r="1.9" stroke="{G3}" stroke-width="0.32" fill="none" opacity="0.52"/>
    <line x1="3.5" y1="-23.8" x2="3.5" y2="-14.2" stroke="{G3}" stroke-width="0.24" opacity="0.46"/>
    <line x1="-1.3" y1="-19" x2="8.3" y2="-19" stroke="{G3}" stroke-width="0.24" opacity="0.46"/>
    <line x1="0.1" y1="-22.5" x2="6.9" y2="-15.5" stroke="{G3}" stroke-width="0.18" opacity="0.38"/>
    <line x1="0.1" y1="-15.5" x2="6.9" y2="-22.5" stroke="{G3}" stroke-width="0.18" opacity="0.38"/>
  </g>
  <!-- Lemon twist curling over the rim (gold) -->
  <g filter="url(#sketch-b)">
    <!-- Peel strip curling elegantly from rim -->
    <path d="M -11,-28 Q -14,-31 -15.5,-34 Q -16,-37.5 -14,-38.5 Q -12,-39.5 -11,-37 Q -10,-34.5 -12,-33 Q -14,-31.5 -15,-28"
          stroke="{G3}" stroke-width="0.65" fill="none" stroke-linecap="round"/>
    <!-- wedge on the rim -->
    <path d="M -11,-28 Q -7.5,-32 -4,-30 Q -2.5,-28 -4.5,-26 Q -7.5,-24.5 -11,-28"
          fill="{G3}" fill-opacity="0.20" stroke="{G3}" stroke-width="0.55"/>
    <path d="M -8,-30 Q -6.2,-29 -7,-27.5" stroke="{G3}" stroke-width="0.28" fill="none" opacity="0.62"/>
    <!-- small highlight lines on wedge -->
    <line x1="-7" y1="-31" x2="-5" y2="-29" stroke="{G3}" stroke-width="0.20" opacity="0.50"/>
  </g>
  <!-- Fresh mint sprig on right side of glass -->
  <g filter="url(#sketch-s)">
    <path d="M 11,-28 Q 14,-31.5 13,-36 Q 12.5,-39.5 14,-41.5"
          stroke="{M3}" stroke-width="0.48" fill="none" stroke-linecap="round"/>
    <path d="M 12,-30.5 Q 15.5,-29.5 16,-33 Q 13.5,-30.5 12,-30.5"
          fill="{M}" fill-opacity="0.25" stroke="{M}" stroke-width="0.40"/>
    <path d="M 12,-34 Q 16,-33 16.5,-36.5 Q 13.5,-34 12,-34"
          fill="{M}" fill-opacity="0.25" stroke="{M}" stroke-width="0.38"/>
    <path d="M 13,-37.5 Q 16.5,-36.5 16.5,-40 Q 14,-37.5 13,-37.5"
          fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.35"/>
    <!-- tiny blossom tip -->
    <g transform="translate(14,-41.5)">
      {petal_ring(5, 3.5, 0.44, 0, M, '0.52', '0.48')}
      <circle r="0.8" fill="{G}"/>
    </g>
  </g>
</symbol>"""

# Elderbloom Spritz — Wide balloon/spritz coupe with elderflower sprig + cucumber
GLASS_ES = f"""<symbol id="glass-es" viewBox="-21 -57 46 62" overflow="visible">
  <!-- Glass body — wide balloon coupe -->
  <g filter="url(#sketch)" stroke="{G}" stroke-width="0.88" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- bowl -->
    <path d="M -14,-43 Q -17,-29 -8.5,-22 Q -4.5,-18.5 0,-18.5 Q 4.5,-18.5 8.5,-22 Q 17,-29 14,-43"/>
    <line x1="-14" y1="-43" x2="14" y2="-43"/>
    <!-- stem -->
    <line x1="0" y1="-18.5" x2="0" y2="-4.5"/>
    <!-- base -->
    <line x1="-10" y1="-4.5" x2="10" y2="-4.5"/>
    <!-- bubbles -->
    <circle cx="-3.5" cy="-29" r="0.90" stroke="{G3}" stroke-width="0.38" opacity="0.78"/>
    <circle cx="3.5"  cy="-36" r="0.90" stroke="{G3}" stroke-width="0.38" opacity="0.78"/>
    <circle cx="0.5"  cy="-26" r="0.72" stroke="{G3}" stroke-width="0.30" opacity="0.68"/>
    <circle cx="-2"   cy="-41" r="0.72" stroke="{G3}" stroke-width="0.30" opacity="0.65"/>
    <circle cx="4.5"  cy="-33" r="0.58" stroke="{G3}" stroke-width="0.25" opacity="0.58"/>
    <circle cx="-5"   cy="-38" r="0.58" stroke="{G3}" stroke-width="0.25" opacity="0.58"/>
    <circle cx="1.5"  cy="-23" r="0.50" stroke="{G3}" stroke-width="0.22" opacity="0.48"/>
    <circle cx="-3"   cy="-32" r="0.50" stroke="{G3}" stroke-width="0.22" opacity="0.48"/>
    <!-- liquid fill line -->
    <path d="M -13,-34 Q 0,-32.5 13,-34" stroke="{G3}" stroke-width="0.38" opacity="0.52"/>
  </g>
  <!-- Elderflower sprig over right rim (mint) -->
  <g filter="url(#sketch-s)">
    <!-- Branching stem -->
    <path d="M 14,-43 Q 17,-47 15.5,-50 Q 14.5,-53 16.5,-55"
          stroke="{M3}" stroke-width="0.50" fill="none" stroke-linecap="round"/>
    <path d="M 15.5,-48 Q 19.5,-48.5 20.5,-52"
          stroke="{M3}" stroke-width="0.42" fill="none" stroke-linecap="round"/>
    <path d="M 15,-46 Q 18,-44.5 19,-41.5"
          stroke="{M3}" stroke-width="0.40" fill="none" stroke-linecap="round"/>
    <!-- Tiny leaf pairs on stem -->
    <path d="M 15.5,-48 Q 13.5,-49 13.5,-51.5 Q 15,-49.5 15.5,-48" fill="{M}" fill-opacity="0.22" stroke="{M}" stroke-width="0.32"/>
    <path d="M 15,-46 Q 13.5,-45 13.5,-43 Q 14.5,-45 15,-46" fill="{M}" fill-opacity="0.20" stroke="{M}" stroke-width="0.30"/>
    <!-- Elderflowers at branch tips (3 small 5-petal blooms) -->
    <g transform="translate(20.5,-52)">
      {petal_ring(5, 4.2, 0.44, 5, M, '0.54', '0.52')}
      <circle r="1.0" fill="{G}"/>
    </g>
    <g transform="translate(19,-41.5)">
      {petal_ring(5, 3.8, 0.44, 12, M, '0.50', '0.50')}
      <circle r="0.9" fill="{G}"/>
    </g>
    <g transform="translate(16.5,-55)">
      {petal_ring(5, 3.5, 0.44, 0, M, '0.56', '0.48')}
      <circle r="0.9" fill="{G}"/>
    </g>
  </g>
  <!-- Cucumber slice on left rim (mint green) -->
  <g filter="url(#sketch-s)">
    <ellipse cx="-15" cy="-43" rx="5" ry="3.2" stroke="{M3}" stroke-width="0.58" fill="none" opacity="0.82"/>
    <ellipse cx="-15" cy="-43" rx="2.0" ry="1.3" stroke="{M3}" stroke-width="0.35" fill="none" opacity="0.65"/>
    <!-- radial segments -->
    <line x1="-15" y1="-46.2" x2="-15" y2="-39.8" stroke="{M3}" stroke-width="0.22" opacity="0.50"/>
    <line x1="-20" y1="-43"   x2="-10" y2="-43"   stroke="{M3}" stroke-width="0.22" opacity="0.50"/>
    <line x1="-18.6" y1="-45.7" x2="-11.4" y2="-40.3" stroke="{M3}" stroke-width="0.18" opacity="0.42"/>
    <line x1="-18.6" y1="-40.3" x2="-11.4" y2="-45.7" stroke="{M3}" stroke-width="0.18" opacity="0.42"/>
    <!-- cucumber seeds hint -->
    <ellipse cx="-16" cy="-43.5" rx="0.55" ry="0.35" fill="{M3}" fill-opacity="0.45"/>
    <ellipse cx="-14" cy="-42.5" rx="0.55" ry="0.35" fill="{M3}" fill-opacity="0.40"/>
  </g>
</symbol>"""

# ─── Placement helpers ─────────────────────────────────────────────────────────
def useb(sym, cx, cy, w, h=None, rot=0):
    if h is None: h = w
    tr = f'transform="rotate({rot},{cx},{cy})"' if rot else ""
    return (f'<g filter="url(#sketch-b)" {tr}>'
            f'<use href="#{sym}" x="{cx-w/2:.2f}" y="{cy-h/2:.2f}" width="{w}" height="{h}"/>'
            f'</g>')

def uses(sym, cx, cy, w, h=None, rot=0):
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
  {MARTINI} {COUPE_D} {WINE_GLASS_D} {SHAKER_D} {JIGGER_D} {STRAINER_D} {NICK_NORA_D} {CITRUS_D}
  {GLASS_HV} {GLASS_GS} {GLASS_ES}
</defs>

<!-- Double gold frame -->
<rect x="6.5" y="6.5" width="135" height="197" fill="none" stroke="{G}" stroke-width="0.80" opacity="0.68"/>
<rect x="8.2" y="8.2" width="131.6" height="193.6" fill="none" stroke="{G}" stroke-width="0.28" opacity="0.40"/>

<!-- Corner ornaments -->
<g stroke="{G}" fill="none" opacity="0.80">
  <polyline points="6.5,22 6.5,14 10,14 10,10 14,10 14,6.5 22,6.5" stroke-width="0.55"/>
  <path d="M 6.5,18 Q 12,12 18,6.5" stroke-width="0.28" opacity="0.62"/>
  <polygon points="10,14 11.4,12 12.8,14 11.4,16" fill="{G}" opacity="0.90"/>
  <polygon points="14,10 15.4,8  16.8,10 15.4,12" fill="{G}" opacity="0.90"/>

  <polyline points="141.5,22 141.5,14 138,14 138,10 134,10 134,6.5 126,6.5" stroke-width="0.55"/>
  <path d="M 141.5,18 Q 136,12 130,6.5" stroke-width="0.28" opacity="0.62"/>
  <polygon points="138,14 136.6,12 135.2,14 136.6,16" fill="{G}" opacity="0.90"/>
  <polygon points="134,10 132.6,8  131.2,10 132.6,12" fill="{G}" opacity="0.90"/>

  <polyline points="6.5,188 6.5,196 10,196 10,200 14,200 14,203.5 22,203.5" stroke-width="0.55"/>
  <path d="M 6.5,192 Q 12,198 18,203.5" stroke-width="0.28" opacity="0.62"/>
  <polygon points="10,196 11.4,198 12.8,196 11.4,194" fill="{G}" opacity="0.90"/>
  <polygon points="14,200 15.4,202 16.8,200 15.4,198" fill="{G}" opacity="0.90"/>

  <polyline points="141.5,188 141.5,196 138,196 138,200 134,200 134,203.5 126,203.5" stroke-width="0.55"/>
  <path d="M 141.5,192 Q 136,198 130,203.5" stroke-width="0.28" opacity="0.62"/>
  <polygon points="138,196 136.6,198 135.2,196 136.6,194" fill="{G}" opacity="0.90"/>
  <polygon points="134,200 132.6,202 131.2,200 132.6,198" fill="{G}" opacity="0.90"/>
</g>

<!-- ═══════ TOP-LEFT cluster (taller — no TADOW above) ═══════ -->
{useb('wf8',   15,  16, 26)}
{useb('wf5b',  29,   8, 20)}
{useb('sprig',  8,   9, 19, 27, 10)}
{useb('bud',   33,  28, 14)}
{useb('branch', 11, 30, 22, 30,-14)}
{useb('berries',31, 27, 20, 22, 10)}
{useb('tendril', 8, 22, 18, 24,  5)}
<g transform="translate(13,14) rotate(-10) scale(0.56)">
  <use href="#martini" x="-18" y="-42" width="36" height="46"/>
</g>
<g transform="translate(34,18) rotate(8) scale(0.52)">
  <use href="#jigger-d" x="-11" y="-30" width="22" height="32"/>
</g>
{uses('wf6',  21,  6, 14)}
{uses('bloom', 30, 34, 15, 21, -6)}
{uses('tiny',   7, 33, 10)}

<!-- ═══════ TOP-RIGHT cluster ═══════ -->
{useb('wf5',  133,  16, 24)}
{useb('wf8',  119,   8, 26)}
{useb('sprig',140,   9, 19, 27, -10)}
{useb('bud',  115,  28, 14)}
{useb('branch',137, 30, 22, 30, 14)}
{useb('berries',117,27, 20, 22,-10)}
{useb('tendril',140,22, 18, 24, -5)}
<g transform="translate(135,14) rotate(10) scale(0.56)">
  <use href="#coupe-d" x="-18" y="-37" width="36" height="41"/>
</g>
<g transform="translate(116,24) rotate(-5) scale(0.66)">
  <use href="#citrus-d" x="-11" y="-11" width="22" height="22"/>
</g>
{uses('wf6',  127,  6, 14)}
{uses('bloom', 118, 34, 15, 21, 6)}
{uses('tiny',  141, 33, 10)}

<!-- ═══════ BOTTOM-LEFT cluster ═══════ -->
{useb('wf5b',  15, 196, 24)}
{useb('wf8',   29, 188, 26)}
{useb('sprig',  8, 204, 19, 27, 12)}
{useb('bud',   33, 184, 14)}
{useb('branch', 11,185, 22, 30, 10)}
{useb('berries',31,202, 20, 22, -7)}
{useb('tendril', 8,192, 18, 24, 10)}
<g transform="translate(18,186) rotate(-7) scale(0.54)">
  <use href="#wine-glass-d" x="-14" y="-46" width="28" height="50"/>
</g>
<g transform="translate(34,200) rotate(12) scale(0.56)">
  <use href="#strainer-d" x="-23" y="-13" width="46" height="15"/>
</g>
{uses('wf6',   21, 207, 14)}
{uses('bloom',  30,180, 15, 21,  5)}
{uses('tiny',    7,181, 10)}

<!-- ═══════ BOTTOM-RIGHT cluster ═══════ -->
{useb('wf8',  133, 196, 26)}
{useb('wf5',  118, 188, 24)}
{useb('sprig',140, 204, 19, 27,-12)}
{useb('bud',  115, 184, 14)}
{useb('branch',137,185, 22, 30,-10)}
{useb('berries',117,202,20, 22,  8)}
{useb('tendril',140,192,18, 24,-10)}
<g transform="translate(122,185) rotate(5) scale(0.52)">
  <use href="#shaker-d" x="-13" y="-46" width="26" height="50"/>
</g>
<g transform="translate(136,199) rotate(-9) scale(0.54)">
  <use href="#nick-nora-d" x="-15" y="-42" width="30" height="46"/>
</g>
{uses('wf6',  127, 207, 14)}
{uses('bloom', 118,180, 15, 21, -5)}
{uses('tiny',  141, 181, 10)}

<!-- ═══════ LEFT garland — full height, denser ═══════ -->
{useb('branch',  10,  38, 17, 25,  9)}
{uses('tiny',    13,  50, 10)}
{useb('berries', 10,  60, 15, 19, -5)}
{uses('bloom',   12,  72, 14, 20,  5)}
{useb('sprig',   10,  86, 17, 25,  6)}
{uses('tiny',    13,  97, 10)}
{useb('herb',     9, 107, 12, 20, 10)}
{uses('wf6',     13, 118, 13)}
{useb('branch',  10, 129, 17, 25, -8)}
{uses('bloom',   12, 141, 14, 20,  4)}
{useb('tendril',  9, 153, 15, 22,  5)}
{uses('tiny',    13, 164, 10)}
{useb('berries', 10, 174, 15, 19, 10)}
{uses('wf5',     13, 185, 14)}

<!-- ═══════ RIGHT garland — full height, denser ═══════ -->
{useb('branch', 138,  38, 17, 25, -9)}
{uses('tiny',   135,  50, 10)}
{useb('berries',138,  60, 15, 19,  5)}
{uses('bloom',  136,  72, 14, 20, -5)}
{useb('sprig',  138,  86, 17, 25, -6)}
{uses('tiny',   135,  97, 10)}
{useb('herb',   139, 107, 12, 20,-10)}
{uses('wf6',    135, 118, 13)}
{useb('branch', 138, 129, 17, 25,  8)}
{uses('bloom',  136, 141, 14, 20, -4)}
{useb('tendril',139, 153, 15, 22, -5)}
{uses('tiny',   135, 164, 10)}
{useb('berries',138, 174, 15, 19,-10)}
{uses('wf5',    135, 185, 14)}
</svg>"""

# ─── Cocktail glass SVGs (reference symbols defined in DECO) ──────────────────
def glass_svg(sym_id, vx, vy, vw, vh, dw_mm, dh_mm):
    """Inline SVG that references a symbol from the DECO SVG in the same document."""
    return (f'<svg width="{dw_mm}mm" height="{dh_mm}mm" viewBox="{vx} {vy} {vw} {vh}" '
            f'xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto 3mm;">'
            f'<use href="#{sym_id}" x="{vx}" y="{vy}" width="{vw}" height="{vh}"/>'
            f'</svg>')

# Highball (HV): viewBox="-14 -57 33 61"  → 33×61 units → scale to 16×26mm
icon_hv = glass_svg('glass-hv', -14, -57, 33, 61, 16, 26)
# Rocks (GS): viewBox="-18 -44 40 47"     → 40×47 units → scale to 18×20mm
icon_gs = glass_svg('glass-gs', -18, -44, 40, 47, 18, 20)
# Spritz coupe (ES): viewBox="-21 -57 46 62" → 46×62 units → scale to 20×24mm
icon_es = glass_svg('glass-es', -21, -57, 46, 62, 20, 24)

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
  padding: 16mm 17mm 13mm;
}}

/* ── Header ── */
.menu-header {{
  width: 100%; text-align: center; margin-bottom: 3mm;
}}
.header-row {{
  display: flex; align-items: center; width: 100%; margin-bottom: 2mm;
}}
.header-line {{ flex: 1; height: 0.35px; background: {G}; opacity: 0.55; }}
.header-dot {{
  width: 2.8px; height: 2.8px; background: {G};
  border-radius: 50%; margin: 0 6px; opacity: 0.72;
}}
.menu-script {{
  font-family: 'Lora', serif; font-weight: 400; font-style: italic;
  font-size: 16px; color: {G}; letter-spacing: 0.03em;
}}
.header-sub {{
  font-family: 'Poppins', sans-serif; font-weight: 300;
  font-size: 4.8px; letter-spacing: 0.35em; color: {G3};
  text-transform: uppercase; margin-top: 1mm;
}}

/* ── Cocktail cards ── */
.cocktails {{
  flex: 1; display: flex; flex-direction: column;
  justify-content: space-evenly; align-items: center; width: 100%;
}}
.cocktail {{ text-align: center; width: 100%; }}

.drink-name {{
  font-family: 'Lora', serif; font-weight: 700; font-size: 15.5px;
  color: #ECEAE0; margin-bottom: 1.8mm; letter-spacing: 0.03em;
}}
.tasting-note {{
  font-family: 'Lora', serif; font-weight: 400; font-style: italic;
  font-size: 8.5px; color: #A8B4A0; line-height: 1.52;
  margin-bottom: 1.8mm; padding: 0 2mm;
}}
.ingredients {{
  font-family: 'Poppins', sans-serif; font-weight: 300;
  font-size: 5.2px; letter-spacing: 0.18em; color: {M3};
  text-transform: uppercase; line-height: 1.65;
}}
.diamond {{ color: {G}; }}

/* ── Dividers ── */
.divider {{
  display: flex; align-items: center; width: 82%;
}}
.div-line {{ flex: 1; height: 0.3px; background: {G}; opacity: 0.45; }}
.div-center {{
  display: flex; gap: 3.5px; padding: 0 5px;
  font-size: 4.5px; color: {G}; line-height: 1; opacity: 0.70;
}}

/* ── Footer ── */
.footer {{ text-align: center; margin-top: 1.5mm; }}
.footer-rule {{
  display: flex; align-items: center; margin-bottom: 1.2mm;
}}
.footer-line {{ flex: 1; height: 0.28px; background: {G}; opacity: 0.40; }}
.footer-diamond {{ font-size: 4.5px; color: {G3}; padding: 0 5px; opacity: 0.75; }}
.footer-text {{
  font-family: 'Poppins', sans-serif; font-weight: 300;
  font-size: 4.2px; letter-spacing: 0.38em; color: {G3};
  text-transform: uppercase; opacity: 0.80;
}}
</style>
</head>
<body>
<div class="page">

  {DECO}

  <div class="content">

    <div class="menu-header">
      <div class="header-row">
        <div class="header-line"></div>
        <div class="header-dot"></div>
        <div class="header-line"></div>
      </div>
      <div class="menu-script">Cocktails Menu</div>
      <div class="header-sub">A · Tadow · Est. 2023</div>
      <div class="header-row" style="margin-top:1.8mm; margin-bottom:0;">
        <div class="header-line"></div>
        <div class="header-dot"></div>
        <div class="header-line"></div>
      </div>
    </div>

    <div class="cocktails">

      <div class="cocktail">
        {icon_hv}
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
        {icon_gs}
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
        {icon_es}
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
