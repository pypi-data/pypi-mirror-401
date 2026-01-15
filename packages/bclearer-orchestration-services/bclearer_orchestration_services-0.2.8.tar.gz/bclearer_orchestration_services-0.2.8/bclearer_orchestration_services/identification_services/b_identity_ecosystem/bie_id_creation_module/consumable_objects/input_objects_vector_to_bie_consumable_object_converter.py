from typing import List

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.objects.bie_consumable_objects import (
    BieConsumableObjects,
)


def _convert_input_objects_vector_to_bie_consumable_object(
    input_objects_vector: List[object],
) -> BieConsumableObjects:
    bie_consumable_object = (
        BieConsumableObjects()
    )

    for (
        input_object
    ) in input_objects_vector:
        bie_consumable_object.add_to_bie_consumable_object(
            input_object=input_object
        )

    return bie_consumable_object


def convert_input_objects_vector_to_bie_consumable_object(
    input_objects_vector: List[object],
) -> BieConsumableObjects:
    # Public wrapper
    return _convert_input_objects_vector_to_bie_consumable_object(
        input_objects_vector
    )
