from bclearer_core.bie.infrastructure.types.bie_common_column_names import (
    BieCommonColumnNames,
)
from bclearer_interop_services.b_dictionary_service.table_as_dictionary_service.table_as_dictionary_to_dataframe_converter import (
    convert_table_as_dictionary_to_dataframe,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.datastructure.column_names.bie_universe_column_names import (
    BieUniverseColumnNames,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.file_system_snapshot_universe_types import (
    FileSystemSnapshotUniverseTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universe_registries import (
    FileSystemSnapshotUniverseRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from pandas import DataFrame


def create_universes_table(
    file_system_snapshot_universe_registry: FileSystemSnapshotUniverseRegistries,
) -> DataFrame:
    table_as_dictionary = {}

    __add_universe_object_row(
        file_system_snapshot_universe_registry=file_system_snapshot_universe_registry,
        table_as_dictionary=table_as_dictionary,
    )

    table_as_dataframe = convert_table_as_dictionary_to_dataframe(
        table_as_dictionary=table_as_dictionary
    )

    return table_as_dataframe.astype(
        str
    )


def __add_universe_object_row(
    file_system_snapshot_universe_registry: FileSystemSnapshotUniverseRegistries,
    table_as_dictionary: dict,
) -> None:
    bie_id = (
        file_system_snapshot_universe_registry.owning_universe.bie_id
    )

    base_hr_name = (
        file_system_snapshot_universe_registry.owning_universe.base_hr_name
    )

    root_relative_path_bie_id = (
        file_system_snapshot_universe_registry.root_relative_path.bie_id
    )

    # TODO: add root_profile (FileSystemSnapshotContainerBieIdProfiles)
    app_run_session_bie_id = (
        file_system_snapshot_universe_registry.owning_universe.app_run_session_object.bie_id
    )

    universe_object_row = {
        BieColumnNames.BIE_IDS.b_enum_item_name: bie_id,
        BieCommonColumnNames.BASE_HR_NAMES.b_enum_item_name: base_hr_name,
        BieCommonColumnNames.BIE_INFRASTRUCTURE_TYPE_IDS.b_enum_item_name: FileSystemSnapshotUniverseTypes.FILE_SYSTEM_SNAPSHOT_UNIVERSE.item_bie_identity,
        BieUniverseColumnNames.BIE_ROOT_RELATIVE_PATH_IDS.b_enum_item_name: root_relative_path_bie_id,
        BieUniverseColumnNames.OWNING_BIE_APP_RUN_SESSION_IDS.b_enum_item_name: app_run_session_bie_id,
    }

    table_as_dictionary[
        len(table_as_dictionary)
    ] = universe_object_row
