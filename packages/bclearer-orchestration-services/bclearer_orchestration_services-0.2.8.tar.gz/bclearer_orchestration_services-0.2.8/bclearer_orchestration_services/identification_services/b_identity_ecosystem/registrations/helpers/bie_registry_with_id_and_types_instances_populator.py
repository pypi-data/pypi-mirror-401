import copy

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registers import (
    BieIdRegisters,
)


def populate_bie_registry_with_id_and_types_instances(
    bie_registry,
    bie_id_register: BieIdRegisters,
    bie_id_types_instances_register: BieIdRegisters,
) -> None:
    from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registries import (
        BieIdRegistries,
    )

    if not isinstance(
        bie_registry, BieIdRegistries
    ):
        raise TypeError

    __update_register(
        bie_registry=bie_registry,
        new_register=bie_id_register,
    )

    __update_register(
        bie_registry=bie_registry,
        new_register=bie_id_types_instances_register,
    )


def __update_register(
    bie_registry,
    new_register: BieIdRegisters,
):
    bie_register_copy = copy.deepcopy(
        new_register
    )

    registers_dictionary = (
        bie_registry.get_registers_dictionary()
    )

    del registers_dictionary[
        new_register.bie_register_type_enum
    ]

    bie_registry.update_register_dictionary(
        dictionary_update={
            bie_register_copy.bie_register_type_enum: bie_register_copy
        }
    )
