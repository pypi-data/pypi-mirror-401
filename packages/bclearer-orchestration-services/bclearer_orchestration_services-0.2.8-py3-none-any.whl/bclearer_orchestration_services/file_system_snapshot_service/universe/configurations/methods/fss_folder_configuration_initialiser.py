from bclearer_orchestration_services.file_system_snapshot_service.universe.configurations.folder_configurations import (
    FolderConfigurations,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.configurations.folder_other_configurations import (
    FolderOtherConfigurations,
)


# TODO: move to nf common - DONE
# TODO: remove ui from name
def initialise_fss_folder_configuration() -> (
    FolderConfigurations
):
    # TODO: FolderConfigurations should have a file_system_objects list, rather than a folders list - change in
    #  nf_common_ui branch
    # TODO: workout better names for titles
    fss_inputs_folder_configuration_title = (
        FolderOtherConfigurations.FSS_INPUTS_FOLDER_CONFIGURATION_TITLE
    )

    fss_inputs_folder_configuration = FolderConfigurations(
        title=fss_inputs_folder_configuration_title,
        optionally_multiple=FolderOtherConfigurations.INPUT_IS_OPTIONALLY_MULTIPLE,
    )

    return (
        fss_inputs_folder_configuration
    )
