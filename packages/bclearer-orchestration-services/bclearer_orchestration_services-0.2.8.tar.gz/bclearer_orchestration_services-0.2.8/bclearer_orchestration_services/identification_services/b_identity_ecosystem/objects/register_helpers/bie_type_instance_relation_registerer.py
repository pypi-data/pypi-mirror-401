from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_core_relation_types import (
    BieCoreRelationTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.register_helpers.bie_relation_if_valid_registerer import (
    register_bie_relation_if_valid,
)


def register_bie_type_instance_relation(
    calling_bie_id_relations_register,
    bie_place_1_id: BieIds,
    bie_place_2_id: BieIds,
) -> None:
    bie_relation_type_id = (
        BieCoreRelationTypes.BIE_TYPES_INSTANCES.item_bie_identity
    )

    register_bie_relation_if_valid(
        calling_bie_id_relations_register=calling_bie_id_relations_register,
        bie_place_1_id=bie_place_1_id,
        bie_place_2_id=bie_place_2_id,
        bie_relation_type_id=bie_relation_type_id,
    )
