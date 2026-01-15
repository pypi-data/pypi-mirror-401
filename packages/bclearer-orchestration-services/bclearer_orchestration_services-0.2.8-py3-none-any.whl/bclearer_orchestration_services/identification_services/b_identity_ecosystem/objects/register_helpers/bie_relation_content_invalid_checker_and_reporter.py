from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.register_helpers.bie_relation_content_invalid_checker import (
    is_bie_relation_content_invalid,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.registrations.helpers.reporters.bie_relation_content_invalid_reporter import (
    report_bie_relation_content_invalid,
)


def check_and_report_if_bie_relation_content_invalid(
    bie_place_1_id: BieIds,
    bie_place_2_id: BieIds,
    bie_relation_type_id: BieIds,
) -> bool:
    bie_relation_content_invalid = is_bie_relation_content_invalid(
        bie_place_1_id=bie_place_1_id,
        bie_place_2_id=bie_place_2_id,
        bie_relation_type_id=bie_relation_type_id,
    )

    if bie_relation_content_invalid:
        report_bie_relation_content_invalid(
            bie_place_1_id=bie_place_1_id,
            bie_place_2_id=bie_place_2_id,
            bie_relation_type_id=bie_relation_type_id,
        )

    return bie_relation_content_invalid
