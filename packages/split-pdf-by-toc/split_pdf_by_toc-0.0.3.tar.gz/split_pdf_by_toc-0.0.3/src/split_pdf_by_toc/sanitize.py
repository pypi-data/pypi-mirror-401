import re
import unicodedata

# Windows reserved names (case-insensitive)
_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def sanitize_filename(
    name: str,
    *,
    replacement: str = "-",
    max_length: int = 255,
) -> str:
    """
    Sanitize a filename for cross-platform filesystem safety.

    - Removes path separators (/ and \\)
    - Removes control characters
    - Avoids Windows reserved names
    - Trims trailing dots/spaces (Windows)
    - Normalizes Unicode (NFC)
    """

    name = unicodedata.normalize("NFC", name)

    # Replace path separators and other illegal characters
    name = re.sub(r'[\/\\:*?"<>|]', replacement, name)

    # Remove ASCII control characters
    name = re.sub(r"[\x00-\x1f\x7f]", "", name)

    # Collapse repeated replacements
    name = re.sub(re.escape(replacement) + r"+", replacement, name)

    # Strip leading/trailing whitespace and dots
    name = name.strip(" .")

    # Avoid Windows reserved device names
    root, dot, ext = name.partition(".")
    if root.upper() in _RESERVED_NAMES:
        root = f"_{root}"
        name = root + (dot + ext if dot else "")

    # Enforce max filename length (preserve extension)
    if len(name) > max_length:
        if dot:
            ext_len = len(ext) + 1
            name = root[: max_length - ext_len] + "." + ext
        else:
            name = name[:max_length]

    return name
