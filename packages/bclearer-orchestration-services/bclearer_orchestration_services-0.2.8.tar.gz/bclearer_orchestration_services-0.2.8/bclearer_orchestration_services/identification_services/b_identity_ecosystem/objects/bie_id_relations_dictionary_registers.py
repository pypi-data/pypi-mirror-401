import copy
from typing import Dict

import pandas
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_relations_registers import (
    BieIdRelationsRegisters,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from pandas import DataFrame


class BieIdRelationsDictionaryRegisters(
    BieIdRelationsRegisters
):
    def __init__(
        self, owning_bie_registry
    ):
        super().__init__(
            owning_bie_registry=owning_bie_registry
        )

        # initialise empty storage structures
        self.__bie_register_dictionary: Dict[
            int, Dict[str, BieIds]
        ] = dict()

        # dataframe placeholder to avoid creating attribute outside __init__
        self.__bie_register = (
            pandas.DataFrame()
        )

    @staticmethod
    def __set_bie_register_dictionary() -> (
        dict
    ):
        # returns an empty dictionary registry
        return dict()

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
        self.__bie_register = (
            pandas.concat(
                [
                    self.__bie_register,
                    dataframe,
                ],
                ignore_index=True,
                axis=0,
            )
        )

    # TODO: double check this code is necessary - WARNING: NOW IT'S BEING USED
    def replace_dataframe(
        self, dataframe: DataFrame
    ) -> None:
        self.__bie_register = dataframe

    def drop_register_duplicates(
        self,
    ) -> None:
        self.__bie_register.drop_duplicates(
            inplace=True
        )
