from ..objects.script import Script
from ..objects.paragraph import Paragraph
from ..objects.image import Image
from ..objects.heading import Heading
from ..objects.link import Link
from typing import Type, Union

def from_tag_to_class(tag: str) -> Type[Union[Script, Paragraph, Image, Heading, Link, str]]:
    """
    Gibt die passende Klasse für einen HTML-Tag aus der Objects-Library zurück.

    Parameter:
        tag (str): HTML-Tag, z. B. "p", "img", "h1", "script", "a".

    Returns:
        Type: Entsprechende Klasse aus `objects`:
              - "script" -> Script
              - "p"      -> Paragraph
              - "img"    -> Image
              - "h1"-"h6"-> Heading
              - "a"      -> Link
              - alles andere -> str

    Beispiel:
        >>> from_tag_to_class("p")
        <class 'mauztoolslib.objects.paragraph.Paragraph'>
        >>> from_tag_to_class("h2")
        <class 'mauztoolslib.objects.heading.Heading'>
        >>> from_tag_to_class("div")
        <class 'str'>
    """
    tag_lower = tag.lower()

    if tag_lower == "script":
        return Script
    elif tag_lower == "p":
        return Paragraph
    elif tag_lower == "img":
        return Image
    elif tag_lower in ["h1","h2","h3","h4","h5","h6"]:
        return Heading
    elif tag_lower == "a":
        return Link
    else:
        return str
