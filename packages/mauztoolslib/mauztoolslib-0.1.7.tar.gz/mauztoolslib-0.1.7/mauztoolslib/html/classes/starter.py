from __future__ import annotations
from pathlib import Path
import webbrowser
from typing import Union
from .writer import HTMLWriter
from .document import HTMLDocument

class HTMLStarter:
    """
    HTMLStarter initialisiert ein HTML-Dokument und startet es im Browser.

    Funktionen:
    - write(): Dokument in Datei schreiben
    - run(): Dokument im Browser öffnen
    - run_as_port(port=8000): Startet HTTP-Server als Context Manager
    """

    def __init__(self, document: HTMLDocument, *, file: Union[str, Path] = "index.html"):
        self.document = document
        self.file = Path(file)
        self._server = None
        self._thread = None

    # ==========================================================
    # Schreiben
    # ==========================================================
    def write(self) -> None:
        writer = HTMLWriter(self.document, file=self.file)
        with writer:
            pass  # schreibt automatisch beim Verlassen des Context Managers

    # ==========================================================
    # Browser starten
    # ==========================================================
    def run(self) -> None:
        if not self.file.exists():
            raise FileNotFoundError(f"Datei {self.file} existiert nicht. Bitte write() vorher aufrufen.")
        webbrowser.open(self.file.resolve().as_uri())