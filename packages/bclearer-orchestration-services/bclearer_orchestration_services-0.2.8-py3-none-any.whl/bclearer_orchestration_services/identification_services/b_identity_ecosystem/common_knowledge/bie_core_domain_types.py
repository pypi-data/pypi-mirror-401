from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_domain_types import (
    BieDomainTypes,
)


class BieCoreDomainTypes(
    BieDomainTypes
):
    NOT_SET = auto()

    BIE_OBJECT_TYPES = auto()

    BIE_RELATION_TYPES = auto()
