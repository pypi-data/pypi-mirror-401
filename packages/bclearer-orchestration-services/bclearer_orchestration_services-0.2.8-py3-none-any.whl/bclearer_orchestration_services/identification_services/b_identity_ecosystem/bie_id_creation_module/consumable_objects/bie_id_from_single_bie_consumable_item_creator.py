from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.hashing.bie_id_base_from_bie_encoding_creator import (
    create_bie_id_base_from_bie_encoding,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.hashing.string_to_bie_encoding_converter import (
    convert_string_to_bie_encoding,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def _create_bie_id_from_single_bie_consumable_item(
    bie_consumable_object_item: object,
) -> BieIds:
    if isinstance(
        bie_consumable_object_item,
        BieIds,
    ):
        return (
            bie_consumable_object_item
        )

    elif isinstance(
        bie_consumable_object_item,
        bytes,
    ):
        bie_encoding = (
            bie_consumable_object_item
        )

    elif isinstance(
        bie_consumable_object_item, str
    ):
        bie_encoding = convert_string_to_bie_encoding(
            input_string=bie_consumable_object_item
        )

    else:
        raise TypeError

    bie_id_base = create_bie_id_base_from_bie_encoding(
        bie_encoding=bie_encoding
    )

    return bie_id_base
