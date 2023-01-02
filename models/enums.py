from enum import Enum


class ProductType(str, Enum):
    chives = "chives"
    oregano = "oregano"
    basil = "basil"
    tarragon = "tarragon"
    corriander = "corriander"
    dill = "dill"
    marjoram = "marjoram"
    mint = "mint"
    baileaf = "baileaf"
    rosemary = "rosemary"
    thyme = "thyme"
    thai_basil = "thay basil"
    parsley = "parsley"


class ProductMeasurement(str, Enum):
    kg = "kilo"
    lb = "libra"


class ProductPackage(str, Enum):
    bolsa = "bolsa"
    caja = "caja"


class ProductStatus(str, Enum):
    sin_modificar = "sin modificar"
    modificado = "modificado"


class UserStatus(str, Enum):
    activo = "activo"
    inactivo = "inactivo"


class RoleType(str, Enum):
    master = "master"
    admin = "admin"
    distribuidor = "distribuidor"
