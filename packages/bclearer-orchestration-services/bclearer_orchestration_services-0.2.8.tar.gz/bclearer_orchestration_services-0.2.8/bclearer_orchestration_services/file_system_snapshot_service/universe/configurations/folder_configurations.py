from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.enums.folder_prefixes import (
    FolderPrefix,
)


# TODO: Move to nf_common - DONE
class FolderConfigurations:
    def __init__(
        self,
        title: str,
        optionally_multiple: bool = False,
    ):
        self.title = title

        self.optionally_multiple = (
            optionally_multiple
        )

        self.folder_list = list()

        # TODO: String should be changed to an Enum
        self.app_run_output_folder_prefix = (
            FolderPrefix.TO_BE_ADDED.b_enum_item_name
        )

    def add_folder_to_folder_list(
        self, input_folder: Folders
    ):
        self.folder_list.append(
            input_folder
        )
