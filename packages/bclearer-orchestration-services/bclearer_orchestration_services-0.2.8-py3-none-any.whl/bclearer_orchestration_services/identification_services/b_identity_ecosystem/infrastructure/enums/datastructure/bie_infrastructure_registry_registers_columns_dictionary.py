from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.enums.datastructure.bie_infrastructure_column_names import (
    BieInfrastructureColumnNames,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.enums.datastructure.bie_infrastructure_registries_registers_types import (
    BieInfrastructureRegistriesRegistersTypes,
)

BIE_INFRASTRUCTURE_REGISTRY_REGISTERS_COLUMNS_DICTIONARY = {
    BieInfrastructureRegistriesRegistersTypes.BIE_ID_TO_SOURCE_UUID_MAPPINGS_REGISTER: [
        BieColumnNames.BIE_IDS.b_enum_item_name,
        BieInfrastructureColumnNames.SOURCE_UUIDS.b_enum_item_name,
    ]
}
