import re
from typing import Tuple

from .find_engine import find_occurrences


def replace_text(
    text: str,
    term: str,
    replacement: str,
    *,
    case_sensitive: bool = True,
    use_regex: bool = False
) -> Tuple[str, int]:
    """
    Substitui ocorrências e retorna (novo_texto, total_de_substituicoes).
    """

    occurrences = find_occurrences(
        text,
        term,
        case_sensitive=case_sensitive,
        use_regex=use_regex
    )

    if not occurrences:
        return text, 0

    flags = 0
    if not case_sensitive:
        flags |= re.IGNORECASE

    if not use_regex:
        term = re.escape(term)

    pattern = re.compile(term, flags)

    new_text, count = pattern.subn(replacement, text)
    return new_text, count
