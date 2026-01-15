from enum import auto

from bclearer_core.configurations.datastructure.b_enums import (
    BEnums,
)


class FileSystemSnapshotBieProfileComparisonExpectedResultTypes(
    BEnums
):
    IGNORE = auto()

    EQUAL = auto()

    DIFFERENT = auto()
