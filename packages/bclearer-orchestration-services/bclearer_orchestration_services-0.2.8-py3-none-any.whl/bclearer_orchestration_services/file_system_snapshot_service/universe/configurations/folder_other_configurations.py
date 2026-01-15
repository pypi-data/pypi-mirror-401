from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.enums.folder_prefixes import (
    FolderPrefix,
)


# TODO: workout better name
class FolderOtherConfigurations:
    # TODO: make prefix an Enum - in nf common - DONE
    B_APP_RUN_OUTPUT_SUB_FOLDER_PREFIX = (
        FolderPrefix.TO_BE_ADDED.b_enum_item_name
    )

    INPUT_IS_OPTIONALLY_MULTIPLE = True

    # TODO: workout better variable names for titles
    FSS_INPUTS_FOLDER_CONFIGURATION_TITLE = (
        "input root folder:"
    )

    # TODO: workout better variable names for titles
    B_APP_OUTPUT_WORKSPACE_CONFIGURATION_TITLE = (
        "bApp output workspace:"
    )
