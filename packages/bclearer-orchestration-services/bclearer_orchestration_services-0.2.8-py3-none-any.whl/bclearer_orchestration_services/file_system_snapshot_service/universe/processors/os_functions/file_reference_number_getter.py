from bclearer_core.infrastructure.session.common.enums.operating_system_kind import (
    OperatingSystemKind,
)
from bclearer_core.infrastructure.session.common.platform_type_getter import (
    get_operating_system_kind,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.os_functions.posix.posix_file_reference_number_getter import (
    get_posix_file_reference_number,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.processors.os_functions.windows.windows_file_reference_number_getter import (
    get_windows_file_reference_number,
)


def get_file_reference_number(
    file_path_as_string: str,
) -> int:
    operating_system_kind = (
        get_operating_system_kind()
    )

    file_reference_number = int()

    match operating_system_kind:
        case (
            OperatingSystemKind.WINDOWS
        ):
            file_reference_number = get_windows_file_reference_number(
                file_path_as_string
            )

        case (
            OperatingSystemKind.LINUX
            | OperatingSystemKind.MACOS
        ):
            file_reference_number = get_posix_file_reference_number(
                file_path_as_string
            )

        case _:
            raise NotImplementedError()

    return file_reference_number
