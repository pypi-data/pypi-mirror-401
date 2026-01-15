from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.datastructure.bie_registries_registers_types import (
    BieRegistriesRegistersTypes,
)
from pandas import DataFrame


def register_objects_in_bie_registry(
    bie_registry,
    not_yet_registered_objects: DataFrame,
) -> None:
    from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registries import (
        BieIdRegistries,
    )

    if not isinstance(
        bie_registry, BieIdRegistries
    ):
        raise TypeError

    bie_objects_register = bie_registry.get_bie_register(
        bie_register_type_enum=BieRegistriesRegistersTypes.BIE_OBJECTS_REGISTER
    )

    bie_objects_register.concatenate_dataframe(
        dataframe=not_yet_registered_objects
    )
