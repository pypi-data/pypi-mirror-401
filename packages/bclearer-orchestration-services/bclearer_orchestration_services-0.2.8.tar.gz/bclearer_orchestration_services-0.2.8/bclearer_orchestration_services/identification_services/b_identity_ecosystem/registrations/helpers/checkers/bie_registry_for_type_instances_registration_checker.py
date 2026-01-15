import pandas
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.datastructure.bie_registration_states import (
    BieRegistrationStates,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.datastructure.bie_registries_registers_types import (
    BieRegistriesRegistersTypes,
)
from pandas import DataFrame


def check_bie_registry_for_type_instances_registration(
    bie_registry,
    type_instances: DataFrame,
) -> dict:
    from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registries import (
        BieIdRegistries,
    )

    if not isinstance(
        bie_registry, BieIdRegistries
    ):
        raise TypeError

    bie_relations_register = bie_registry.get_bie_register(
        bie_register_type_enum=BieRegistriesRegistersTypes.BIE_RELATIONS_REGISTER
    )

    registered_relations = (
        bie_relations_register.get_bie_register_dataframe()
    )

    already_registered_relations = (
        pandas.merge(
            registered_relations,
            type_instances,
            how="inner",
        )
    )

    not_yet_registered_relations = type_instances[
        ~type_instances.isin(
            registered_relations.to_dict(
                orient="list"
            )
        ).all(axis=1)
    ]

    result = {
        BieRegistrationStates.ALREADY_REGISTERED_NON_PREFERRED_NAME: already_registered_relations,
        BieRegistrationStates.NOT_YET_REGISTERED: not_yet_registered_relations,
    }

    return result
