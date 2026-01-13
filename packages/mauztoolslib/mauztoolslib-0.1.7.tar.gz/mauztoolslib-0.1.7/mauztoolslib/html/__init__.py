from .classes.reader import HTMLReader
from .classes.writer import HTMLWriter
from .classes.document import HTMLDocument
from .classes.starter import HTMLStarter
from .objects.script import Script
from .objects.paragraph import Paragraph
from .objects.image import Image
from .objects.heading import Heading
from .objects.link import Link
from .functions.from_tag_to_class import from_tag_to_class
from .functions.find_all import find_all

__all__ = [
    "HTMLReader",
    "HTMLWriter",
    "HTMLDocument",
    "HTMLStarter",
    "Script",
    "Paragraph",
    "Image",
    "Heading",
    "Link",
    "from_tag_to_class",
    "find_all",
]