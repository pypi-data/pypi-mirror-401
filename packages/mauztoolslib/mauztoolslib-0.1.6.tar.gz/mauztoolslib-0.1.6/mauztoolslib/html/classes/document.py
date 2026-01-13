from __future__ import annotations
from typing import Iterable, Union


class HTMLDocument:
    """
    HTMLDocument speichert die HTML-Struktur eines Dokuments.

    Verantwortlichkeiten:
    - Verwaltung aller HTML-Objekte (Paragraph, Script, Image, Heading, Link, ...)
    - Entfernen von Elementen
    - Serialisierung zu HTML
    - Zugriff wie bei einer Liste (getitem, setitem)
    - Hinzufügen von Elementen mit +=
    """

    def __init__(self):
        self.elements: list[object] = []

    # ==========================================================
    # Elemente verwalten
    # ==========================================================

    def add(self, element: object) -> None:
        """Fügt ein HTML-Objekt hinzu. Muss eine to_html()-Methode besitzen."""
        if not hasattr(element, "to_html"):
            raise TypeError(f"{element.__class__.__name__} besitzt keine to_html()-Methode")
        self.elements.append(element)

    def extend(self, elements: Iterable[object]) -> None:
        """Fügt mehrere HTML-Objekte hinzu."""
        for el in elements:
            self.add(el)

    def remove(self, element: object) -> None:
        """Entfernt ein Element aus dem Dokument."""
        self.elements.remove(element)

    def clear(self) -> None:
        """Entfernt alle Elemente."""
        self.elements.clear()

    # ==========================================================
    # Zugriff (getitem / setitem)
    # ==========================================================

    def __getitem__(self, index: Union[int, slice]):
        """Gibt ein oder mehrere HTML-Objekte zurück."""
        return self.elements[index]

    def __setitem__(self, index: Union[int, slice], value: Union[object, Iterable[object]]):
        """Ersetzt ein oder mehrere HTML-Objekte."""
        if isinstance(index, slice):
            for el in value:
                if not hasattr(el, "to_html"):
                    raise TypeError(f"{el.__class__.__name__} besitzt keine to_html()-Methode")
            self.elements[index] = list(value)
        else:
            if not hasattr(value, "to_html"):
                raise TypeError(f"{value.__class__.__name__} besitzt keine to_html()-Methode")
            self.elements[index] = value

    def __iadd__(self, element: object):
        """
        Ermöglicht: doc += Paragraph("Text")
        """
        self.add(element)
        return self

    # ==========================================================
    # Serialisierung
    # ==========================================================

    def to_html(self, pretty: bool = False) -> str:
        """Serialisiert das Dokument zu HTML."""
        sep = "\n" if pretty else ""
        return sep.join(el.to_html() for el in self.elements)

    # ==========================================================
    # Python-Integration
    # ==========================================================

    def __len__(self) -> int:
        return len(self.elements)

    def __iter__(self):
        return iter(self.elements)

    def __repr__(self) -> str:
        return f"<HTMLDocument elements={len(self.elements)}>"
