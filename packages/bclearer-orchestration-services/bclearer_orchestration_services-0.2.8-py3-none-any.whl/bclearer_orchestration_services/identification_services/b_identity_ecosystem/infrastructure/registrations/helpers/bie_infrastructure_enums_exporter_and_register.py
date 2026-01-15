from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.reportable_bie_enums_list_getter import (
    get_reportable_bie_enums_list,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registries import (
    BieIdRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.registrations.helpers.registerers.bie_enums_to_registry_base_register import (
    register_bie_enums_to_registry_base,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def register_and_export_bie_infrastructure_enums(
    bie_registry: BieIdRegistries,
    reportable_additional_enums: list,
) -> None:
    # TODO: This has been copied to the infrastructure registry - will eventually need to be deleted
    reportable_bie_enums = (
        get_reportable_bie_enums_list()
    )

    bie_enums = (
        reportable_bie_enums
        + reportable_additional_enums
        + [BieEnums]
    )

    for child_enum in bie_enums:
        register_bie_enums_to_registry_base(
            bie_enum_type=child_enum,
            bie_registry=bie_registry,
        )
