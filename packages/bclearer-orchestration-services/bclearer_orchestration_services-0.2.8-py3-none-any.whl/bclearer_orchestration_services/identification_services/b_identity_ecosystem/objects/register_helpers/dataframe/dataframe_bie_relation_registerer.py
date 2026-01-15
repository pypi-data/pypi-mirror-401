from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.datastructure.bie_registries_registers_types import (
    BieRegistriesRegistersTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.datastructure.bie_registry_registers_columns_dictionary import (
    BIE_REGISTRY_REGISTERS_COLUMNS_DICTIONARY,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from pandas import DataFrame


# TODO: Maybe inside this method it will check the register implementation (dataframe/dictionary) and it will deal with
#  both registrations?
def register_dataframe_bie_relation(
    calling_bie_id_relations_register,
    bie_place_1_id: BieIds,
    bie_place_2_id: BieIds,
    bie_relation_type_id: BieIds,
    bie_relation_row_signature_bie_id: BieIds,
):
    bie_id_relations_register_columns = BIE_REGISTRY_REGISTERS_COLUMNS_DICTIONARY[
        BieRegistriesRegistersTypes.BIE_RELATIONS_REGISTER
    ]

    bie_id_relations_dataframe_row = DataFrame(
        data=[
            [
                bie_place_1_id,
                bie_place_2_id,
                bie_relation_type_id,
            ]
        ],
        columns=bie_id_relations_register_columns,
        index=[
            bie_relation_row_signature_bie_id.int_value
        ],
    )

    calling_bie_id_relations_register.concatenate_dataframe(
        dataframe=bie_id_relations_dataframe_row
    )
