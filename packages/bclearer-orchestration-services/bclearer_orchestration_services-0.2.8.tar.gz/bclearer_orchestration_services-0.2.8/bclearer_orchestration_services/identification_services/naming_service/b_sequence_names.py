import copy
from typing import List

from bclearer_core.configurations.bie_configurations.bie_configurations import (
    BieConfigurations,
)


class BSequenceNames:
    def __init__(
        self,
        initial_b_sequence_name_list: List[
            str
        ] = None,
    ):
        self.b_sequence_name_list: List[
            str
        ]

        if initial_b_sequence_name_list:
            self.b_sequence_name_list = initial_b_sequence_name_list

        else:
            self.b_sequence_name_list = (
                list()
            )

        self.b_sequence_name_list_delimiter = str(
            r"::"
        )

    def add_name_to_b_sequence_name_list(
        self, name: str
    ) -> None:
        self.b_sequence_name_list.append(
            name
        )

    def add_name_list_to_b_sequence_name_list(
        self,
        name_list_to_add: List[str],
    ) -> None:
        self.b_sequence_name_list += (
            name_list_to_add
        )

    def get_deep_copy(self):
        return copy.deepcopy(self)

    def get_b_sequence_name_display_string(
        self,
    ) -> str:
        # TODO: take out to helper file - get_b_sequence_name_display_string
        # # TODO: take out to helper file - get_truncated_bsequence_name_list
        truncation_level = (
            BieConfigurations.B_SEQUENCE_NAME_TRUNCATION_LEVEL
        )

        if truncation_level < 1:
            display_b_sequence_name_list = (
                self.b_sequence_name_list
            )

        else:
            display_b_sequence_name_list = self.b_sequence_name_list[
                -truncation_level:
            ]

        # # TODO: take out to helper file - remove_quotes
        b_sequence_name_no_quotes_list = (
            list()
        )

        for (
            b_sequence_name_item
        ) in (
            display_b_sequence_name_list
        ):
            if (
                '"'
                in b_sequence_name_item
            ):
                b_sequence_name_item = b_sequence_name_item.replace(
                    '"', str()
                )

            b_sequence_name_no_quotes_list.append(
                b_sequence_name_item
            )

        self.b_sequence_name_list = b_sequence_name_no_quotes_list

        display_string = self.b_sequence_name_list_delimiter.join(
            b_sequence_name_no_quotes_list
        )

        return display_string

    #
    # def __truncate_yourself(
    #         self) \
    #         -> None:
    #     truncation_level = \
    #         BieConfigurations.B_SEQUENCE_NAME_TRUNCATION_LEVEL
    #
    #     if truncation_level < 1:
    #         return
    #
    #     else:
    #         self.bsequence_name_list = \
    #             self.bsequence_name_list[-truncation_level:]
    #
    # # TODO: take out to helper file
    # def __strip_out_double_quotes_from_name_list(
    #         self) \
    #         -> None:
    #     b_sequence_name_no_quotes_list = \
    #         list()
    #
    #     for b_sequence_name_item \
    #             in self.bsequence_name_list:
    #         if '"' in b_sequence_name_item:
    #             b_sequence_name_item = \
    #                 b_sequence_name_item.replace(
    #                     '"',
    #                     str())
    #
    #         b_sequence_name_no_quotes_list.append(
    #             b_sequence_name_item)
    #
    #     self.bsequence_name_list = \
    #         b_sequence_name_no_quotes_list

    def __str__(self):
        return (
            self.get_b_sequence_name_display_string()
        )

    def __lt__(self, other):
        return str(self) < str(other)

    def __le__(self, other):
        return str(self) <= str(other)

    def __gt__(self, other):
        return str(self) > str(other)

    def __ge__(self, other):
        return str(self) >= str(other)

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return str(self) != str(other)
