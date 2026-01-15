from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.file_byte_contents import (
    FileByteContents,
)


class FolderFileByteContents(
    FileByteContents
):
    def __init__(self):
        super().__init__(
            bie_id=BieIds(int_value=0)
        )
