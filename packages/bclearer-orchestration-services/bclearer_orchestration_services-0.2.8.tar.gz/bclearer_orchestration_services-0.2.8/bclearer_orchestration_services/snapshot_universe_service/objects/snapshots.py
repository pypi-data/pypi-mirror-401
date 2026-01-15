from typing import Dict

from bclearer_core.bie.domain.bie_domain_objects import (
    BieDomainObjects,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_domain_types import (
    BieDomainTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.extended_objects import (
    ExtendedObjects,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.sum_objects import (
    SumObjects,
)


class Snapshots(BieDomainObjects):
    def __init__(
        self,
        bie_id: BieIds,
        base_hr_name: str,
        bie_domain_type: BieDomainTypes,
    ):
        super().__init__(
            bie_id=bie_id,
            base_hr_name=base_hr_name,
            bie_domain_type=bie_domain_type,
        )

        self.parts = set()

        self.wholes = set()

        self.extended_objects: Dict[
            BieDomainTypes,
            ExtendedObjects,
        ] = {}

        self.inclusive_ancestor_sum_objects: Dict[
            BieDomainTypes, SumObjects
        ] = {}

        self.inclusive_descendant_sum_objects: Dict[
            BieDomainTypes, SumObjects
        ] = {}

        self.exclusive_ancestor_sum_objects: Dict[
            BieDomainTypes, SumObjects
        ] = {}

        self.exclusive_descendant_sum_objects: Dict[
            BieDomainTypes, SumObjects
        ] = {}

    def add_extended_object(
        self,
        extended_object: ExtendedObjects,
    ) -> None:
        self.extended_objects[
            extended_object.bie_type
        ] = extended_object

        extended_object.set_snapshot(
            snapshot=self
        )

    def get_children_count(self) -> int:
        return len(self.parts)
