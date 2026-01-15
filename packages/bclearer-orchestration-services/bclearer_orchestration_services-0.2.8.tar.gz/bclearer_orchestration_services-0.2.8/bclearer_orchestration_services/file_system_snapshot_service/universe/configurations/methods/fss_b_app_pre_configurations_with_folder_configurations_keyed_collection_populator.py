# from bclearer_core.configurations.b_configurations.b_app_pre_configurations import BAppPreConfigurations
# from bclearer_orchestration_services.file_system_snapshot_service.universe.configurations.folder_configurations import FolderConfigurations
#
#
# def populate_fss_b_app_pre_configurations_with_fss_folder_configuration(
#         folder_configuration: FolderConfigurations) \
#         -> None:
#     BAppPreConfigurations.INPUT_ROOT_FILE_SYSTEM_OBJECTS = \
#         folder_configuration.folder_list
#
#     # outputs_folder_configuration = \
#     #     folder_configurations_keyed_collection.get_folder_configuration_by_key(
#     #             folder_configuration_key=FssFolderConfigurationTypes.OUTPUTS)
#     #
#     # # TODO: to add conditional here? no more than one folder?
#     # BAppPreConfigurations.B_APP_OUTPUT_WORKSPACE = \
#     #     outputs_folder_configuration.folder_list[0]
#     #
#     # BAppPreConfigurations.B_APP_RUN_OUTPUT_SUB_FOLDER_PREFIX = \
#     #     FolderOtherConfigurations.B_APP_RUN_OUTPUT_SUB_FOLDER_PREFIX
