# from enum import Enum
# from typing import Dict
# from typing import Iterator
# from typing import Tuple
# from bclearer_orchestration_services.file_system_snapshot_service.universe.configurations.folder_configurations import FolderConfigurations
#
#
# # TODO: Move to nf_common - DONE
# class FolderConfigurationsKeyedCollections:
#     def __init__(
#             self):
#         # TODO: double check the keys are always going to be Enums (or subtypes of Enums)
#         self.__typed_dictionary: Dict[Enum, FolderConfigurations] = \
#             {}
#
#     def add_folder_configuration_to_keyed_collection(
#             self,
#             folder_configuration_key: Enum,
#             folder_configuration: FolderConfigurations):
#         self.__typed_dictionary[folder_configuration_key] = \
#             folder_configuration
#
#         # TODO: Need to error-check the above (key overwriting)
#
#     def items(
#             self) \
#             -> Iterator[Tuple[Enum, FolderConfigurations]]:
#         return \
#             iter(
#                 self.__typed_dictionary.items())
#
#     # TODO: Add get folder configuration by key - DONE
#     def get_folder_configuration_by_key(
#             self,
#             folder_configuration_key: Enum) \
#             -> FolderConfigurations:
#         return \
#             self.__typed_dictionary[folder_configuration_key]
