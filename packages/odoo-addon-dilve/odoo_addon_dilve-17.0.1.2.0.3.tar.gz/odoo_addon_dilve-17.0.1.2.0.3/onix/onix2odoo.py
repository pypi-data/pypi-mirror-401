from enum import Enum
from .onix_book_product_code_lists import List17, List19, List48, List50
import logging

_logger = logging.getLogger(__name__)

class UnnamedPersons(Enum):
    """
    Mapper for Onix Product Code List - List 19 - UnnamedPersons
    """
    def __init__(self, code, name):
        self.code = code
        self.display_name = name

    UNKNOWN = (List19.VALUE_01, "Unknown")
    ANONYMOUS = (List19.VALUE_02, "Anonymous")
    ET_AL = (List19.VALUE_03, "et al")
    VARIOUS = (List19.VALUE_04, "Various")
    SYNTHESISED_VOICE_MALE = (List19.VALUE_05, "Synthesised voice – male")
    SYNTHESISED_VOICE_FEMALE = (List19.VALUE_06, "Synthesized voice – female")
    SYNTHESISED_VOICE_UNSPECIFIED = (List19.VALUE_07, "Synthesized voice – unspecified")
    SYNTHESISES_VOICE_BASED_ON_REAL_VOICE_ACTOR = (List19.VALUE_08, "Synthesized voice – based on real voice actor")
    AI = (List19.VALUE_09, "AI (Artificial intelligence)")

    @classmethod
    def get_display_name(cls, code):
        for element in cls:
            if element.code == code:
                return element.display_name
        return 'Unknown'

class ContributorRole(Enum):
    """
    Mapper for Onix Product Code List - List 17 - Contributor role code
    """
    def __init__(self, code, reference):
        self.code = code
        self.reference = reference

    AUTHOR = (List17.A01, "gestion_editorial.contact_type_author")
    SCREENPLAY_BY = (List17.A03, "gestion_editorial.contact_type_screenplay_by")
    DESIGNED_BY = (List17.A11, "gestion_editorial.contact_type_designed_by")
    ILLUSTRATED_BY = (List17.A12, "gestion_editorial.contact_type_illustrator")
    PHOTOGRAPHER = (List17.A13, "gestion_editorial.contact_type_photographer")
    TEXT_BY = (List17.A14, "gestion_editorial.contact_type_text_by")
    PROLOGUE_BY = (List17.A16, "gestion_editorial.contact_type_prologue_by")
    COMMENTARIES_BY = (List17.A21, "gestion_editorial.contact_type_commentaries_by")
    EPILOGUE_BY = (List17.A22, "gestion_editorial.contact_type_epilogue_by")
    FOREWORD_BY = (List17.A23, "gestion_editorial.contact_type_prologue_by")
    INTRODUCTION_BY = (List17.A24, "gestion_editorial.contact_type_introduction_by")
    DRAWINGS_BY = (List17.A35, "gestion_editorial.contact_type_drawings_by")
    ILLUSTRATION_BY = (List17.A36, "gestion_editorial.contact_type_illustrator")
    EDITOR = (List17.B01, "gestion_editorial.contact_type_editor")
    TRANSLATION_BY = (List17.B06, "gestion_editorial.contact_type_translator")
    GUEST_EDITOR = (List17.B12, "gestion_editorial.contact_type_guest_editor")

    @classmethod
    def get_reference(cls, code):
        for element in cls:
            if element.code == code:
                return element.reference
        return "gestion_editorial.contact_type_unknown"

class MeasureType(Enum):
    """
       Mapper for Onix Product Code List - List 48 - MeasureType
    """

    def __init__(self, code):
        self.code = code

    HEIGHT = List48.VALUE_01
    WIDTH = List48.VALUE_02
    THICKNESS = List48.VALUE_03
    WEIGHT = List48.VALUE_08

class MeasureUnit(Enum):
    """
       Mapper for Onix Product Code List - List 50 - MeasureUnit
    """

    def __init__(self, code, reference):
        self.code = code
        self.reference = reference

    CM = (List50.CM, "uom.product_uom_cm")
    GR = (List50.GR, "uom.product_uom_gram")
    IN = (List50.IN, "uom.product_uom_inch")
    KG = (List50.KG, "uom.product_uom_kgm")
    LB = (List50.LB, "uom.product_uom_lb")
    MM = (List50.MM, "uom.product_uom_millimeter")
    OZ = (List50.OZ, "uom.product_uom_oz")
    PX = (List50.PX, None)

    @classmethod
    def get_reference(cls, code):
        for element in cls:
            if element.code == code:
                return element.reference
        return "uom.product_uom_kgm"
