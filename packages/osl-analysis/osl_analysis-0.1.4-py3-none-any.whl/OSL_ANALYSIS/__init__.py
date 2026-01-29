# OSL_ANALYSIS package initialization

__version__ = "0.1.3"
def set_E_values():
    global E1, E2, E3
    E1 = float(input("Enter E1: "))
    E2 = float(input("Enter E2: "))
    E3 = float(input("Enter E3: "))

# Inicializamos con None para evitar errores al importar
E1 = None
E2 = None
E3 = None

# You can import the main module here if desired
from . import modulo1
from . import modulo2
from . import modulo3
from . import modulo4



