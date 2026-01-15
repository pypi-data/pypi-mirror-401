from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.register_helpers.bie_relation_already_registered_checker_and_reporter import (
    check_and_report_if_bie_relation_already_registered,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.register_helpers.bie_relation_content_invalid_checker_and_reporter import (
    check_and_report_if_bie_relation_content_invalid,
)


# TODO: This may be converted into a BieRegisters object method
def register_bie_relation_if_valid(
    calling_bie_id_relations_register,
    bie_place_1_id: BieIds,
    bie_place_2_id: BieIds,
    bie_relation_type_id: BieIds,
) -> None:
    from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_relations_registers import (
        BieIdRelationsRegisters,
    )

    if not isinstance(
        calling_bie_id_relations_register,
        BieIdRelationsRegisters,
    ):
        raise TypeError()

    bie_relation_content_invalid = check_and_report_if_bie_relation_content_invalid(
        bie_place_1_id=bie_place_1_id,
        bie_place_2_id=bie_place_2_id,
        bie_relation_type_id=bie_relation_type_id,
    )

    if bie_relation_content_invalid:
        return

    bie_relation_bie_id_list_signature_bie_id = __get_bie_relation_bie_id_list_signature_bie_id(
        bie_place_1_id=bie_place_1_id,
        bie_place_2_id=bie_place_2_id,
        bie_relation_type_id=bie_relation_type_id,
    )

    bie_relation_already_registered = check_and_report_if_bie_relation_already_registered(
        calling_bie_id_relations_register=calling_bie_id_relations_register,
        bie_place_1_id=bie_place_1_id,
        bie_place_2_id=bie_place_2_id,
        bie_relation_type_id=bie_relation_type_id,
        bie_relation_bie_id_list_signature_bie_id=bie_relation_bie_id_list_signature_bie_id,
    )

    if bie_relation_already_registered:
        return

    calling_bie_id_relations_register.register_bie_relation(
        bie_place_1_id=bie_place_1_id,
        bie_place_2_id=bie_place_2_id,
        bie_relation_type_id=bie_relation_type_id,
        bie_relation_row_signature_bie_id=bie_relation_bie_id_list_signature_bie_id,
    )


def __get_bie_relation_bie_id_list_signature_bie_id(
    bie_place_1_id: BieIds,
    bie_place_2_id: BieIds,
    bie_relation_type_id: BieIds,
) -> BieIds:
    bie_relation_bie_id_list = [
        bie_place_1_id,
        bie_place_2_id,
        bie_relation_type_id,
    ]

    bie_relation_bie_id_list_signature_bie_id = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
        input_objects=bie_relation_bie_id_list
    )

    return bie_relation_bie_id_list_signature_bie_id
