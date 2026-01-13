from __future__ import annotations
from pathlib import Path
from typing import Union, Iterable, TextIO
from .document import HTMLDocument


class HTMLWriter:
    """
    HTMLWriter ist für Ausgabe, Zugriff und Manipulation eines HTMLDocument
    zuständig.

    Verantwortlichkeiten:
    - Schreiben von HTML in Dateien oder TextIO
    - getitem / setitem / remove
    - Context-Manager-Unterstützung
    - KEINE eigene HTML-Struktur
    """

    def __init__(
        self,
        document: HTMLDocument,
        *,
        encoding: str = "utf-8",
        auto_doctype: bool = True,
        file: str | Path | None = None,
    ):
        """
        Initialisiert den HTMLWriter.

        Parameter:
            document (HTMLDocument):
                Das zu schreibende HTML-Dokument.

            encoding (str):
                Textkodierung für Ausgabedateien.

            auto_doctype (bool):
                Fügt <!DOCTYPE html> beim Schreiben hinzu,
                falls das Dokument keines enthält.

            file (str | Path | None):
                Optionaler Zielpfad für automatische Ausgabe
                beim Verlassen des Context Managers.
        """
        self.document = document
        self.encoding = encoding
        self.auto_doctype = auto_doctype
        self._file = Path(file) if file else None

    # ==========================================================
    # Context Manager
    # ==========================================================

    def __enter__(self) -> HTMLWriter:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc_type is None and self._file:
            self.write_to(self._file)

    # ==========================================================
    # Zugriff / Manipulation
    # ==========================================================

    def __getitem__(self, tag: str):
        """
        Gibt alle Elemente mit dem gegebenen Tag zurück.
        """
        return self.document[tag]

    def __setitem__(self, tag: str, elements: Iterable[object]):
        """
        Ersetzt alle Elemente eines Tags.
        """
        self.document.remove_tag(tag)
        for el in elements:
            self.document.add(el)

    def remove(self, element: object) -> None:
        """
        Entfernt ein Element aus dem Dokument.
        """
        self.document.remove(element)
        
    def add(self, element: object) -> None:
        """
        Fügt ein HTML-Objekt in das Dokument ein.
        """
        if not hasattr(element, "to_html"):
            raise TypeError(f"{element.__class__.__name__} besitzt keine to_html()-Methode")
        self.document.add(element)  # <-- kein self._elements mehr

    def extend(self, elements: Iterable[object]) -> None:
        """
        Fügt mehrere HTML-Objekte in das Dokument ein.
        """
        for el in elements:
            self.add(el)

    # ==========================================================
    # Ausgabe
    # ==========================================================

    def to_html(self, pretty: bool = False) -> str:
        """
        Serialisiert das HTMLDocument zu HTML.
        """
        html = self.document.to_html(pretty=pretty)

        if self.auto_doctype and not html.lstrip().lower().startswith("<!doctype"):
            html = "<!DOCTYPE html>\n" + html

        return html

    def write_to(self, target: Union[str, Path, TextIO]) -> None:
        """
        Schreibt HTML in Datei oder TextIO.
        """
        html = self.to_html(pretty=True)

        if hasattr(target, "write"):
            target.write(html)
            return

        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding=self.encoding) as f:
            f.write(html)

    # ==========================================================
    # Python-Integration
    # ==========================================================

    def __str__(self) -> str:
        return self.to_html(pretty=True)

    def __repr__(self) -> str:
        return (
            f"<HTMLWriter document={self.document.__class__.__name__}, "
            f"auto_doctype={self.auto_doctype}>"
        )
