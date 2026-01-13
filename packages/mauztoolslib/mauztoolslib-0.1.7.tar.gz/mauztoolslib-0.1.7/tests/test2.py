from pathlib import Path
import sys

# MauzLib zum Import bereitstellen
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mauztoolslib.html import HTMLDocument, Heading, Paragraph, Image, Link, HTMLWriter

# ==========================================================
# 1️⃣ HTMLDocument erstellen und Elemente hinzufügen
# ==========================================================
doc = HTMLDocument()

doc += Heading("Willkommen auf Mauz!", level=1)
doc += Paragraph(
    "Dies ist ein Beispieltext für Mauz. "
    "Wir demonstrieren HTMLDocument und HTMLWriter."
)
doc += Image("logo.png", alt="Mauz Logo")
doc += Link("https://mauz.com", "Zur Mauz Website")

# Optional: weitere Elemente
doc += Heading("Abschnitt 2", level=2)
doc += Paragraph("Noch ein kleiner Textabschnitt.")

# ==========================================================
# 2️⃣ HTMLWriter anwenden und HTML-Datei erstellen
# ==========================================================
file_path = Path("output.html")

# Optimiert: direkt document in Writer und dann einmal serialisieren
with HTMLWriter(doc, file=file_path, auto_doctype=True) as writer:
    # Keine Schleife über jedes Element nötig – Writer schreibt alles beim __exit__
    # Optional: kannst du Elemente noch hinzufügen, z.B. neue Paragraphen
    writer.add(Paragraph("Zusätzlicher Absatz am Ende des Dokuments."))

print(f"HTML-Datei erstellt: {file_path}")
