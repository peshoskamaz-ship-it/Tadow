#!/usr/bin/env python3
"""
Render cocktail-menu.html → output/cocktail-menu.pdf
using headless Chromium via Playwright (Node.js).
"""
import os, subprocess, sys

ROOT     = os.path.dirname(os.path.abspath(__file__))
HTML     = os.path.join(ROOT, 'cocktail-menu.html')
SCRIPT   = os.path.join(ROOT, 'render.js')
OUT_PDF  = os.path.join(ROOT, 'output', 'cocktail-menu.pdf')
NODE     = '/opt/node22/bin/node'

if not os.path.exists(HTML):
    sys.exit(f'ERROR: {HTML} not found. Run generate_menu.py first.')

result = subprocess.run([NODE, SCRIPT], capture_output=False, text=True)
if result.returncode != 0:
    sys.exit(f'Render failed (exit {result.returncode})')

size_kb = os.path.getsize(OUT_PDF) / 1024
print(f'\nPDF ready: {OUT_PDF}  ({size_kb:.0f} KB)')
