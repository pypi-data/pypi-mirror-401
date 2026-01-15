from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.file_byte_contents import (
    FileByteContents,
)


class FileFileByteContents(
    FileByteContents
):
    def __init__(self, file: Files):
        with open(
            file.absolute_path_string,
            mode="rb",
        ) as python_native_file:
            file_content_as_bytes = (
                python_native_file.read()
            )

        content_bie_id = BieIdCreationFacade.create_bie_id_for_single_object(
            input_object=file_content_as_bytes
        )

        if content_bie_id.is_empty:
            bie_id = content_bie_id

        else:
            bie_id = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
                input_objects=[
                    BieFileSystemSnapshotDomainTypes.BIE_FILE_BYTE_CONTENTS.item_bie_identity,
                    content_bie_id,
                ]
            )

        super().__init__(bie_id=bie_id)
