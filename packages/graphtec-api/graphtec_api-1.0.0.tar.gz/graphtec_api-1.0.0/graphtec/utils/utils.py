from graphtec.core.exceptions import CommandError, ParameterError

def get_last_token(response: str | bytes | bytearray | None) -> str:
    """Devuelve el último token no vacío de una respuesta SCPI del GL100."""
    if not response:
        return ""
    
    # Manejo de bytes/bytearray
    if isinstance(response, (bytes, bytearray)):
        decoded = response.decode().strip()
    else:
        decoded = str(response).strip()

    # Reemplazar caracteres por espacios
    for char in [',', ':', '"']:
        decoded = decoded.replace(char, " ")
    
    parts = decoded.split()
    return parts[-1] if parts else ""

def to_str(response):
    """Convierte respuestas a str y la limpia."""
    if response is None:
        return ""
    if isinstance(response, (bytes, bytearray)):
        return response.decode(errors="replace").strip()
    return str(response).strip()

def normalize_choice(value, aliases):
    """
    Normaliza 'value' usando el diccionario 'aliases'
    Devuelve el valor normalizado o lanza ParameterError si no existe.  
    """
    if not isinstance(value, str):
        raise ParameterError(f"Se esperaba str, recibido: {type(value).__name__}")

    val = value.strip().upper()

    normalized_value = aliases.get(val)

    if normalized_value is None:
        valid_display = ", ".join(sorted(set(aliases.values())))
        raise ValueError(f"Valor inválido: {value}. Válidos: {valid_display}")

    return normalized_value

def validate_channel(ch):
    try:
        ch_int = int(ch)
    except (TypeError, ValueError):
        raise ParameterError(f"Canal inválido: {ch}")
    if ch_int not in (1, 2, 3, 4):
        raise ParameterError(f"Canal inválido: {ch_int} (válidos: 1..4)")
    return ch_int

def validate_range(value, as_type, min_val=None, max_val=None, inclusive=True):
    """
    Valida y formatea un valor numérico para los comandos del GL100.
    as_type: int o float
    """
    if isinstance(value, bool):
        raise ValueError(f"bool no es válido como {as_type.__name__}")

    # 1. Conversión y validación de tipo
    try:
        num_value = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"No se pudo convertir a número: {value!r}")

    if as_type is int:
        if not num_value.is_integer():
            raise ValueError(f"El valor no es un valor entero: {value!r}")
        num_value = int(num_value)
    else:
        num_value = float(num_value)

    # 2. Validación de rango
    if min_val is not None:
        limit = as_type(min_val)
        if inclusive:
            if num_value < limit:
                raise ValueError(f"{num_value} debe ser >= {limit}")
        else:
            if num_value <= limit:
                raise ValueError(f"{num_value} debe ser > {limit}")

    if max_val is not None:
        limit = as_type(max_val)
        if inclusive:
            if num_value > limit:
                raise ValueError(f"{num_value} debe ser <= {limit}")
        else:
            if num_value >= limit:
                raise ValueError(f"{num_value} debe ser < {limit}")

    # 3. Formateo de salida según el tipo
    if as_type is int:
        return num_value
    
    # Para floats: máximo 3 decimales, sin ceros sobrantes
    s = f"{num_value:.3f}".rstrip("0").rstrip(".")
    if s:
        return float(s)
    else:
        return 0.0