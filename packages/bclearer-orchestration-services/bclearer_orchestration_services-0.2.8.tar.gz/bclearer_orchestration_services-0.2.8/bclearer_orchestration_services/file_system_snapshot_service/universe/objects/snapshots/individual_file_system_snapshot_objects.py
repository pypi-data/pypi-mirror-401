from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.path_properties import (
    PathProperties,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.bie.bie_id_creators.file_system_snapshot_object_bie_id_creator import (
    create_file_system_snapshot_object_bie_id,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.extended.file_reference_numbers import (
    FileReferenceNumbers,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.extended.relative_paths import (
    RelativePaths,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.file_system_snapshot_objects import (
    FileSystemSnapshotObjects,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.object_contents import (
    ObjectContents,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.snapshot_domains import (
    SnapshotDomains,
)


class IndividualFileSystemSnapshotObjects(
    FileSystemSnapshotObjects
):
    def __init__(
        self,
        bie_domain_type: BieFileSystemSnapshotDomainTypes,
        file_system_object: FileSystemObjects,
        owning_snapshot_domain: SnapshotDomains,
        relative_path: RelativePaths,
        object_content: ObjectContents,
    ):
        self._file_system_object = (
            file_system_object
        )

        file_reference_number = FileReferenceNumbers(
            file_system_object=self._file_system_object
        )

        bie_id = create_file_system_snapshot_object_bie_id(
            base_system_object_bie_id=file_reference_number.bie_id,
            owning_snapshot_domain=owning_snapshot_domain,
        )

        if (
            file_system_object.absolute_path.exists()
        ):
            self.file_system_object_properties = PathProperties(
                input_file_system_object_path=file_system_object.absolute_path_string
            )

        super().__init__(
            bie_id=bie_id,
            base_hr_name=file_system_object.base_name,
            bie_domain_type=bie_domain_type,
            owning_snapshot_domain=owning_snapshot_domain,
            relative_path=relative_path,
            file_reference_number=file_reference_number,
            object_content=object_content,
        )

    def get_file_system_object(
        self,
    ) -> FileSystemObjects:
        return self._file_system_object
