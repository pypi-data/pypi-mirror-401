from PIL import Image as PILImage
from typing import TextIO
from pathlib import Path
import os

class Image:
    """
    Repräsentiert ein HTML-<img>-Element.

    Unterstützt optional echte Bilddaten (PIL) und HTML-Attribute.
    """

    def __init__(
        self,
        src: str | Path | None = None,
        *,
        attrs: dict | None = None,
        pil_image: PILImage.Image | None = None,
        alt: str | None = None
    ):
        """
        Initialisiert ein Image-Objekt.

        Parameter:
            src (str | Path | None):
                Pfad zur Bilddatei (wird als 'src'-Attribut gesetzt).

            attrs (dict | None):
                Optionales Dictionary für HTML-Attribute wie class, id, style.
                'src' und 'alt' werden bei Bedarf überschrieben.

            pil_image (PIL.Image.Image | None):
                Optionales PIL-Bildobjekt.

            alt (str | None):
                Alternativtext für das Bild.
        """
        # attrs immer als Dict initialisieren
        self.attrs = attrs.copy() if attrs else {}

        # src setzen
        if src is not None:
            self.attrs["src"] = str(src)
        else:
            self.attrs.setdefault("src", "")

        # alt setzen
        if alt is not None:
            self.attrs["alt"] = alt
        else:
            self.attrs.setdefault("alt", "")

        self.pil_image = pil_image
        
    @property
    def src(self) -> str:
        return self.attrs.get("src", "")

    @src.setter
    def src(self, value: str):
        self.attrs["src"] = value

    @property
    def alt(self) -> str | None:
        return self.attrs.get("alt")

    def save(self, path: str, format: str | None = None):
        """
        Speichert das Bild in einer Datei.

        Parameters:
            path (str): Pfad, unter dem das Bild gespeichert werden soll.
            format (str | None): Optionales Format (z. B. "PNG", "JPEG").

        Raises:
            ValueError: Wenn kein PIL-Image vorhanden ist.
        """
        if self.pil_image is None:
            raise ValueError("Kein PIL-Image vorhanden zum Speichern.")

        self.pil_image.save(path, format=format)
        self.src = os.path.basename(path)  # src automatisch setzen

    def to_html(self) -> str:
        """
        Gibt das HTML <img>-Tag zurück.

        Raises:
            ValueError: Wenn src leer ist.

        Returns:
            str: HTML-String.
        """
        if not self.src:
            raise ValueError("src muss gesetzt sein, bevor das HTML erzeugt wird.")
        attr_string = " ".join(f'{k}="{v}"' for k, v in self.attrs.items())
        return f"<img {attr_string}>"

    def write_to(self, target: TextIO) -> None:
        """
        Schreibt das HTML-Tag in ein schreibbares Objekt.

        Parameters:
            target (TextIO): Schreibbares Objekt.
        """
        if not hasattr(target, "write"):
            raise TypeError("write_to() erwartet ein schreibbares TextIO-Objekt")
        target.write(self.to_html())

    def __str__(self) -> str:
        return self.to_html()

    def __repr__(self) -> str:
        pil_info = f" size={self.pil_image.size}" if self.pil_image else ""
        return f"<Image src='{self.src}'{pil_info} attrs={self.attrs}>"
