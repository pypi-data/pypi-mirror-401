from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.file_system_snapshot_bie_profile_comparison_expected_result_types import (
    FileSystemSnapshotBieProfileComparisonExpectedResultTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.comparers.first_and_second_root_folders_bie_profile_comparer_getter import (
    get_first_and_second_root_folders_bie_profile_comparer,
)
from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
    log_inspection_message,
)


# TODO: Use this to test if the profile and the comparer are giving us the right bie signature sums - they may be wrong
def is_root_folders_bie_comparison_result_expected(
    first_root_folder: Folders,
    second_root_folder: Folders,
    frn_signature_sum_comparison_expected_result: FileSystemSnapshotBieProfileComparisonExpectedResultTypes = FileSystemSnapshotBieProfileComparisonExpectedResultTypes.IGNORE,
    relative_path_signature_sum_comparison_expected_result: FileSystemSnapshotBieProfileComparisonExpectedResultTypes = FileSystemSnapshotBieProfileComparisonExpectedResultTypes.IGNORE,
    content_signature_sum_comparison_expected_result: FileSystemSnapshotBieProfileComparisonExpectedResultTypes = FileSystemSnapshotBieProfileComparisonExpectedResultTypes.IGNORE,
    optional_fssu_reporting_root_folder: (
        Folders | None
    ) = None,
) -> bool:
    first_and_second_root_folders_bie_profile_comparer = get_first_and_second_root_folders_bie_profile_comparer(
        first_root_folder=first_root_folder,
        second_root_folder=second_root_folder,
        optional_fssu_reporting_root_folder=optional_fssu_reporting_root_folder,
    )

    is_frn_comparison_result_expected = __is_specific_bie_signature_sum_comparison_result_expected(
        expected_result_type=frn_signature_sum_comparison_expected_result,
        is_specific_bie_signature_sum_comparison_equal=first_and_second_root_folders_bie_profile_comparer.is_container_signature_sum_file_reference_number_equal,
        comparison_type_name="SIGNATURE SUM BIE COMPARISON - FILE REFERENCE NUMBER",
    )

    is_relative_path_comparison_result_expected = __is_specific_bie_signature_sum_comparison_result_expected(
        expected_result_type=relative_path_signature_sum_comparison_expected_result,
        is_specific_bie_signature_sum_comparison_equal=first_and_second_root_folders_bie_profile_comparer.is_container_signature_sum_relative_path_equal,
        comparison_type_name="SIGNATURE SUM BIE COMPARISON - RELATIVE PATH",
    )

    is_content_comparison_result_expected = __is_specific_bie_signature_sum_comparison_result_expected(
        expected_result_type=content_signature_sum_comparison_expected_result,
        is_specific_bie_signature_sum_comparison_equal=first_and_second_root_folders_bie_profile_comparer.is_container_signature_sum_content_equal,
        comparison_type_name="SIGNATURE SUM BIE COMPARISON - FILE BYTE CONTENT",
    )

    return (
        is_frn_comparison_result_expected
        and is_relative_path_comparison_result_expected
        and is_content_comparison_result_expected
    )


def __is_specific_bie_signature_sum_comparison_result_expected(
    expected_result_type: FileSystemSnapshotBieProfileComparisonExpectedResultTypes,
    is_specific_bie_signature_sum_comparison_equal: bool,
    comparison_type_name: str,
) -> bool:
    match expected_result_type:
        case (
            FileSystemSnapshotBieProfileComparisonExpectedResultTypes.IGNORE
        ):
            if is_specific_bie_signature_sum_comparison_equal:
                log_inspection_message(
                    message=f"{comparison_type_name}\n - BIE IDS ARE EQUAL - COMPARISON IGNORED",
                    logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.INFO,
                )

                return True

            else:
                log_inspection_message(
                    message=f"{comparison_type_name}\n - BIE IDS ARE DIFFERENT - COMPARISON IGNORED",
                    logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.INFO,
                )

                return True

        case (
            FileSystemSnapshotBieProfileComparisonExpectedResultTypes.EQUAL
        ):
            if is_specific_bie_signature_sum_comparison_equal:
                log_inspection_message(
                    message=f"{comparison_type_name}\n - BIE IDS ARE EQUAL - THIS IS EXPECTED",
                    logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.INFO,
                )

                return True

            else:
                log_inspection_message(
                    message=f"{comparison_type_name}\n - BIE IDS ARE NOT EQUAL - THIS IS NOT EXPECTED",
                    logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.WARNING,
                )

                return False

        case (
            FileSystemSnapshotBieProfileComparisonExpectedResultTypes.DIFFERENT
        ):
            if (
                not is_specific_bie_signature_sum_comparison_equal
            ):
                log_inspection_message(
                    message=f"{comparison_type_name}\n - BIE IDS ARE DIFFERENT - THIS IS EXPECTED",
                    logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.INFO,
                )

                return True

            else:
                log_inspection_message(
                    message=f"{comparison_type_name}\n - BIE IDS ARE EQUAL - THIS IS NOT EXPECTED",
                    logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.WARNING,
                )

                return False

        case _:
            log_inspection_message(
                message=f"{comparison_type_name}\n - RESULT TYPE NOT SUPPORTED",
                logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.ERROR,
            )

            return False
