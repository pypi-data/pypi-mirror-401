from enum import auto

from bclearer_core.configurations.datastructure.b_enums import (
    BEnums,
)


class BieColumnNames(BEnums):
    NOT_SET = auto()

    BIE_IDS = auto()

    BIE_NAMES = auto()

    BIE_RELATION_TYPE_IDS = auto()

    BIE_PLACE_1_IDS = auto()

    BIE_PLACE_2_IDS = auto()

    BIE_RELATION_TYPE_NAMES = auto()

    SUM_VALUE_BIE_IDS = auto()
