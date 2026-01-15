from bclearer_core.infrastructure.nf.objects.verses.nf_universes import (
    NfUniverses,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.registrations.bie_infrastructure_registries import (
    BieInfrastructureRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class BieIdUniverses(NfUniverses):
    def __init__(
        self, bie_id: BieIds = None
    ) -> None:
        super().__init__()

        self.bie_id = bie_id

        self.bie_infrastructure_registry = (
            BieInfrastructureRegistries()
        )
