from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registers import (
    BieIdRegisters,
)


def get_register_dataframes_as_dictionary(
    bie_registry,
) -> dict:
    from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registries import (
        BieIdRegistries,
    )

    if not isinstance(
        bie_registry, BieIdRegistries
    ):
        raise TypeError

    bie_register_dataframes_as_dictionary = (
        dict()
    )

    registers_dictionary = (
        bie_registry.get_registers_dictionary()
    )

    for (
        bie_register
    ) in registers_dictionary.values():
        __add_dataframe_to_dictionary(
            bie_register_dataframes_as_dictionary=bie_register_dataframes_as_dictionary,
            bie_register=bie_register,
        )

    return bie_register_dataframes_as_dictionary


def __add_dataframe_to_dictionary(
    bie_register_dataframes_as_dictionary: dict,
    bie_register: BieIdRegisters,
) -> None:
    register_dataframe = (
        bie_register.get_bie_register_dataframe()
    )

    register_dataframe_stringified = (
        register_dataframe.astype("str")
    )

    bie_register_dataframes_as_dictionary[
        bie_register.bie_register_type_enum.b_enum_item_name
    ] = register_dataframe_stringified
