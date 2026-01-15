from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_relation_types import (
    BieRelationTypes,
)


class BieCoreRelationTypes(
    BieRelationTypes
):
    NOT_SET = auto()

    # TODO - moved from graph
    BIE_TYPES_INSTANCES = auto()

    BIE_WHOLES_PARTS = auto()

    BIE_SUB_SUPER_SETS = auto()

    BIE_SAME_AS = auto()

    BIE_SUMMED = auto()

    BIE_SUMMING = auto()

    BIE_COUPLES = auto()
