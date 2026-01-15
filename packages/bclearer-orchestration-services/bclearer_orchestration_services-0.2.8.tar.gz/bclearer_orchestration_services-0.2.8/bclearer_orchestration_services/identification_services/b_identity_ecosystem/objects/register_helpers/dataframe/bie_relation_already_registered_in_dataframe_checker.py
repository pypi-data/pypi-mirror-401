from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


# TODO: depending of the type of the register, this method will deal with both options, dataframes and dictionaries?
def is_bie_relation_already_registered_in_dataframe(
    calling_bie_id_relations_register,
    new_bie_relation_bie_id_list_signature_bie_id: BieIds,
) -> bool:
    from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_relations_registers import (
        BieIdRelationsRegisters,
    )

    if not isinstance(
        calling_bie_id_relations_register,
        BieIdRelationsRegisters,
    ):
        raise TypeError()

    bie_register_dataframe = (
        calling_bie_id_relations_register.get_bie_register_dataframe()
    )

    bie_type_instance_already_registered = (
        new_bie_relation_bie_id_list_signature_bie_id.int_value
        in bie_register_dataframe.index
    )

    return bie_type_instance_already_registered
