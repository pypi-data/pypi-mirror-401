from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)


class BieRegistrationStates(BieEnums):
    NOT_SET = auto()

    NOT_YET_REGISTERED = auto()

    ALREADY_REGISTERED_NON_PREFERRED_NAME = (
        auto()
    )

    ALREADY_REGISTERED_PREFERRED_NAME = (
        auto()
    )
