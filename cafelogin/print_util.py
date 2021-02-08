import colorama


def clr(*colored_text: str, sep: str = "") -> str:
    """Add the color reset code after each colored_text."""
    return (sep + colorama.Style.RESET_ALL).join(
        colored_text
    ) + colorama.Style.RESET_ALL


def print_clr(*colored_text: str, sep: str = ""):
    """Add the color reset code after each colored_text."""
    print(clr(*colored_text, sep=sep))
