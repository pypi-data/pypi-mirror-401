from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.registrations.helpers.reporters.bie_relation_already_registered_reporter import (
    report_bie_relation_already_registered,
)


def check_and_report_if_bie_relation_already_registered(
    calling_bie_id_relations_register,
    bie_place_1_id: BieIds,
    bie_place_2_id: BieIds,
    bie_relation_type_id: BieIds,
    bie_relation_bie_id_list_signature_bie_id: BieIds,
) -> bool:
    from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_relations_registers import (
        BieIdRelationsRegisters,
    )

    if not isinstance(
        calling_bie_id_relations_register,
        BieIdRelationsRegisters,
    ):
        raise TypeError()

    bie_relation_already_registered = calling_bie_id_relations_register.is_bie_relation_already_registered(
        bie_relation_bie_id_list_signature_bie_id=bie_relation_bie_id_list_signature_bie_id
    )

    if bie_relation_already_registered:
        report_bie_relation_already_registered(
            calling_bie_id_relations_register=calling_bie_id_relations_register,
            bie_place_1_id=bie_place_1_id,
            bie_place_2_id=bie_place_2_id,
            bie_relation_type_id=bie_relation_type_id,
        )

    return (
        bie_relation_already_registered
    )
