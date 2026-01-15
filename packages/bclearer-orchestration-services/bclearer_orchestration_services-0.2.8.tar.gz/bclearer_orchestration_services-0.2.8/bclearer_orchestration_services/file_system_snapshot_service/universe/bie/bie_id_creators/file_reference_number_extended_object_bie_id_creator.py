from bclearer_core.infrastructure.session.operating_system.operating_system_objects import (
    OperatingSystemObjects,
)
from bclearer_interop_services.file_system_service.objects.file_system_objects import (
    FileSystemObjects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def create_file_reference_number_extended_object_bie_id(
    file_system_object: FileSystemObjects,
    file_reference_number: str,
) -> BieIds:
    operating_system_object = (
        OperatingSystemObjects()
    )

    input_objects = [
        BieFileSystemSnapshotDomainTypes.BIE_FILE_SYSTEM_SNAPSHOT_BASE_SYSTEM_BIE_IDS.item_bie_identity,
        operating_system_object.bie_id,
        file_system_object.drive,  # TODO: or get the device ID / hardware ID instead
        file_reference_number,
    ]

    file_system_snapshot_object_base_system_object_bie_id = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
        input_objects=input_objects
    )

    return file_system_snapshot_object_base_system_object_bie_id
