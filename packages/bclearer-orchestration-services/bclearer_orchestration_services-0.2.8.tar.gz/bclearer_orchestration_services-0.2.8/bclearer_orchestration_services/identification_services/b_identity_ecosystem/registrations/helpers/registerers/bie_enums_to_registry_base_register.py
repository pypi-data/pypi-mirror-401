from typing import Type

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registries import (
    BieIdRegistries,
)
from bclearer_orchestration_services.identification_services.naming_service.b_sequence_names import (
    BSequenceNames,
)


def register_bie_enums_to_registry_base(
    bie_enum_type: Type[BieEnums],
    bie_registry: BieIdRegistries,
) -> None:
    __register_bie_enum_object(
        bie_enum_type=bie_enum_type,
        bie_registry=bie_registry,
    )

    __register_bie_enums_to_bie_registry(
        bie_enum_type=bie_enum_type,
        bie_registry=bie_registry,
    )


def __register_bie_enum_object(
    bie_enum_type: Type[BieEnums],
    bie_registry: BieIdRegistries,
) -> None:
    bie_sequence_name = BSequenceNames(
        initial_b_sequence_name_list=[
            bie_enum_type.b_enum_name()
        ]
    )

    # TODO: this method is temporal, needs to review the creating new bie_ids issue here.
    #  it needs to use the enum_bie_identity property instead
    if bie_enum_type != BieEnums:
        bie_enum_parent = (
            bie_enum_type.__bases__[0]
        )

        # TODO: For the children table_names of BieEnums, their parent is not an instance of BieEnums, it IS BieEnums - FIXED
        # if isinstance(bie_enum_parent, BieEnums):
        if bie_enum_parent == BieEnums:
            bie_id_type_id = (
                bie_enum_parent.enum_bie_identity
            )

        else:
            bie_id_type_id = None

        bie_item_id = (
            bie_enum_type.enum_bie_identity
        )

    else:
        bie_id_type_id = None

        bie_item_id = (
            bie_enum_type.enum_bie_identity
        )

    bie_registry.register_bie_id_and_type_instance(
        bie_id_type_id=bie_id_type_id,
        bie_sequence_name=bie_sequence_name,
        bie_item_id=bie_item_id,
    )


def __register_bie_enums_to_bie_registry(
    bie_registry: BieIdRegistries,
    bie_enum_type: Type[BieEnums],
) -> None:
    for bie_enum_item in bie_enum_type:
        __register_bie_enum_item(
            bie_bclearer_processing_registry=bie_registry,
            bie_enum_item=bie_enum_item,
        )


def __register_bie_enum_item(
    bie_bclearer_processing_registry: BieIdRegistries,
    bie_enum_item,
) -> None:
    if bie_enum_item.name == "NOT_SET":
        return

    if isinstance(
        bie_enum_item, BieEnums
    ):
        b_sequence_name_component = (
            bie_enum_item.b_enum_item_name
        )

    else:
        b_sequence_name_component = (
            bie_enum_item.b_enum_item_name
        )

    bie_sequence_name = BSequenceNames(
        initial_b_sequence_name_list=[
            b_sequence_name_component
        ]
    )

    # bie_sequence_name.add_name_to_b_sequence_name_list(
    #     name=bie_enum_item.name)

    bie_bclearer_processing_registry.register_bie_id_and_type_instance(
        bie_id_type_id=bie_enum_item.enum_bie_identity,
        bie_sequence_name=bie_sequence_name,
        bie_item_id=bie_enum_item.item_bie_identity,
    )
