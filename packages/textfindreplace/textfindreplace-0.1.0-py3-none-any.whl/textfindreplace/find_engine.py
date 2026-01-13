import re
from typing import List, Tuple


def find_occurrences(
    text: str,
    term: str,
    *,
    case_sensitive: bool = True,
    use_regex: bool = False
) -> List[Tuple[int, int]]:
    """
    Retorna uma lista de ocorrências (inicio, fim) de um termo em um texto.
    """

    if not term:
        return []

    flags = 0
    if not case_sensitive:
        flags |= re.IGNORECASE

    if not use_regex:
        term = re.escape(term)

    pattern = re.compile(term, flags)

    return [(m.start(), m.end()) for m in pattern.finditer(text)]
