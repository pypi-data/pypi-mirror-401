from typing import Optional

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from matplotlib._api import (
    classproperty,
)


class BieExtendedEnums(BieEnums):
    @classproperty
    def get_bie_id_additional_input_list(
        self,
    ):
        pass

    @property
    def item_bie_identity(
        self,
    ) -> Optional[BieIds]:
        if not self.b_enum_item_name:
            return None

        input_list = [
            self.enum_bie_identity,
            self.b_enum_item_name,
        ]

        additional_input_list = (
            self.get_bie_id_additional_input_list()
        )

        extended_input_list = (
            input_list
            + additional_input_list
        )

        item_bie_identity = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
            input_objects=[
                extended_input_list
            ]
        )

        return item_bie_identity
