from enum import Enum

class Category(str, Enum):
    comestibles = "comestibles"
    ocio = "ocio"
    electronica = "electronica"
    servicios_publicos = "servicios_publicos"
    ropa = "ropa"
    salud = "salud"
    otros = "otros"