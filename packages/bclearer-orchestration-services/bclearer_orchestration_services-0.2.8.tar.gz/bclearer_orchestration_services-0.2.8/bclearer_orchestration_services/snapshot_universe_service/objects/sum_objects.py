from bclearer_core.bie.domain.bie_domain_objects import (
    BieDomainObjects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_domain_types import (
    BieDomainTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.snapshot_universe_service.common_knowledge.snapshot_domain_literals import (
    SnapshotDomainLiterals,
)


class SumObjects(BieDomainObjects):
    def __init__(
        self,
        bie_id: BieIds,
        direction_type: BieDomainTypes,
        bie_summed_type: BieDomainTypes,
    ):
        super().__init__(
            bie_id=bie_id,
            base_hr_name=SnapshotDomainLiterals.sum_object,
            bie_domain_type=BieFileSystemSnapshotDomainTypes.SUM_OBJECTS,
        )

        self.direction_type = (
            direction_type
        )

        self.bie_summed_type = (
            bie_summed_type
        )
