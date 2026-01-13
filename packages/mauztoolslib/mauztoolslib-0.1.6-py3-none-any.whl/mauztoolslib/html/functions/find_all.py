import re
from typing import List, Tuple

def find_all(html: str) -> List[Tuple[str, str, dict]]:
    """
    Findet alle HTML-Tags im String und gibt sie als Liste zurück.

    Parameter:
        html (str): HTML-Inhalt als String.

    Returns:
        List[Tuple[str, str, dict]]: Liste von Tupeln mit
            (tag_name, inner_html, attributes)
            - tag_name: Name des Tags, z. B. "p", "img", "a"
            - inner_html: Inhalt zwischen den Tags (leer bei selbstschließenden Tags)
            - attributes: Dict mit allen Attributen des Tags

    Beispiel:
        >>> html = '<p class="text">Hallo</p><img src="bild.png"/>'
        >>> find_all(html)
        [('p', 'Hallo', {'class': 'text'}), ('img', '', {'src': 'bild.png'})]
    """
    pattern = r'<(\w+)([^>]*)>(.*?)</\1>|<(\w+)([^>]*)/?>'
    matches = re.finditer(pattern, html, re.DOTALL | re.IGNORECASE)
    result = []

    for m in matches:
        if m.group(1):  # reguläres Tag mit End-Tag
            tag = m.group(1).lower()
            content = m.group(3).strip()
            attr_string = m.group(2)
        else:  # selbstschließendes Tag
            tag = m.group(4).lower()
            content = ""
            attr_string = m.group(5)

        # Attribute in Dict parsen
        attrs = dict(re.findall(r'(\w+)=[\'"]([^\'"]+)[\'"]', attr_string))
        result.append((tag, content, attrs))

    return result
