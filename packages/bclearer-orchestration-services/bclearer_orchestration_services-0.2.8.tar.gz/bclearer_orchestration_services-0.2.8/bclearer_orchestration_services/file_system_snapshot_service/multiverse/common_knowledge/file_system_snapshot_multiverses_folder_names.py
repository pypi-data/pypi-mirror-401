from enum import auto

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)


class FileSystemSnapshotMultiversesOutputFolderNames(
    BieEnums
):
    NOT_SET = auto()

    MULTI_FSSU = auto()

    FSS_SERVICE = auto()

    SINGLE_FSSU_RUNS = auto()

    FSSU_RUN = auto()
