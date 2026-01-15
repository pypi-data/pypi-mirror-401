from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universe_registries import (
    FileSystemSnapshotUniverseRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.datastructure.bie_registries_registers_types import (
    BieRegistriesRegistersTypes,
)


# TODO: it should be passing the bie infrastructure registry rather than something domain-specific.
#  Then, move this up to the BieUniverses area b_identity_ecosystem
def create_parallel_bie_dataframes_dictionary(
    file_system_snapshot_universe_registry: FileSystemSnapshotUniverseRegistries,
) -> dict:
    bie_objects_register = file_system_snapshot_universe_registry.owning_universe.parallel_bie_universe.bie_infrastructure_registry.get_bie_register(
        bie_register_type_enum=BieRegistriesRegistersTypes.BIE_OBJECTS_REGISTER
    )

    bie_objects_dataframe = bie_objects_register.get_bie_register_dataframe().astype(
        str
    )

    bie_relations_dataframe = file_system_snapshot_universe_registry.owning_universe.parallel_bie_universe.bie_infrastructure_registry.get_bie_relation_register_as_dataframe().astype(
        str
    )

    bie_dataframes_dictionary = {
        BieRegistriesRegistersTypes.BIE_OBJECTS_REGISTER.b_enum_item_name: bie_objects_dataframe,
        BieRegistriesRegistersTypes.BIE_RELATIONS_REGISTER.b_enum_item_name: bie_relations_dataframe,
    }

    return bie_dataframes_dictionary
