from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_universes import (
    BieIdUniverses,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class BieFileSystemSnapshotUniverses(
    BieIdUniverses
):
    def __init__(
        self, bie_id: BieIds = None
    ) -> None:
        super().__init__(bie_id)
