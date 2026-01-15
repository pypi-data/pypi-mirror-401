from pandas import DataFrame


def register_type_instances_in_bie_registry(
    bie_registry,
    bie_relations_register,
    not_yet_registered_type_instances: DataFrame,
) -> None:
    from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registries import (
        BieIdRegistries,
    )

    if not isinstance(
        bie_registry, BieIdRegistries
    ):
        raise TypeError

    bie_relations_register.concatenate_dataframe(
        dataframe=not_yet_registered_type_instances
    )
