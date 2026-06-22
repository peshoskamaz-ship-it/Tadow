#!/usr/bin/env python3
"""Generate A5 cocktail menu HTML."""
import base64, math, os

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

lr = b64('/tmp/fonts/lora-regular.ttf')
lb = b64('/tmp/fonts/lora-bold.ttf')
li = b64('/tmp/fonts/lora-italic.ttf')
pl = b64('/tmp/fonts/poppins-light.ttf')

# ─── SVG path helpers ──────────────────────────────────────────────────────────
def petal(r, wf=0.50):
    w = r * wf
    return (f"M 0,0 C {w*0.7:.2f},{-r*0.08:.2f} {w*0.95:.2f},{-r*0.62:.2f} 0,{-r:.2f} "
            f"C {-w*0.95:.2f},{-r*0.62:.2f} {-w*0.7:.2f},{-r*0.08:.2f} 0,0 Z")

def thin_petal(r, wf=0.20):
    w = r * wf
    return (f"M 0,0 C {w:.2f},{-r*0.15:.2f} {w*0.85:.2f},{-r*0.75:.2f} 0,{-r:.2f} "
            f"C {-w*0.85:.2f},{-r*0.75:.2f} {-w:.2f},{-r*0.15:.2f} 0,0 Z")

def broad_petal(r, wf=0.62):
    w = r * wf
    tip = r * 0.10
    return (f"M 0,0 C {w*0.75:.2f},{-r*0.08:.2f} {w*1.05:.2f},{-r*0.50:.2f} {w*0.6:.2f},{-(r-tip):.2f} "
            f"Q 0,{-(r+tip*0.5):.2f} {-w*0.6:.2f},{-(r-tip):.2f} "
            f"C {-w*1.05:.2f},{-r*0.50:.2f} {-w*0.75:.2f},{-r*0.08:.2f} 0,0 Z")

def ring(fn, n, r, wf, offset, fill, stroke_c=None, sw=0.0):
    parts = []
    step = 360 / n
    sk = f' stroke="{stroke_c}" stroke-width="{sw}"' if stroke_c else ' stroke="none"'
    for i in range(n):
        a = offset + step * i
        parts.append(f'<path d="{fn(r,wf)}" fill="{fill}"{sk} transform="rotate({a:.1f})"/>')
    return "\n".join(parts)

def stamen_dots(n, radius, dot_r, fill):
    out = []
    for i in range(n):
        a = math.radians(i * 360 / n)
        out.append(f'<circle cx="{radius*math.cos(a):.2f}" cy="{radius*math.sin(a):.2f}" r="{dot_r}" fill="{fill}"/>')
    return "".join(out)

# ─── SVG Symbols ──────────────────────────────────────────────────────────────

ROSE = f"""<symbol id="rose" viewBox="-22 -22 44 44" overflow="visible">
  <defs>
    <radialGradient id="rg-ro" cx="0" cy="0" r="20" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#A85040"/>
      <stop offset="0.4" stop-color="#D89080"/>
      <stop offset="1" stop-color="#F8DDD5"/>
    </radialGradient>
    <radialGradient id="rg-rm" cx="0" cy="0" r="14" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#904030"/>
      <stop offset="1" stop-color="#E0A898"/>
    </radialGradient>
    <radialGradient id="rg-ri" cx="0" cy="0" r="9" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#703020"/>
      <stop offset="1" stop-color="#C07060"/>
    </radialGradient>
  </defs>
  {ring(petal,5,18,0.52,0,'url(#rg-ro)')}
  {ring(petal,5,13,0.48,36,'url(#rg-rm)')}
  {ring(petal,5,8,0.44,18,'url(#rg-ri)')}
  <circle r="3.2" fill="#6A2820"/>
  {stamen_dots(8,2.2,0.55,'#F0C870')}
  <circle r="1.3" fill="#E09040"/>
</symbol>"""

MUM = f"""<symbol id="mum" viewBox="-20 -20 40 40" overflow="visible">
  <defs>
    <radialGradient id="rg-mo" cx="0" cy="0" r="18" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#A07820"/>
      <stop offset="0.5" stop-color="#D4A840"/>
      <stop offset="1" stop-color="#F2D888"/>
    </radialGradient>
    <radialGradient id="rg-mi" cx="0" cy="0" r="11" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#806010"/>
      <stop offset="1" stop-color="#C89030"/>
    </radialGradient>
  </defs>
  {ring(thin_petal,16,15,0.22,0,'url(#rg-mo)')}
  {ring(thin_petal,12,10,0.24,15,'url(#rg-mi)')}
  {ring(thin_petal,7,6,0.28,0,'#A07828')}
  <circle r="2.5" fill="#705010"/>
  {stamen_dots(6,1.5,0.45,'#F8E080')}
</symbol>"""

COSMOS = f"""<symbol id="cosmos" viewBox="-20 -20 40 40" overflow="visible">
  <defs>
    <radialGradient id="rg-cs" cx="0" cy="0" r="19" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#988010"/>
      <stop offset="0.45" stop-color="#C8A030"/>
      <stop offset="1" stop-color="#EDD880"/>
    </radialGradient>
  </defs>
  {ring(broad_petal,8,16,0.60,0,'url(#rg-cs)')}
  <circle r="4" fill="#806010"/>
  {stamen_dots(10,2.8,0.5,'#F4DC60')}
  <circle r="1.8" fill="#C09020"/>
</symbol>"""

DAISY = f"""<symbol id="daisy" viewBox="-20 -20 40 40" overflow="visible">
  <defs>
    <radialGradient id="rg-dy" cx="0" cy="0" r="18" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#C0B090"/>
      <stop offset="0.5" stop-color="#E8D8B8"/>
      <stop offset="1" stop-color="#FAF0DC"/>
    </radialGradient>
  </defs>
  {ring(petal,16,15,0.35,0,'url(#rg-dy)')}
  {ring(petal,10,9,0.38,18,'#EDE0C0')}
  <circle r="4" fill="#D4A820"/>
  {stamen_dots(12,2.8,0.4,'#F8D860')}
  <circle r="1.5" fill="#A07818"/>
</symbol>"""

TULIP = """<symbol id="tulip" viewBox="-16 -36 32 50" overflow="visible">
  <defs>
    <radialGradient id="rg-tl" cx="0" cy="-20" r="22" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ECD4D0"/>
      <stop offset="0.6" stop-color="#D8A8A0"/>
      <stop offset="1" stop-color="#C08080"/>
    </radialGradient>
  </defs>
  <!-- Left petal -->
  <path d="M -1,0 C -9,-4 -15,-20 -11,-30 C -9,-33 -5,-30 -3,-22 C -2,-15 -1,-8 0,0 Z"
        fill="url(#rg-tl)" stroke="#B07070" stroke-width="0.25"/>
  <!-- Right petal (mirror) -->
  <path d="M 1,0 C 9,-4 15,-20 11,-30 C 9,-33 5,-30 3,-22 C 2,-15 1,-8 0,0 Z"
        fill="url(#rg-tl)" stroke="#B07070" stroke-width="0.25"/>
  <!-- Middle petal (tallest) -->
  <path d="M -3,0 C -9,-6 -9,-24 0,-32 C 9,-24 9,-6 3,0 Z"
        fill="#EAC0B8" stroke="#B07878" stroke-width="0.25"/>
  <!-- Stem -->
  <line x1="0" y1="0" x2="0" y2="14" stroke="#5A8050" stroke-width="1.2" stroke-linecap="round"/>
  <!-- Leaves -->
  <path d="M 0,4 Q -10,6 -12,12 Q -6,11 0,7 Z" fill="#6A9060"/>
  <path d="M 0,8 Q 9,9 11,15 Q 5,14 0,10 Z" fill="#5A8050"/>
</symbol>"""

BLOSSOM = """<symbol id="blossom" viewBox="-10 -10 20 20" overflow="visible">
  <defs>
    <radialGradient id="rg-bl" cx="0" cy="0" r="9" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#B08830"/>
      <stop offset="1" stop-color="#EDD898"/>
    </radialGradient>
  </defs>
  <path d="M 0,0 C 2,-1 3,-6 0,-8 C -3,-6 -2,-1 0,0 Z" fill="url(#rg-bl)" transform="rotate(0)"/>
  <path d="M 0,0 C 2,-1 3,-6 0,-8 C -3,-6 -2,-1 0,0 Z" fill="url(#rg-bl)" transform="rotate(72)"/>
  <path d="M 0,0 C 2,-1 3,-6 0,-8 C -3,-6 -2,-1 0,0 Z" fill="url(#rg-bl)" transform="rotate(144)"/>
  <path d="M 0,0 C 2,-1 3,-6 0,-8 C -3,-6 -2,-1 0,0 Z" fill="url(#rg-bl)" transform="rotate(216)"/>
  <path d="M 0,0 C 2,-1 3,-6 0,-8 C -3,-6 -2,-1 0,0 Z" fill="url(#rg-bl)" transform="rotate(288)"/>
  <circle r="2" fill="#E0A840"/>
</symbol>"""

BLOSSOM_C = """<symbol id="blossom-c" viewBox="-10 -10 20 20" overflow="visible">
  <path d="M 0,0 C 2,-1 3,-6 0,-8 C -3,-6 -2,-1 0,0 Z" fill="#F0E0C0" transform="rotate(0)"/>
  <path d="M 0,0 C 2,-1 3,-6 0,-8 C -3,-6 -2,-1 0,0 Z" fill="#F0E0C0" transform="rotate(72)"/>
  <path d="M 0,0 C 2,-1 3,-6 0,-8 C -3,-6 -2,-1 0,0 Z" fill="#EDD8B0" transform="rotate(144)"/>
  <path d="M 0,0 C 2,-1 3,-6 0,-8 C -3,-6 -2,-1 0,0 Z" fill="#EDD8B0" transform="rotate(216)"/>
  <path d="M 0,0 C 2,-1 3,-6 0,-8 C -3,-6 -2,-1 0,0 Z" fill="#F0E0C0" transform="rotate(288)"/>
  <circle r="2" fill="#D4C080"/>
</symbol>"""

BERRY = """<symbol id="berry" viewBox="-12 -10 24 16" overflow="visible">
  <circle cx="0" cy="-6" r="3.5" fill="#C9A24B" opacity="0.9"/>
  <circle cx="-5" cy="0" r="3" fill="#D4B060" opacity="0.85"/>
  <circle cx="5" cy="0" r="3" fill="#B88830" opacity="0.85"/>
  <circle cx="-2" cy="-2" r="2" fill="#E0C070" opacity="0.7"/>
  <circle cx="2" cy="-1.5" r="1.8" fill="#C8A048" opacity="0.7"/>
  <!-- stems -->
  <path d="M 0,-2.5 Q 0,-4, 0,-6" stroke="#6A8A50" stroke-width="0.6" fill="none"/>
  <path d="M -2,-0.5 Q -3,-2, -5,0" stroke="#6A8A50" stroke-width="0.6" fill="none"/>
  <path d="M 2,-0.5 Q 3,-2, 5,0" stroke="#6A8A50" stroke-width="0.6" fill="none"/>
</symbol>"""

SPRIG = """<symbol id="sprig" viewBox="-14 -24 28 26" overflow="visible">
  <!-- main stem -->
  <path d="M 0,2 Q 1,-10, 0,-22" stroke="#5A8050" stroke-width="0.9" fill="none"/>
  <!-- leaf pairs -->
  <ellipse cx="-5" cy="-4" rx="5" ry="2.5" fill="#6A9060" transform="rotate(-30,-5,-4)"/>
  <ellipse cx="5" cy="-4" rx="5" ry="2.5" fill="#5A8050" transform="rotate(30,5,-4)"/>
  <ellipse cx="-5" cy="-10" rx="4.5" ry="2.2" fill="#6A9060" transform="rotate(-25,-5,-10)"/>
  <ellipse cx="5" cy="-10" rx="4.5" ry="2.2" fill="#5A8050" transform="rotate(25,5,-10)"/>
  <ellipse cx="-4" cy="-16" rx="4" ry="2" fill="#6A9060" transform="rotate(-20,-4,-16)"/>
  <ellipse cx="4" cy="-16" rx="4" ry="2" fill="#5A8050" transform="rotate(20,4,-16)"/>
  <ellipse cx="0" cy="-22" rx="3" ry="1.8" fill="#7AA070"/>
</symbol>"""

SK_FILTER = """<filter id="sketch" x="-30%" y="-30%" width="160%" height="160%" color-interpolation-filters="linearRGB">
  <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="7" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="2.3" xChannelSelector="R" yChannelSelector="G"/>
</filter>"""

SK = '#DAD2BE'  # sketch stroke color
SK2 = '#C0B8A4'
SK_W = '0.8'

MARTINI = f"""<symbol id="martini" viewBox="-17 -40 34 44" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SK_W}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <line x1="-14" y1="-36" x2="14" y2="-36"/>
    <line x1="-14" y1="-36" x2="0" y2="-20"/>
    <line x1="14" y1="-36" x2="0" y2="-20"/>
    <line x1="0" y1="-20" x2="0" y2="-3"/>
    <line x1="-10" y1="-3" x2="10" y2="-3"/>
    <!-- olive -->
    <circle cx="-4" cy="-30" r="2" stroke="{SK2}" stroke-width="0.5"/>
    <circle cx="4" cy="-30" r="2" stroke="{SK2}" stroke-width="0.5"/>
    <line x1="-4" y1="-28" x2="4" y2="-28" stroke="{SK2}" stroke-width="0.4"/>
  </g>
</symbol>"""

COUPE = f"""<symbol id="coupe" viewBox="-17 -36 34 40" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SK_W}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -15,-32 Q -10,-24 0,-22 Q 10,-24 15,-32"/>
    <line x1="-15" y1="-32" x2="15" y2="-32"/>
    <line x1="0" y1="-22" x2="0" y2="-4"/>
    <line x1="-9" y1="-4" x2="9" y2="-4"/>
  </g>
</symbol>"""

WINE_GLASS = f"""<symbol id="wine-glass" viewBox="-12 -44 24 48" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SK_W}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -10,-40 Q -11,-28 -6,-24 Q -3,-20 0,-20 Q 3,-20 6,-24 Q 11,-28 10,-40"/>
    <line x1="-10" y1="-40" x2="10" y2="-40"/>
    <!-- liquid line at 2/3 -->
    <path d="M -7,-30 Q 0,-28 7,-30" stroke="{SK2}" stroke-width="0.5" opacity="0.7"/>
    <line x1="0" y1="-20" x2="0" y2="-4"/>
    <line x1="-8" y1="-4" x2="8" y2="-4"/>
  </g>
</symbol>"""

NICK_NORA = f"""<symbol id="nick-nora" viewBox="-14 -40 28 44" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SK_W}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -11,-36 Q -13,-28 -8,-24 Q -4,-20 0,-20 Q 4,-20 8,-24 Q 13,-28 11,-36"/>
    <line x1="-11" y1="-36" x2="11" y2="-36"/>
    <line x1="0" y1="-20" x2="0" y2="-4"/>
    <line x1="-8" y1="-4" x2="8" y2="-4"/>
  </g>
</symbol>"""

HIGHBALL = f"""<symbol id="highball" viewBox="-10 -42 32 46" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SK_W}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- glass body -->
    <path d="M -8,-38 L -9,2 L 9,2 L 8,-38 Z"/>
    <!-- liquid -->
    <path d="M -8.5,-20 L -8.8,2" stroke="{SK2}" stroke-width="0.4" opacity="0.0"/>
    <!-- straw -->
    <line x1="4" y1="-40" x2="2" y2="2" stroke="{SK}" stroke-width="0.7" opacity="0.9"/>
    <!-- lime wheel on rim -->
    <circle cx="-3" cy="-36" r="4" stroke="{SK2}" stroke-width="0.5" opacity="0.8"/>
    <line x1="-3" y1="-40" x2="-3" y2="-32" stroke="{SK2}" stroke-width="0.4" opacity="0.6"/>
    <line x1="-7" y1="-36" x2="1" y2="-36" stroke="{SK2}" stroke-width="0.4" opacity="0.6"/>
    <line x1="-6" y1="-39" x2="0" y2="-33" stroke="{SK2}" stroke-width="0.3" opacity="0.5"/>
    <line x1="-6" y1="-33" x2="0" y2="-39" stroke="{SK2}" stroke-width="0.3" opacity="0.5"/>
  </g>
</symbol>"""

ROCKS = f"""<symbol id="rocks" viewBox="-12 -28 24 32" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SK_W}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -10,-24 L -11,2 L 11,2 L 10,-24 Z"/>
    <!-- ice cubes -->
    <rect x="-7" y="-20" width="6" height="5" rx="0.5" stroke="{SK2}" stroke-width="0.5" opacity="0.7"/>
    <rect x="1" y="-18" width="6" height="5" rx="0.5" stroke="{SK2}" stroke-width="0.5" opacity="0.7"/>
    <rect x="-4" y="-13" width="5" height="4" rx="0.5" stroke="{SK2}" stroke-width="0.4" opacity="0.6"/>
    <!-- liquid surface -->
    <path d="M -9,-9 Q 0,-8 9,-9" stroke="{SK2}" stroke-width="0.4" opacity="0.6"/>
  </g>
</symbol>"""

FLUTE = f"""<symbol id="flute" viewBox="-8 -48 16 52" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SK_W}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M -5,-44 Q -7,-24 -4,-18 Q -2,-14 0,-14 Q 2,-14 4,-18 Q 7,-24 5,-44 Z"/>
    <line x1="-5" y1="-44" x2="5" y2="-44"/>
    <line x1="0" y1="-14" x2="0" y2="-2"/>
    <line x1="-6" y1="-2" x2="6" y2="-2"/>
    <!-- bubbles -->
    <circle cx="-2" cy="-30" r="0.8" stroke="{SK2}" stroke-width="0.4" opacity="0.8"/>
    <circle cx="2" cy="-36" r="0.8" stroke="{SK2}" stroke-width="0.4" opacity="0.8"/>
    <circle cx="0" cy="-24" r="0.6" stroke="{SK2}" stroke-width="0.3" opacity="0.7"/>
    <circle cx="-1" cy="-42" r="0.6" stroke="{SK2}" stroke-width="0.3" opacity="0.7"/>
    <circle cx="2" cy="-20" r="0.5" stroke="{SK2}" stroke-width="0.3" opacity="0.6"/>
  </g>
</symbol>"""

SHAKER = f"""<symbol id="shaker" viewBox="-12 -44 24 48" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SK_W}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- tin body -->
    <path d="M -9,-14 Q -10,-4 -8,2 L 8,2 Q 10,-4 9,-14 Z"/>
    <!-- cap -->
    <path d="M -9,-14 Q -8,-24 -5,-32 L 5,-32 Q 8,-24 9,-14 Z"/>
    <!-- top cap -->
    <path d="M -5,-32 Q -3,-40 0,-42 Q 3,-40 5,-32 Z"/>
    <!-- strainer band -->
    <line x1="-9" y1="-14" x2="9" y2="-14" stroke-width="1.2"/>
    <!-- small strainer holes line -->
    <path d="M -6,-16 Q 0,-17 6,-16" stroke="{SK2}" stroke-width="0.4" opacity="0.7"/>
  </g>
</symbol>"""

JIGGER = f"""<symbol id="jigger" viewBox="-10 -28 20 30" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SK_W}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- large cone (top) -->
    <path d="M -8,-24 L -1.5,-12 L 1.5,-12 L 8,-24 Z"/>
    <line x1="-8" y1="-24" x2="8" y2="-24"/>
    <!-- small cone (bottom) -->
    <path d="M -1.5,-12 L -5,0 L 5,0 L 1.5,-12 Z"/>
    <line x1="-5" y1="0" x2="5" y2="0"/>
  </g>
</symbol>"""

STRAINER = f"""<symbol id="strainer" viewBox="-22 -12 44 14" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SK_W}" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <!-- disc -->
    <circle cx="-5" cy="0" r="9"/>
    <!-- spring/coil -->
    <path d="M -14,0 Q -12,-4 -10,0 Q -8,4 -6,0 Q -4,-4 -2,0 Q 0,4 2,0 Q 4,-4 6,0"
          stroke="{SK2}" stroke-width="0.7" opacity="0.9"/>
    <!-- handle -->
    <line x1="4" y1="0" x2="21" y2="-3"/>
    <line x1="4" y1="0" x2="21" y2="3"/>
    <line x1="21" y1="-3" x2="21" y2="3" stroke-linecap="round"/>
  </g>
</symbol>"""

CITRUS = f"""<symbol id="citrus" viewBox="-10 -10 20 20" overflow="visible">
  <g filter="url(#sketch)" stroke="{SK}" stroke-width="{SK_W}" fill="none" stroke-linecap="round">
    <circle cx="0" cy="0" r="8"/>
    <circle cx="0" cy="0" r="3"/>
    <line x1="0" y1="-8" x2="0" y2="8" stroke-width="0.5"/>
    <line x1="-8" y1="0" x2="8" y2="0" stroke-width="0.5"/>
    <line x1="-5.6" y1="-5.6" x2="5.6" y2="5.6" stroke-width="0.4"/>
    <line x1="5.6" y1="-5.6" x2="-5.6" y2="5.6" stroke-width="0.4"/>
  </g>
</symbol>"""

# Per-cocktail drink icons (smaller, same sketch style)
HIGHBALL_ICON = HIGHBALL.replace('id="highball"', 'id="icon-hb"')
ROCKS_ICON = ROCKS.replace('id="rocks"', 'id="icon-rk"')
FLUTE_ICON = FLUTE.replace('id="flute"', 'id="icon-fl"')

# ─── Decoration placements ─────────────────────────────────────────────────────
# Units: mm, matching the SVG viewBox="0 0 148 210"

def use(sym, cx, cy, w, h=None, extra=""):
    if h is None: h = w
    return f'<use href="#{sym}" x="{cx-w/2:.2f}" y="{cy-h/2:.2f}" width="{w}" height="{h}" {extra}/>'

def leaf(cx, cy, s, rot=0):
    return f'<use href="#sprig" x="{cx-s/2:.2f}" y="{cy-s:.2f}" width="{s}" height="{s}" transform="rotate({rot},{cx},{cy})"/>'

DECO_SVG = f"""<svg class="deco" viewBox="0 0 148 210" xmlns="http://www.w3.org/2000/svg" overflow="visible">
  <defs>
    {SK_FILTER}
    {ROSE.replace('<symbol','<symbol').replace('</symbol>','')}
    </symbol>
    {MUM.replace('<symbol','<symbol').replace('</symbol>','')}
    </symbol>
    {COSMOS.replace('<symbol','<symbol').replace('</symbol>','')}
    </symbol>
    {DAISY.replace('<symbol','<symbol').replace('</symbol>','')}
    </symbol>
    {TULIP}
    {BLOSSOM}
    {BLOSSOM_C}
    {BERRY}
    {SPRIG}
    {MARTINI}
    {COUPE}
    {WINE_GLASS}
    {NICK_NORA}
    {HIGHBALL}
    {ROCKS}
    {FLUTE}
    {SHAKER}
    {JIGGER}
    {STRAINER}
    {CITRUS}
    {HIGHBALL_ICON}
    {ROCKS_ICON}
    {FLUTE_ICON}
  </defs>

  <!-- ── Art Deco Frame ── -->
  <rect x="6.5" y="6.5" width="135" height="197" fill="none" stroke="#C9A24B" stroke-width="0.85"/>
  <rect x="8.2" y="8.2" width="131.6" height="193.6" fill="none" stroke="#C9A24B" stroke-width="0.35"/>

  <!-- ── Corner ornaments (stepped fan) ── -->
  <!-- TL -->
  <g stroke="#C9A24B" fill="none" stroke-width="0.5">
    <polyline points="6.5,20 6.5,14 10,14 10,10 14,10 14,6.5 20,6.5"/>
    <path d="M 6.5,17 Q 11.5,11.5 17,6.5" stroke-width="0.35" opacity="0.8"/>
    <path d="M 6.5,14 Q 10,10 14,6.5" stroke-width="0.25" opacity="0.55"/>
    <polygon points="10,14 11.2,12 12.4,14 11.2,16" fill="#C9A24B" opacity="0.9"/>
    <polygon points="14,10 15.2,8 16.4,10 15.2,12" fill="#C9A24B" opacity="0.9"/>
  </g>
  <!-- TR -->
  <g stroke="#C9A24B" fill="none" stroke-width="0.5" transform="translate(148,0) scale(-1,1)">
    <polyline points="6.5,20 6.5,14 10,14 10,10 14,10 14,6.5 20,6.5"/>
    <path d="M 6.5,17 Q 11.5,11.5 17,6.5" stroke-width="0.35" opacity="0.8"/>
    <path d="M 6.5,14 Q 10,10 14,6.5" stroke-width="0.25" opacity="0.55"/>
    <polygon points="10,14 11.2,12 12.4,14 11.2,16" fill="#C9A24B" opacity="0.9"/>
    <polygon points="14,10 15.2,8 16.4,10 15.2,12" fill="#C9A24B" opacity="0.9"/>
  </g>
  <!-- BL -->
  <g stroke="#C9A24B" fill="none" stroke-width="0.5" transform="translate(0,210) scale(1,-1)">
    <polyline points="6.5,20 6.5,14 10,14 10,10 14,10 14,6.5 20,6.5"/>
    <path d="M 6.5,17 Q 11.5,11.5 17,6.5" stroke-width="0.35" opacity="0.8"/>
    <path d="M 6.5,14 Q 10,10 14,6.5" stroke-width="0.25" opacity="0.55"/>
    <polygon points="10,14 11.2,12 12.4,14 11.2,16" fill="#C9A24B" opacity="0.9"/>
    <polygon points="14,10 15.2,8 16.4,10 15.2,12" fill="#C9A24B" opacity="0.9"/>
  </g>
  <!-- BR -->
  <g stroke="#C9A24B" fill="none" stroke-width="0.5" transform="translate(148,210) scale(-1,-1)">
    <polyline points="6.5,20 6.5,14 10,14 10,10 14,10 14,6.5 20,6.5"/>
    <path d="M 6.5,17 Q 11.5,11.5 17,6.5" stroke-width="0.35" opacity="0.8"/>
    <path d="M 6.5,14 Q 10,10 14,6.5" stroke-width="0.25" opacity="0.55"/>
    <polygon points="10,14 11.2,12 12.4,14 11.2,16" fill="#C9A24B" opacity="0.9"/>
    <polygon points="14,10 15.2,8 16.4,10 15.2,12" fill="#C9A24B" opacity="0.9"/>
  </g>

  <!-- ══════════ TOP-LEFT CORNER CLUSTER ══════════ -->
  <!-- large rose -->
  {use('rose', 17, 19, 34)}
  <!-- chrysanthemum upper right of rose -->
  {use('mum', 31, 10, 24)}
  <!-- small blossoms -->
  {use('blossom', 8, 10, 14)}
  {use('blossom-c', 30, 28, 12)}
  {use('blossom', 38, 18, 10)}
  <!-- leaf sprigs -->
  {leaf(9, 28, 20, 15)}
  {leaf(24, 8, 18, -20)}
  <!-- berry cluster -->
  {use('berry', 36, 30, 14)}
  <!-- SKETCH: martini glass (tilted slightly) -->
  <g transform="translate(11,14) rotate(-12) scale(0.55)">
    <use href="#martini" x="-17" y="-40" width="34" height="44"/>
  </g>
  <!-- SKETCH: jigger -->
  <g transform="translate(31,24) rotate(8) scale(0.5)">
    <use href="#jigger" x="-10" y="-28" width="20" height="30"/>
  </g>

  <!-- ══════════ TOP-RIGHT CORNER CLUSTER ══════════ -->
  <!-- daisy -->
  {use('daisy', 131, 19, 32)}
  <!-- cosmos -->
  {use('cosmos', 118, 10, 26)}
  <!-- small blossoms -->
  {use('blossom-c', 140, 10, 14)}
  {use('blossom', 118, 30, 12)}
  {use('blossom-c', 108, 20, 10)}
  <!-- leaf sprigs -->
  {leaf(139, 28, 20, -15)}
  {leaf(124, 8, 18, 20)}
  <!-- berry cluster -->
  {use('berry', 110, 30, 14)}
  <!-- SKETCH: coupe glass -->
  <g transform="translate(137,14) rotate(10) scale(0.52)">
    <use href="#coupe" x="-17" y="-36" width="34" height="40"/>
  </g>
  <!-- SKETCH: citrus wheel -->
  <g transform="translate(119,26) rotate(-5) scale(0.7)">
    <use href="#citrus" x="-10" y="-10" width="20" height="20"/>
  </g>

  <!-- ══════════ BOTTOM-LEFT CORNER CLUSTER ══════════ -->
  <!-- tulip -->
  {use('tulip', 12, 193, 22, 34)}
  <!-- chrysanthemum -->
  {use('mum', 28, 185, 26)}
  <!-- berry clusters -->
  {use('berry', 10, 181, 14)}
  {use('berry', 36, 200, 12)}
  <!-- small blossoms -->
  {use('blossom', 36, 192, 12)}
  {use('blossom-c', 22, 204, 10)}
  <!-- leaf sprigs -->
  {leaf(8, 202, 18, -10)}
  {leaf(25, 178, 18, 20)}
  <!-- SKETCH: wine glass -->
  <g transform="translate(18,184) rotate(-8) scale(0.52)">
    <use href="#wine-glass" x="-12" y="-44" width="24" height="48"/>
  </g>
  <!-- SKETCH: strainer -->
  <g transform="translate(32,196) rotate(15) scale(0.55)">
    <use href="#strainer" x="-22" y="-12" width="44" height="14"/>
  </g>

  <!-- ══════════ BOTTOM-RIGHT CORNER CLUSTER ══════════ -->
  <!-- rose (peony style - larger) -->
  {use('rose', 131, 191, 36)}
  <!-- daisy -->
  {use('daisy', 118, 182, 28)}
  <!-- small blossoms -->
  {use('blossom-c', 140, 200, 14)}
  {use('blossom', 110, 194, 12)}
  {use('blossom-c', 142, 182, 10)}
  <!-- leaf sprigs -->
  {leaf(140, 178, 20, 15)}
  {leaf(114, 202, 18, -20)}
  <!-- berry cluster -->
  {use('berry', 108, 181, 14)}
  <!-- SKETCH: shaker -->
  <g transform="translate(121,184) rotate(6) scale(0.5)">
    <use href="#shaker" x="-12" y="-44" width="24" height="48"/>
  </g>
  <!-- SKETCH: nick-nora glass -->
  <g transform="translate(138,196) rotate(-10) scale(0.52)">
    <use href="#nick-nora" x="-14" y="-40" width="28" height="44"/>
  </g>

  <!-- ══════════ LEFT GARLAND ══════════ -->
  <!-- y: 38 to 172, x: 6-18mm -->
  {leaf(11, 46, 16, 8)}
  {use('blossom-c', 14, 58, 10)}
  {leaf(9, 68, 16, -5)}
  {use('blossom', 13, 80, 10)}
  {use('berry', 10, 92, 12)}
  {leaf(12, 102, 16, 10)}
  {use('blossom-c', 11, 114, 10)}
  {leaf(10, 124, 16, -8)}
  {use('blossom', 14, 136, 10)}
  {leaf(9, 148, 16, 5)}
  {use('blossom-c', 12, 160, 10)}
  {leaf(11, 170, 16, -10)}

  <!-- ══════════ RIGHT GARLAND ══════════ -->
  <!-- y: 38 to 172, x: 130-142mm -->
  {leaf(137, 44, 16, -8)}
  {use('blossom', 134, 56, 10)}
  {leaf(139, 66, 16, 6)}
  {use('blossom-c', 135, 78, 10)}
  {leaf(138, 90, 16, -6)}
  {use('berry', 137, 102, 12)}
  {leaf(136, 112, 16, 9)}
  {use('blossom', 139, 124, 10)}
  {leaf(137, 134, 16, -5)}
  {use('blossom-c', 134, 146, 10)}
  {leaf(138, 158, 16, 7)}
  {use('blossom', 136, 170, 10)}
</svg>"""

# ─── Fix the defs block (symbols with nested defs) ────────────────────────────
# Build a clean defs section instead
DEFS = f"""<defs>
  {SK_FILTER}
  {ROSE}
  {MUM}
  {COSMOS}
  {DAISY}
  {TULIP}
  {BLOSSOM}
  {BLOSSOM_C}
  {BERRY}
  {SPRIG}
  {MARTINI}
  {COUPE}
  {WINE_GLASS}
  {NICK_NORA}
  {HIGHBALL}
  {ROCKS}
  {FLUTE}
  {SHAKER}
  {JIGGER}
  {STRAINER}
  {CITRUS}
  {HIGHBALL_ICON}
  {ROCKS_ICON}
  {FLUTE_ICON}
</defs>"""

DECO_CLEAN = f"""<svg class="deco" viewBox="0 0 148 210" xmlns="http://www.w3.org/2000/svg">
  {DEFS}

  <!-- ── Art Deco Frame ── -->
  <rect x="6.5" y="6.5" width="135" height="197" fill="none" stroke="#C9A24B" stroke-width="0.85"/>
  <rect x="8.2" y="8.2" width="131.6" height="193.6" fill="none" stroke="#C9A24B" stroke-width="0.35"/>

  <!-- Corner ornaments -->
  <g stroke="#C9A24B" fill="none">
    <!-- TL -->
    <polyline points="6.5,20 6.5,14 10,14 10,10 14,10 14,6.5 20,6.5" stroke-width="0.5"/>
    <path d="M 6.5,17 Q 11.5,11.5 17,6.5" stroke-width="0.35" opacity="0.8"/>
    <path d="M 6.5,14 Q 10,10 14,6.5" stroke-width="0.25" opacity="0.55"/>
    <polygon points="10,14 11.2,12 12.4,14 11.2,16" fill="#C9A24B" opacity="0.9"/>
    <polygon points="14,10 15.2,8 16.4,10 15.2,12" fill="#C9A24B" opacity="0.9"/>
    <!-- TR (reflected) -->
    <polyline points="141.5,20 141.5,14 138,14 138,10 134,10 134,6.5 128,6.5" stroke-width="0.5"/>
    <path d="M 141.5,17 Q 136.5,11.5 131,6.5" stroke-width="0.35" opacity="0.8"/>
    <polygon points="138,14 136.8,12 135.6,14 136.8,16" fill="#C9A24B" opacity="0.9"/>
    <polygon points="134,10 132.8,8 131.6,10 132.8,12" fill="#C9A24B" opacity="0.9"/>
    <!-- BL (reflected) -->
    <polyline points="6.5,190 6.5,196 10,196 10,200 14,200 14,203.5 20,203.5" stroke-width="0.5"/>
    <path d="M 6.5,193 Q 11.5,198.5 17,203.5" stroke-width="0.35" opacity="0.8"/>
    <polygon points="10,196 11.2,198 12.4,196 11.2,194" fill="#C9A24B" opacity="0.9"/>
    <polygon points="14,200 15.2,202 16.4,200 15.2,198" fill="#C9A24B" opacity="0.9"/>
    <!-- BR -->
    <polyline points="141.5,190 141.5,196 138,196 138,200 134,200 134,203.5 128,203.5" stroke-width="0.5"/>
    <path d="M 141.5,193 Q 136.5,198.5 131,203.5" stroke-width="0.35" opacity="0.8"/>
    <polygon points="138,196 136.8,198 135.6,196 136.8,194" fill="#C9A24B" opacity="0.9"/>
    <polygon points="134,200 132.8,202 131.6,200 132.8,198" fill="#C9A24B" opacity="0.9"/>
  </g>

  <!-- ══ TOP-LEFT corner cluster ══ -->
  {use('rose', 16, 20, 34)}
  {use('mum', 30, 11, 24)}
  {use('blossom', 8, 10, 14)}
  {use('blossom-c', 30, 30, 12)}
  {use('blossom', 37, 18, 10)}
  {leaf(9, 28, 22, 15)}
  {leaf(24, 7, 18, -20)}
  {use('berry', 36, 30, 14)}
  <g transform="translate(11,13) rotate(-12) scale(0.55)">
    <use href="#martini" x="-17" y="-40" width="34" height="44"/>
  </g>
  <g transform="translate(32,25) rotate(8) scale(0.5)">
    <use href="#jigger" x="-10" y="-28" width="20" height="30"/>
  </g>

  <!-- ══ TOP-RIGHT corner cluster ══ -->
  {use('daisy', 132, 20, 32)}
  {use('cosmos', 119, 10, 26)}
  {use('blossom-c', 140, 10, 14)}
  {use('blossom', 119, 30, 12)}
  {use('blossom-c', 109, 20, 10)}
  {leaf(139, 28, 22, -15)}
  {leaf(125, 7, 18, 20)}
  {use('berry', 110, 30, 14)}
  <g transform="translate(137,13) rotate(10) scale(0.52)">
    <use href="#coupe" x="-17" y="-36" width="34" height="40"/>
  </g>
  <g transform="translate(120,26) rotate(-5) scale(0.7)">
    <use href="#citrus" x="-10" y="-10" width="20" height="20"/>
  </g>

  <!-- ══ BOTTOM-LEFT corner cluster ══ -->
  {use('tulip', 12, 193, 22, 34)}
  {use('mum', 28, 185, 26)}
  {use('berry', 10, 181, 14)}
  {use('berry', 36, 200, 12)}
  {use('blossom', 37, 192, 12)}
  {use('blossom-c', 22, 205, 10)}
  {leaf(8, 202, 18, -10)}
  {leaf(26, 178, 18, 20)}
  <g transform="translate(18,184) rotate(-8) scale(0.52)">
    <use href="#wine-glass" x="-12" y="-44" width="24" height="48"/>
  </g>
  <g transform="translate(33,197) rotate(15) scale(0.55)">
    <use href="#strainer" x="-22" y="-12" width="44" height="14"/>
  </g>

  <!-- ══ BOTTOM-RIGHT corner cluster ══ -->
  {use('rose', 131, 191, 36)}
  {use('daisy', 118, 182, 28)}
  {use('blossom-c', 140, 200, 14)}
  {use('blossom', 110, 194, 12)}
  {use('blossom-c', 142, 182, 10)}
  {leaf(140, 178, 20, 15)}
  {leaf(115, 203, 18, -20)}
  {use('berry', 108, 181, 14)}
  <g transform="translate(121,184) rotate(6) scale(0.5)">
    <use href="#shaker" x="-12" y="-44" width="24" height="48"/>
  </g>
  <g transform="translate(138,197) rotate(-10) scale(0.52)">
    <use href="#nick-nora" x="-14" y="-40" width="28" height="44"/>
  </g>

  <!-- ══ LEFT garland ══ -->
  {leaf(11, 46, 16, 8)}   {use('blossom-c', 13, 58, 10)}
  {leaf(9,  68, 16,-5)}   {use('blossom',   13, 80, 10)}
  {use('berry', 10, 92, 12)}
  {leaf(12, 102, 16, 10)} {use('blossom-c', 11, 114, 10)}
  {leaf(10, 124, 16,-8)}  {use('blossom',   14, 136, 10)}
  {leaf(9,  148, 16,  5)} {use('blossom-c', 12, 160, 10)}
  {leaf(11, 170, 16,-10)}

  <!-- ══ RIGHT garland ══ -->
  {leaf(137, 44, 16,-8)}  {use('blossom',   134,  56, 10)}
  {leaf(139, 66, 16, 6)}  {use('blossom-c', 135,  78, 10)}
  {leaf(138, 90, 16,-6)}
  {use('berry', 137, 102, 12)}
  {leaf(136,112, 16, 9)}  {use('blossom',   139, 124, 10)}
  {leaf(137,134, 16,-5)}  {use('blossom-c', 134, 146, 10)}
  {leaf(138,158, 16, 7)}  {use('blossom',   136, 170, 10)}
</svg>"""

# ─── Per-cocktail icon SVGs ────────────────────────────────────────────────────
def drink_icon(sym, vx, vy, vw, vh, disp_w=11, disp_h=14):
    return (f'<svg width="{disp_w}mm" height="{disp_h}mm" '
            f'viewBox="{vx} {vy} {vw} {vh}" '
            f'xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto 2mm;">'
            f'<use href="#icon-{sym}" x="{vx}" y="{vy}" width="{vw}" height="{vh}"/>'
            f'</svg>')

icon_hb = drink_icon('hb', -10, -42, 32, 46, 9, 13)
icon_rk = drink_icon('rk', -12, -28, 24, 32, 9, 11)
icon_fl = drink_icon('fl', -8, -48, 16, 52, 7, 14)

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

html, body {{
  width: 148mm; height: 210mm;
  overflow: hidden;
}}

.page {{
  position: relative;
  width: 148mm; height: 210mm;
  background: radial-gradient(ellipse 80% 90% at 50% 38%,
    #1E4A39 0%, #1A4233 28%, #123026 58%, #0B1E17 100%);
}}

.deco {{
  position: absolute;
  top: 0; left: 0;
  width: 148mm; height: 210mm;
  pointer-events: none;
}}

.content {{
  position: absolute;
  top: 0; left: 0;
  width: 148mm; height: 210mm;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 19mm 17mm 15mm;
}}

/* ── Masthead ── */
.venue-name {{
  font-family: 'Poppins', sans-serif;
  font-weight: 300;
  font-size: 5.5px;
  letter-spacing: 0.30em;
  color: #C0B080;
  text-transform: uppercase;
  margin-bottom: 3mm;
  text-align: center;
}}
.cocktails-title {{
  font-family: 'Lora', serif;
  font-weight: 700;
  font-size: 27px;
  color: #D9B259;
  text-align: center;
  line-height: 1.05;
  margin-bottom: 3.5mm;
  letter-spacing: 0.04em;
}}
.sig-row {{
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: 5mm;
}}
.sig-line {{ flex: 1; height: 0.4px; background: #C9A24B; }}
.sig-text {{
  font-family: 'Poppins', sans-serif;
  font-weight: 300;
  font-size: 5px;
  letter-spacing: 0.28em;
  color: #C9A24B;
  padding: 0 5px;
  white-space: nowrap;
}}

/* ── Cocktail cards ── */
.cocktails {{
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  width: 100%;
}}
.cocktail {{
  text-align: center;
  width: 100%;
}}
.drink-name {{
  font-family: 'Lora', serif;
  font-weight: 700;
  font-size: 16.5px;
  color: #D4AB52;
  margin-bottom: 2.2mm;
  letter-spacing: 0.025em;
}}
.tasting-note {{
  font-family: 'Lora', serif;
  font-weight: 400;
  font-style: italic;
  font-size: 9.5px;
  color: #ECE2C4;
  line-height: 1.45;
  margin-bottom: 2.5mm;
  padding: 0 2mm;
}}
.ingredients {{
  font-family: 'Poppins', sans-serif;
  font-weight: 300;
  font-size: 6px;
  letter-spacing: 0.18em;
  color: #8FB199;
  text-transform: uppercase;
  line-height: 1.6;
}}
.diamond {{ color: #C9A24B; }}

/* ── Art Deco divider between cocktails ── */
.divider {{
  display: flex;
  align-items: center;
  width: 88%;
  gap: 0;
}}
.div-line {{ flex: 1; height: 0.4px; background: #C9A24B; opacity: 0.8; }}
.div-diamonds {{
  display: flex;
  gap: 5px;
  padding: 0 6px;
  font-size: 6px;
  color: #C9A24B;
  line-height: 1;
}}

/* ── Footer ── */
.footer {{
  text-align: center;
  margin-top: 3mm;
}}
.footer-rule {{
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 2mm;
}}
.footer-line {{ flex: 1; height: 0.4px; background: #C9A24B; opacity: 0.7; }}
.footer-diamond {{ font-size: 5px; color: #C9A24B; padding: 0 5px; }}
.footer-text {{
  font-family: 'Poppins', sans-serif;
  font-weight: 300;
  font-size: 5.5px;
  letter-spacing: 0.30em;
  color: #C0B890;
  text-transform: uppercase;
}}
</style>
</head>
<body>
<div class="page">

  <!-- Decoration layer -->
  {DECO_CLEAN}

  <!-- Content layer -->
  <div class="content">

    <!-- Masthead -->
    <div class="venue-name">Your Venue Name</div>
    <h1 class="cocktails-title">Cocktails</h1>
    <div class="sig-row">
      <div class="sig-line"></div>
      <span class="sig-text">Signature Selection</span>
      <div class="sig-line"></div>
    </div>

    <!-- Three cocktails -->
    <div class="cocktails">

      <!-- Hibiscus Veil -->
      <div class="cocktail">
        {icon_hb}
        <h2 class="drink-name">Hibiscus Veil</h2>
        <p class="tasting-note">A blush-pink long drink — floral and bittersweet,<br>veiled in cool botanical effervescence.</p>
        <p class="ingredients">
          Vodka <span class="diamond">◆</span> Rosato Aperitivo <span class="diamond">◆</span>
          Fresh Lime <span class="diamond">◆</span> Thomas Henry Botanical Tonic
        </p>
      </div>

      <!-- Divider -->
      <div class="divider">
        <div class="div-line"></div>
        <div class="div-diamonds"><span>◆</span><span>◆</span><span>◆</span></div>
        <div class="div-line"></div>
      </div>

      <!-- Golden Sour -->
      <div class="cocktail">
        {icon_rk}
        <h2 class="drink-name">Golden Sour</h2>
        <p class="tasting-note">Silken and amber-warm, where ripe pear softens<br>the whiskey's edge over a whisper of spice.</p>
        <p class="ingredients">
          Whiskey <span class="diamond">◆</span> Pear Syrup <span class="diamond">◆</span>
          Fresh Lemon <span class="diamond">◆</span> Angostura Bitters
        </p>
      </div>

      <!-- Divider -->
      <div class="divider">
        <div class="div-line"></div>
        <div class="div-diamonds"><span>◆</span><span>◆</span><span>◆</span></div>
        <div class="div-line"></div>
      </div>

      <!-- Elderbloom Spritz -->
      <div class="cocktail">
        {icon_fl}
        <h2 class="drink-name">Elderbloom Spritz</h2>
        <p class="tasting-note">Effervescent and garden-fresh — elderflower and mint<br>lifted by chilled Prosecco and a ribbon of cucumber.</p>
        <p class="ingredients">
          Prosecco <span class="diamond">◆</span> Elderflower <span class="diamond">◆</span>
          Fresh Mint <span class="diamond">◆</span> Cucumber <span class="diamond">◆</span> Lime
        </p>
      </div>

    </div><!-- /.cocktails -->

    <!-- Footer -->
    <div class="footer">
      <div class="footer-rule">
        <div class="footer-line"></div>
        <span class="footer-diamond">◆</span>
        <div class="footer-line"></div>
      </div>
      <p class="footer-text">Crafted to Order</p>
    </div>

  </div><!-- /.content -->
</div><!-- /.page -->
</body>
</html>"""

out_path = '/home/user/Tadow/cocktail-menu.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(HTML)

size_kb = os.path.getsize(out_path) / 1024
print(f"Written: {out_path}  ({size_kb:.0f} KB)")
