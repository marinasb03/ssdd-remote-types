"""Clase customset."""
from typing import Optional

class StringSet(set):
    """Conjunto que solo admite elementos de tipo str."""

    def __init__(self, *args, force_upper_case: Optional[bool] = False, **kwargs):
        if args:
            for item in args[0]:
                if not isinstance(item, str):
                    raise ValueError("Todos los elementos deben ser cadenas de texto.")

        self.upper_case = force_upper_case
        super().__init__(*args, **kwargs)

    def add(self, item: str) -> None:
        if not isinstance(item, str):
            raise ValueError("Solo se permiten cadenas.")
        if self.upper_case:
            item = item.upper()
        super().add(item)

    def __contains__(self, o: object) -> bool:
        if not isinstance(o, str):
            o = str(o)
        if self.upper_case:
            o = o.upper()
        return super().__contains__(o)
