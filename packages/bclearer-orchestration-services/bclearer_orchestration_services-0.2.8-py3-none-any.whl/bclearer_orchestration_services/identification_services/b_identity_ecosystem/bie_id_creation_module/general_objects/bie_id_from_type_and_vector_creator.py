from typing import List, Optional

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.common_knowledge.types.bie_vector_structure_types import (
    BieVectorStructureTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.consumable_objects.bie_id_from_bie_consumable_object_creator import (
    create_bie_id_from_bie_consumable_object,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.consumable_objects.input_objects_vector_to_bie_consumable_object_converter import (
    convert_input_objects_vector_to_bie_consumable_object,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def create_bie_id_from_type_and_vector(
    input_objects_vector: List[object],
    bie_vector_structure_type: BieVectorStructureTypes,
    bie_domain_type: Optional[BieEnums],
) -> BieIds:
    bie_consumable_object = convert_input_objects_vector_to_bie_consumable_object(
        input_objects_vector=input_objects_vector
    )

    vector_bie_id = create_bie_id_from_bie_consumable_object(
        bie_consumable_object=bie_consumable_object,
        bie_vector_structure_type=bie_vector_structure_type,
    )

    if not bie_domain_type:
        return vector_bie_id

    typed_vector_bie_id = create_bie_id_from_type_and_vector(
        input_objects_vector=[
            bie_domain_type.item_bie_identity,
            vector_bie_id,
        ],
        bie_vector_structure_type=BieVectorStructureTypes.MULTI_DIMENSIONAL_ORDER_SENSITIVE,
        bie_domain_type=None,
    )

    return typed_vector_bie_id
