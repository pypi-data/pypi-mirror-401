from pathlib import Path

from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.extended_objects import (
    ExtendedObjects,
)


class RelativePaths(ExtendedObjects):
    def __init__(
        self,
        base_hr_name: str,
        relative_path: Path,
    ):
        self.relative_path_children = (
            set()
        )

        self.relative_path = (
            relative_path
        )

        bie_id = BieIdCreationFacade.create_bie_id_for_single_object(
            input_object=self.relative_path
        )

        super().__init__(
            bie_id=bie_id,
            base_hr_name=base_hr_name,
            bie_domain_type=BieFileSystemSnapshotDomainTypes.BIE_RELATIVE_PATHS,
        )

    def add_relative_path_child(
        self,
        relative_path_child: "RelativePaths",
    ):
        self.relative_path_children.add(
            relative_path_child
        )
