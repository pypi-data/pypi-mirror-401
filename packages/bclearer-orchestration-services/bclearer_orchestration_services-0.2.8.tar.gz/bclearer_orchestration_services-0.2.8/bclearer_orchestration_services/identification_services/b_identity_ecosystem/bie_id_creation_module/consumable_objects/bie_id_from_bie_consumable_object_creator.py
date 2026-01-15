from typing import List

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_ids.order_insensitive_bie_id_for_multiple_bie_ids_creator import (
    __create_order_insensitive_bie_id_for_multiple_bie_ids,
    create_order_insensitive_bie_id_for_multiple_bie_ids,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_ids.order_sensitive_bie_id_for_multiple_bie_ids_creator import (
    __create_order_sensitive_bie_id_for_multiple_bie_ids,
    create_order_sensitive_bie_id_for_multiple_bie_ids,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.common_knowledge.types.bie_vector_structure_types import (
    BieVectorStructureTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.consumable_objects.bie_id_from_single_bie_consumable_item_creator import (
    _create_bie_id_from_single_bie_consumable_item,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.objects.bie_consumable_objects import (
    BieConsumableObjects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def _create_bie_id_from_bie_consumable_object(
    bie_consumable_object: BieConsumableObjects,
    bie_vector_structure_type: BieVectorStructureTypes,
) -> BieIds:
    bie_ids = __create_list_of_bie_ids_from_bie_consumable_object(
        bie_consumable_object=bie_consumable_object
    )

    bie_id = __create_bie_id(
        bie_ids=bie_ids,
        bie_vector_structure_type=bie_vector_structure_type,
    )

    return bie_id


def __create_bie_id(
    bie_ids: list[BieIds],
    bie_vector_structure_type: BieVectorStructureTypes,
) -> BieIds:
    match bie_vector_structure_type:
        # TODO: add or
        case (
            BieVectorStructureTypes.SINGLE_DIMENSIONAL
        ):
            return __create_order_sensitive_bie_id_for_multiple_bie_ids(
                bie_ids=bie_ids
            )

        case (
            BieVectorStructureTypes.MULTI_DIMENSIONAL_ORDER_SENSITIVE
        ):
            return __create_order_sensitive_bie_id_for_multiple_bie_ids(
                bie_ids=bie_ids
            )

        case (
            BieVectorStructureTypes.MULTI_DIMENSIONAL_ORDER_INSENSITIVE
        ):
            return __create_order_insensitive_bie_id_for_multiple_bie_ids(
                bie_ids=bie_ids
            )

        case _:
            raise NotImplementedError()


def __create_list_of_bie_ids_from_bie_consumable_object(
    bie_consumable_object: BieConsumableObjects,
) -> List[BieIds]:
    bie_ids = list()

    for (
        bie_consumable_object_item
    ) in (
        bie_consumable_object.bie_consumable_object_list
    ):
        __add_bie_consumable_object_item_to_bie_ids(
            bie_ids=bie_ids,
            bie_consumable_object_item=bie_consumable_object_item,
        )

    return bie_ids


def __add_bie_consumable_object_item_to_bie_ids(
    bie_ids: List[BieIds],
    bie_consumable_object_item: str,
) -> None:
    bie_id = _create_bie_id_from_single_bie_consumable_item(
        bie_consumable_object_item=bie_consumable_object_item
    )

    bie_ids.append(bie_id)


def create_bie_id_from_bie_consumable_object(
    bie_consumable_object: BieConsumableObjects,
    bie_vector_structure_type: BieVectorStructureTypes,
) -> BieIds:
    # Public wrapper
    if bie_vector_structure_type in (
        BieVectorStructureTypes.SINGLE_DIMENSIONAL,
        BieVectorStructureTypes.MULTI_DIMENSIONAL_ORDER_SENSITIVE,
    ):
        bie_ids = __create_list_of_bie_ids_from_bie_consumable_object(
            bie_consumable_object
        )
        return create_order_sensitive_bie_id_for_multiple_bie_ids(
            bie_ids
        )

    if (
        bie_vector_structure_type
        == BieVectorStructureTypes.MULTI_DIMENSIONAL_ORDER_INSENSITIVE
    ):
        bie_ids = __create_list_of_bie_ids_from_bie_consumable_object(
            bie_consumable_object
        )
        return create_order_insensitive_bie_id_for_multiple_bie_ids(
            bie_ids
        )

    raise NotImplementedError()
