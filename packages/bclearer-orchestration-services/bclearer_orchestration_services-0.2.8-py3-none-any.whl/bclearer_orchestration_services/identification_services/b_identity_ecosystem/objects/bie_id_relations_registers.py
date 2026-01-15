from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.datastructure.bie_registries_registers_types import (
    BieRegistriesRegistersTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registers import (
    BieIdRegisters,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.register_helpers.bie_relation_if_valid_registerer import (
    register_bie_relation_if_valid,
)


class BieIdRelationsRegisters(
    BieIdRegisters
):
    def __init__(
        self, owning_bie_registry
    ):
        bie_register_type_enum = (
            BieRegistriesRegistersTypes.BIE_RELATIONS_REGISTER
        )

        bie_register_columns = [
            BieColumnNames.BIE_PLACE_1_IDS.b_enum_item_name,
            BieColumnNames.BIE_PLACE_2_IDS.b_enum_item_name,
            BieColumnNames.BIE_RELATION_TYPE_IDS.b_enum_item_name,
        ]

        super().__init__(
            bie_register_type_enum=bie_register_type_enum,
            bie_register_columns=bie_register_columns,
            owning_bie_registry=owning_bie_registry,
        )

    def register_bie_relation_if_valid(
        self,
        bie_place_1_id: BieIds,
        bie_place_2_id: BieIds,
        bie_relation_type_id: BieIds,
    ):
        register_bie_relation_if_valid(
            calling_bie_id_relations_register=self,
            bie_place_1_id=bie_place_1_id,
            bie_place_2_id=bie_place_2_id,
            bie_relation_type_id=bie_relation_type_id,
        )

    def is_bie_relation_already_registered(
        self,
        bie_relation_bie_id_list_signature_bie_id: BieIds,
    ):
        raise NotImplementedError()

    def register_bie_relation(
        self,
        bie_place_1_id: BieIds,
        bie_place_2_id: BieIds,
        bie_relation_type_id: BieIds,
        bie_relation_row_signature_bie_id: BieIds,
    ):
        raise NotImplementedError()

    def get_bie_relation_register_as_dataframe(
        self,
    ):
        raise NotImplementedError()

    # def __set_bie_register_dataframe(
    #         self) \
    #         -> DataFrame:
    #     register_dataframe = \
    #         DataFrame(
    #             columns=self.__bie_register_columns)
    #
    #     return \
    #         register_dataframe

    # def get_bie_register_dataframe(
    #         self) \
    #         -> DataFrame:
    #     return \
    #         self.__bie_register
    #
    # def get_refreshed_bie_register_summary_signature(
    #         self) \
    #         -> DataFrame:
    #     # TODO: need to add algorithm here
    #     refreshed_bie_register_summary_signature = \
    #         copy.deepcopy(
    #             self.__bie_register_simple_signature)
    #
    #     return \
    #         refreshed_bie_register_summary_signature
    #
    # def concatenate_dataframe(
    #         self,
    #         dataframe: DataFrame) \
    #         -> None:
    #     self.__bie_register = \
    #         pandas.concat(
    #             [
    #                 self.__bie_register,
    #                 dataframe
    #             ],
    #             ignore_index=True,
    #             axis=0)
    #
    # # TODO: double check this code is necessary - WARNING: NOW IT'S BEING USED
    # def replace_dataframe(
    #         self,
    #         dataframe: DataFrame) \
    #         -> None:
    #     self.__bie_register = \
    #         dataframe
    #
    # def drop_register_duplicates(
    #         self) \
    #         -> None:
    #     self.__bie_register.drop_duplicates(
    #         inplace=True)
