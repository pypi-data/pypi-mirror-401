from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)


class BieRegistriesRegistersTypes(
    BieEnums
):
    NOT_SET = auto()

    # TODO: split the next out
    BIE_OBJECTS_REGISTER = auto()

    BIE_RELATIONS_REGISTER = auto()
