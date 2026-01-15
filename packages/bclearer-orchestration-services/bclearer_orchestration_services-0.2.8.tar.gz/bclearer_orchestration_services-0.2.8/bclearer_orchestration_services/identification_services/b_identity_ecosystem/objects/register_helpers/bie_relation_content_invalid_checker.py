from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def is_bie_relation_content_invalid(
    bie_place_1_id: BieIds,
    bie_place_2_id: BieIds,
    bie_relation_type_id: BieIds,
) -> bool:
    if bie_place_1_id is None:
        raise Exception(
            "Parameter bie_item_id is None or empty."
        )

    if (
        (not bie_place_1_id)
        | (not bie_place_2_id)
        | (not bie_relation_type_id)
    ):
        return True

    return False
