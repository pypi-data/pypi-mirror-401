import copy
from typing import List

import pandas
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)
from pandas import DataFrame


class BieIdRegisters:
    def __init__(
        self,
        bie_register_type_enum: BieEnums,
        bie_register_columns: List[
            BieEnums
        ],
        owning_bie_registry,
    ) -> None:
        self.bie_register_type_enum = (
            bie_register_type_enum
        )

        self.bie_register_columns = (
            bie_register_columns
        )

        self.__bie_id_relations_register_as_dataframe = (
            self.__set_bie_register_dataframe()
        )

        self.__bie_register_simple_signature = (
            DataFrame()
        )

        self.__bie_register_column_signature = (
            DataFrame()
        )

        self.__bie_register_row_signature = (
            DataFrame()
        )

        self.owning_bie_registry = (
            owning_bie_registry
        )

    def __set_bie_register_dataframe(
        self,
    ) -> DataFrame:
        register_dataframe = DataFrame(
            columns=self.bie_register_columns
        )

        return register_dataframe

    def get_bie_register_dataframe(
        self,
    ) -> DataFrame:
        return (
            self.__bie_id_relations_register_as_dataframe
        )

    def get_refreshed_bie_register_summary_signature(
        self,
    ) -> DataFrame:
        # TODO: need to add algorithm here
        refreshed_bie_register_summary_signature = copy.deepcopy(
            self.__bie_register_simple_signature
        )

        return refreshed_bie_register_summary_signature

    def concatenate_dataframe(
        self, dataframe: DataFrame
    ) -> None:
        self.__bie_id_relations_register_as_dataframe = pandas.concat(
            [
                self.__bie_id_relations_register_as_dataframe,
                dataframe,
            ],
            ignore_index=False,
            axis=0,
        )

    # TODO: double check this code is necessary - WARNING: NOW IT'S BEING USED
    def replace_dataframe(
        self, dataframe: DataFrame
    ) -> None:
        self.__bie_id_relations_register_as_dataframe = (
            dataframe
        )

    def drop_register_duplicates(
        self,
    ) -> None:
        self.__bie_id_relations_register_as_dataframe.drop_duplicates(
            inplace=True
        )
