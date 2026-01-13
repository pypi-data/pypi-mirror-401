# test_html_starter.py
from pathlib import Path
import sys
from PIL import Image as PILImage

# Lokales Projekt importieren
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mauztoolslib.html import HTMLDocument, Heading, Paragraph, Image, Link, HTMLStarter

image = PILImage.new("RGB", (1000, 1000), "red")

# ==========================================================
# 1️⃣ HTML-Dokument erstellen
# ==========================================================
doc = HTMLDocument()
doc += Heading("Willkommen auf Mauz!", level=1)
doc += Paragraph("Dies ist ein Test für HTMLDocument und HTMLStarter.")
doc += Image("logo.png", alt="Mauz Logo", pil_image=image)
doc[2].save("test.png", "PNG")
doc += Link("https://mauz.com", "Zur Mauz Website")

# ==========================================================
# 2️⃣ HTMLStarter initialisieren
# ==========================================================
starter = HTMLStarter(doc, file=Path("output.html"))

# ==========================================================
# 3️⃣ HTML-Datei schreiben
# ==========================================================
starter.write()
print(f"HTML-Datei erstellt: {starter.file}")

starter.run()