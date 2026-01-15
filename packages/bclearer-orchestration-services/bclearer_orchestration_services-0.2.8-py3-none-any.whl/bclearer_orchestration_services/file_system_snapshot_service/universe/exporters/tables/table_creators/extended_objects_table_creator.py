from bclearer_core.bie.infrastructure.types.bie_common_column_names import (
    BieCommonColumnNames,
)
from bclearer_core.configurations.bie_configurations.bie_id_configurations import (
    BieIdConfigurations,
)
from bclearer_interop_services.b_dictionary_service.table_as_dictionary_service.table_as_dictionary_to_dataframe_converter import (
    convert_table_as_dictionary_to_dataframe,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.datastructure.column_names.bie_extended_objects_column_names import (
    BieExtendedObjectsColumnNames,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.file_system_snapshot_objects import (
    FileSystemSnapshotObjects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_folders import (
    IndividualFileSystemSnapshotFolders,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universe_registries import (
    FileSystemSnapshotUniverseRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.extended_objects import (
    ExtendedObjects,
)
from pandas import DataFrame


def create_extended_objects_table(
    file_system_snapshot_universe_registry: FileSystemSnapshotUniverseRegistries,
) -> DataFrame:
    table_as_dictionary = {}
    root_snapshot = (
        file_system_snapshot_universe_registry.root_relative_path.snapshot
    )

    __add_file_system_snapshot_object_to_table(
        table_as_dictionary=table_as_dictionary,
        file_system_snapshot_object=root_snapshot,
    )

    table_as_dataframe = convert_table_as_dictionary_to_dataframe(
        table_as_dictionary=table_as_dictionary
    )

    return table_as_dataframe.astype(
        str
    )


def __add_file_system_snapshot_object_to_table(
    table_as_dictionary: dict,
    file_system_snapshot_object: FileSystemSnapshotObjects,
) -> None:
    __add_file_system_snapshot_extended_object_rows(
        table_as_dictionary=table_as_dictionary,
        file_system_snapshot_object=file_system_snapshot_object,
    )

    if isinstance(
        file_system_snapshot_object,
        IndividualFileSystemSnapshotFolders,
    ):
        for (
            snapshot_part
        ) in (
            file_system_snapshot_object.parts
        ):
            __add_file_system_snapshot_object_to_table(
                table_as_dictionary=table_as_dictionary,
                file_system_snapshot_object=snapshot_part,
            )


def __add_file_system_snapshot_extended_object_rows(
    table_as_dictionary: dict,
    file_system_snapshot_object: FileSystemSnapshotObjects,
) -> None:
    for (
        extended_object_type,
        extended_object,
    ) in (
        file_system_snapshot_object.extended_objects.items()
    ):
        __add_extended_object_row(
            table_as_dictionary=table_as_dictionary,
            extended_object=extended_object,
        )


def __add_extended_object_row(
    table_as_dictionary: dict,
    extended_object: ExtendedObjects,
) -> None:
    extended_object_row = {
        BieColumnNames.BIE_IDS.b_enum_item_name: extended_object.bie_id,
        BieCommonColumnNames.BASE_HR_NAMES.b_enum_item_name: extended_object.base_hr_name,
        BieCommonColumnNames.BIE_DOMAIN_TYPE_IDS.b_enum_item_name: extended_object.bie_type.item_bie_identity,
        BieExtendedObjectsColumnNames.OWNING_BIE_SNAPSHOT_IDS.b_enum_item_name: extended_object.snapshot.bie_id,
    }

    if (
        BieIdConfigurations.EXPORT_INT_VALUE_COLUMNS
    ):
        extended_object_row.update(
            {
                BieExtendedObjectsColumnNames.EXTENDED_OBJECT_BIE_ID_INT_VALUES.b_enum_item_name: extended_object.bie_id.int_value
            }
        )

    table_as_dictionary[
        len(table_as_dictionary)
    ] = extended_object_row
