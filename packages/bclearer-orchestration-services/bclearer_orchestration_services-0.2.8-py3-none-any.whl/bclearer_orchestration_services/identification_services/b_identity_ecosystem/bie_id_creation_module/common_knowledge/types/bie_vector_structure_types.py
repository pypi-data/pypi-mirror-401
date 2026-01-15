from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)


class BieVectorStructureTypes(BieEnums):
    NOT_SET = auto()

    ZERO_DIMENSIONAL = auto()

    SINGLE_DIMENSIONAL = auto()

    MULTI_DIMENSIONAL_ORDER_SENSITIVE = (
        auto()
    )

    MULTI_DIMENSIONAL_ORDER_INSENSITIVE = (
        auto()
    )
