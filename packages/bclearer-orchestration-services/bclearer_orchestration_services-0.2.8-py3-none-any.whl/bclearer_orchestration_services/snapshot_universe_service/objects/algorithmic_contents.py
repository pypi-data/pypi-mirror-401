from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_domain_types import (
    BieDomainTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.object_contents import (
    ObjectContents,
)


class AlgorithmicContents(
    ObjectContents
):
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
