from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_core_domain_types import (
    BieCoreDomainTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_core_relation_types import (
    BieCoreRelationTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.datastructure.bie_registries_registers_types import (
    BieRegistriesRegistersTypes,
)


def get_reportable_bie_enums_list() -> (
    list
):
    reportable_bie_enums = [
        BieCoreDomainTypes,
        BieCoreRelationTypes,
        BieRegistriesRegistersTypes,
    ]

    return reportable_bie_enums
