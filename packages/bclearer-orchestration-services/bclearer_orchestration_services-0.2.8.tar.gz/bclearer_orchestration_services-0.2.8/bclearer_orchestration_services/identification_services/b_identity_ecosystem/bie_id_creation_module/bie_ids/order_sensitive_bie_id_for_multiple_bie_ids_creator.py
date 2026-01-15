from typing import List

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.hashing.bie_id_base_from_bie_encoding_creator import (
    __create_bie_id_base_from_bie_encoding,
    create_bie_id_base_from_bie_encoding,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.hashing.string_to_bie_encoding_converter import (
    __convert_string_to_bie_encoding,
    convert_string_to_bie_encoding,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def create_order_sensitive_bie_id_for_multiple_bie_ids(
    bie_ids: List[BieIds],
) -> BieIds:
    # Public wrapper
    if len(bie_ids) == 1:
        return bie_ids[0]
    list_of_bie_ids_as_string = str(
        bie_ids
    )

    bie_encoding = (
        convert_string_to_bie_encoding(
            list_of_bie_ids_as_string
        )
    )

    return create_bie_id_base_from_bie_encoding(
        bie_encoding
    )


def __create_order_sensitive_bie_id_for_multiple_bie_ids(
    bie_ids: List[BieIds],
) -> BieIds:
    if len(bie_ids) == 1:
        return bie_ids[0]

    list_of_bie_ids_as_string = str(
        bie_ids
    )

    bie_encoding = __convert_string_to_bie_encoding(
        input_string=list_of_bie_ids_as_string
    )

    bie_id = __create_bie_id_base_from_bie_encoding(
        bie_encoding=bie_encoding
    )

    return bie_id
