from typing import Dict

from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.populators.bie_signatures.file_system_snapshot_object_to_root_bie_signature_registry_adder import (
    add_file_system_snapshot_object_to_root_bie_signature_registry,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_signatures import (
    BieSignatures,
)


# TODO: Is this actually a Register?
class RootRelativePathBieSignatureRegistries:
    def __init__(self) -> None:
        self.file_system_snapshot_object_bie_id_signatures: Dict[
            BieFileSystemSnapshotDomainTypes,
            BieSignatures,
        ] = dict()

    def add_file_system_snapshot_object_to_registry(
        self,
        file_system_snapshot_object: "FileSystemSnapshotObjects",
    ) -> None:
        from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.file_system_snapshot_objects import (
            FileSystemSnapshotObjects,
        )

        if not isinstance(
            file_system_snapshot_object,
            FileSystemSnapshotObjects,
        ):
            raise TypeError

        add_file_system_snapshot_object_to_root_bie_signature_registry(
            root_bie_signature_registry=self,
            file_system_snapshot_object=file_system_snapshot_object,
        )

    def add_bie_id_to_signature_by_type(
        self,
        bie_id: BieIds,
        bie_id_type: BieFileSystemSnapshotDomainTypes,
    ) -> None:
        if (
            bie_id_type
            not in self.file_system_snapshot_object_bie_id_signatures
        ):
            self.file_system_snapshot_object_bie_id_signatures[
                bie_id_type
            ] = BieSignatures()

        bie_cell_source_value_type_signature: (
            BieSignatures
        ) = self.file_system_snapshot_object_bie_id_signatures[
            bie_id_type
        ]

        bie_cell_source_value_type_signature.add_bie_id(
            bie_id
        )
