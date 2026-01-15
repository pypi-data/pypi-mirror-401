from typing import Set

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class BieSignatures:
    def __init__(self) -> None:
        self.bie_ids_set: Set[
            BieIds
        ] = set()

        # TODO decide what an empty bie looks like
        self.signature_sum_bie_id: (
            BieIds
        ) = BieIds(int_value=0)

    def add_bie_id(
        self, bie_id: BieIds
    ) -> None:
        if bie_id in self.bie_ids_set:
            return

        self.bie_ids_set.add(bie_id)

        self.signature_sum_bie_id = BieIdCreationFacade.create_order_insensitive_bie_id_for_multiple_objects(
            input_objects=[
                self.signature_sum_bie_id,
                bie_id,
            ]
        )
