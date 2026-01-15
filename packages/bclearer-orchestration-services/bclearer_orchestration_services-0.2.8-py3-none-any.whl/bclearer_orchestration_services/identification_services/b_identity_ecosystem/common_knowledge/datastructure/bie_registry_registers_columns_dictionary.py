from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.datastructure.bie_registries_registers_types import (
    BieRegistriesRegistersTypes,
)

BIE_REGISTRY_REGISTERS_COLUMNS_DICTIONARY = {
    BieRegistriesRegistersTypes.BIE_OBJECTS_REGISTER: [
        BieColumnNames.BIE_IDS.b_enum_item_name,
        BieColumnNames.BIE_NAMES.b_enum_item_name,
    ],
    BieRegistriesRegistersTypes.BIE_RELATIONS_REGISTER: [
        BieColumnNames.BIE_PLACE_1_IDS.b_enum_item_name,
        BieColumnNames.BIE_PLACE_2_IDS.b_enum_item_name,
        BieColumnNames.BIE_RELATION_TYPE_IDS.b_enum_item_name,
    ],
    # TODO: Maybe this register is also common??
    # BieBClearerProcessingRegistriesRegistersTypes.U_BIE_REGISTER_SIGNATURES_REGISTER                     :
    #     [
    #         'signature_' + BieColumnNames.BIE_IDS.b_enum_item_name,
    #         'signature_' + BieBClearerProcessingColumnNames.BIE_REGISTRY_NAMES.b_enum_item_name,  # TODO: delete it later, added to check the output easily
    #         'signature_' + BieBClearerProcessingColumnNames.BIE_REGISTRY_IDS.b_enum_item_name,
    #         'signature_bie_id_type_names',  # TODO: delete it later, added to check the output easily
    #         'signature_' + BieBClearerProcessingColumnNames.BIE_ID_TYPE_IDS.b_enum_item_name
    #     ],
}
