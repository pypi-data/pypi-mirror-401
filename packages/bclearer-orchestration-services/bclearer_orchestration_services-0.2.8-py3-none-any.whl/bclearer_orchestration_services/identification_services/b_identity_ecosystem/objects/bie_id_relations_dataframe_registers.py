import copy

import pandas
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_relations_registers import (
    BieIdRelationsRegisters,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.register_helpers.dataframe.bie_relation_already_registered_in_dataframe_checker import (
    is_bie_relation_already_registered_in_dataframe,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.register_helpers.dataframe.dataframe_bie_relation_registerer import (
    register_dataframe_bie_relation,
)
from pandas import DataFrame


class BieIdRelationsDataframeRegisters(
    BieIdRelationsRegisters
):
    def __init__(
        self, owning_bie_registry
    ):
        super().__init__(
            owning_bie_registry=owning_bie_registry
        )

        self.__bie_id_relations_register_as_dataframe = (
            self.__set_bie_register_dataframe()
        )

    def is_bie_relation_already_registered(
        self,
        bie_relation_bie_id_list_signature_bie_id: BieIds,
    ) -> bool:
        return is_bie_relation_already_registered_in_dataframe(
            calling_bie_id_relations_register=self,
            new_bie_relation_bie_id_list_signature_bie_id=bie_relation_bie_id_list_signature_bie_id,
        )

    def register_bie_relation(
        self,
        bie_place_1_id: BieIds,
        bie_place_2_id: BieIds,
        bie_relation_type_id: BieIds,
        bie_relation_row_signature_bie_id: BieIds,
    ) -> None:
        register_dataframe_bie_relation(
            calling_bie_id_relations_register=self,
            bie_place_1_id=bie_place_1_id,
            bie_place_2_id=bie_place_2_id,
            bie_relation_type_id=bie_relation_type_id,
            bie_relation_row_signature_bie_id=bie_relation_row_signature_bie_id,
        )

    def get_bie_relation_register_as_dataframe(
        self,
    ) -> DataFrame:
        return (
            self.__bie_id_relations_register_as_dataframe
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
            ignore_index=True,
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
