from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.profiles.file_system_snapshot_container_bie_id_profiles import (
    FileSystemSnapshotContainerBieIdProfiles,
)


# TODO: 20251009 - pytest-fss OXi To be promoted to universe
class FileSystemSnapshotContainerBieIdProfileWrappers:
    def __init__(self):
        self.container_bie_id_profile: FileSystemSnapshotContainerBieIdProfiles = (None)

    def set_profile(
        self,
        container_bie_id_profile: FileSystemSnapshotContainerBieIdProfiles,
    ):
        self.container_bie_id_profile = (
            container_bie_id_profile
        )
