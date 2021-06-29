import typing

def all_bindings() -> list[dict[str, str]]:
    """Get all bndings as a list of dictionaries

    - return empty list if no bindings found
    """

def get_binding(_type: str, provider: typing.Optional[str] = None) -> dict[str, str]:
    """Get bnding as a dictionary for a give type and optional provider

    - return empty dictionary if no binding found
    - raise KeyError if duplicate entry found
    """

    return {}
