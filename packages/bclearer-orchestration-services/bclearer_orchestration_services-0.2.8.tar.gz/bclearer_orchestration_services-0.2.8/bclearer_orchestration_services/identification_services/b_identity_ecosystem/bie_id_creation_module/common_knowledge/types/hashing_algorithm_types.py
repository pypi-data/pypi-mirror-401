from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)


class HashingAlgorithmTypes(BieEnums):
    NOT_SET = auto()

    BLAKE2B = auto()

    BLAKE3 = auto()
