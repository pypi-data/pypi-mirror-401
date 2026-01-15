from bclearer_orchestration_services.snapshot_universe_service.objects.snapshots import (
    Snapshots,
)


class IndividualSnapshots(Snapshots):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
