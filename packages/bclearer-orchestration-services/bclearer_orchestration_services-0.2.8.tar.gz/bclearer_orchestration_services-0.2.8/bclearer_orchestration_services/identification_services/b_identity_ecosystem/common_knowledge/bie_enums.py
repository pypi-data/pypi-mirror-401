from typing import Optional

from bclearer_core.configurations.datastructure.b_enums import (
    BEnums,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class classproperty:
    """Descriptor to create a class-level property."""

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func(owner)


# TODO: add new abstract method to export snapshot_universe_service to dataframe - export all columns
class BieEnums(BEnums):
    # TODO: add method to register an bie_enum - using the bie_ids calculation - needs designing.
    # TODO: add a bie_enum type component to the b_source
    @classproperty
    def enum_bie_identity(
        self,
    ) -> Optional[BieIds]:
        if not self.b_enum_name:
            return None

        from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
            BieIdCreationFacade,
        )

        enum_bie_identity = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
            input_objects=[
                self.b_enum_name()
            ]
        )

        return enum_bie_identity

    @property
    def item_bie_identity(
        self,
    ) -> Optional[BieIds]:
        if not self.b_enum_item_name:
            return None

        from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
            BieIdCreationFacade,
        )

        item_bie_identity = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
            input_objects=[
                self.enum_bie_identity,
                self.b_enum_item_name,
            ]
        )

        return item_bie_identity
