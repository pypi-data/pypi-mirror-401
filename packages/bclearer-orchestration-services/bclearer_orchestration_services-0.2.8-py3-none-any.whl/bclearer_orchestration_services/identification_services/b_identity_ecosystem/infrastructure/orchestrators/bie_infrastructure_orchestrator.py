from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.registrations.bie_infrastructure_registries import (
    BieInfrastructureRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.registrations.helpers.bie_infrastructure_enums_exporter_and_register import (
    register_and_export_bie_infrastructure_enums,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_universes import (
    BieIdUniverses,
)
from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)


@run_and_log_function
def orchestrate_bie_infrastructure(
    reportable_additional_enums: list,
    bie_universe_type: type,
) -> BieIdUniverses:
    parallel_bie_universe = (
        bie_universe_type()
    )

    bie_infrastructure_registry = (
        parallel_bie_universe.bie_infrastructure_registry
    )

    __run_infrastructure_components(
        bie_infrastructure_registry=bie_infrastructure_registry,
        reportable_additional_enums=reportable_additional_enums,
    )

    return parallel_bie_universe


def __run_infrastructure_components(
    bie_infrastructure_registry: BieInfrastructureRegistries,
    reportable_additional_enums: list,
) -> None:
    register_and_export_bie_infrastructure_enums(
        bie_registry=bie_infrastructure_registry,
        reportable_additional_enums=reportable_additional_enums,
    )
