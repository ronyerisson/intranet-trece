import re


def is_valid_email(value: str) -> bool:
    """Validar se o email é @tre-ce.jus.br."""
    has_match = True if value.endswith("@tre-ce.jus.br") else False
    return has_match if value else True


def is_valid_extension(value: str) -> bool:
    """Validar se o o ramal tem 4 dígitos numéricos."""
    has_match = True if re.match(r"^\d{4}$", value) else False
    return has_match if value else True
