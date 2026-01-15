from abc import ABC, abstractmethod

from bclearer_core.bie.top.bie_objects import (
    BieObjects,
)
from bclearer_core.infrastructure.nf.objects.registries.nf_universe_registries import (
    NfUniverseRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_column_names import (
    BieColumnNames,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_core_relation_types import (
    BieCoreRelationTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.datastructure.bie_registry_registers_columns_dictionary import (
    BIE_REGISTRY_REGISTERS_COLUMNS_DICTIONARY,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registers import (
    BieIdRegisters,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_relations_dataframe_registers import (
    BieIdRelationsDataframeRegisters,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_relations_registers import (
    BieIdRelationsRegisters,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.register_helpers.bie_type_instance_relation_registerer import (
    register_bie_type_instance_relation,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.registers_factory.bie_registry_register_factories import (
    BieRegistryRegisterFactories,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.registrations.helpers.bclearer_processing.type_instances_in_bie_registry_registerer import (
    register_type_instances_in_bie_registry,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.registrations.helpers.checkers.bie_registry_for_type_instances_registration_checker import (
    check_bie_registry_for_type_instances_registration,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.registrations.helpers.pascal_case_to_words_converter import (
    convert_pascal_case_to_words,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.registrations.helpers.registerers.bie_id_registerer import (
    register_bie_id,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.registrations.helpers.registerers.objects_in_bie_registry_registerer import (
    register_objects_in_bie_registry,
)
from bclearer_orchestration_services.identification_services.naming_service.b_sequence_names import (
    BSequenceNames,
)
from pandas import DataFrame


class BieIdRegistries(
    ABC, NfUniverseRegistries
):
    def __init__(self) -> None:
        super().__init__()

        self.__register_dictionary: (
            dict[
                BieEnums, BieIdRegisters
            ]
        ) = (dict())

        self.__bie_relations_register: (
            BieIdRelationsRegisters
        ) = BieIdRelationsDataframeRegisters(
            owning_bie_registry=self
        )

        self.bie_registry_name = convert_pascal_case_to_words(
            type(self).__name__
        )

        bie_registry_register_factory = BieRegistryRegisterFactories(
            register_column_names_dictionary=BIE_REGISTRY_REGISTERS_COLUMNS_DICTIONARY,
            bie_registry=self,
        )

        bie_registry_register_factory.create_bie_registry_registers()

    def get_registers_dictionary(self):
        return (
            self.__register_dictionary
        )

    def update_register_dictionary(
        self, dictionary_update: dict
    ):
        # TODO: concatenate two dicts, check for duplicated keys
        self.__register_dictionary = (
            self.__register_dictionary
            | dictionary_update
        )

    def bie_register_exists(
        self,
        bie_register_type_enum: BieEnums,
    ) -> bool:
        return (
            bie_register_type_enum
            in self.__register_dictionary
        )

    def get_bie_register(
        self,
        bie_register_type_enum: BieEnums,
    ) -> BieIdRegisters:
        return (
            self.__register_dictionary[
                bie_register_type_enum
            ]
        )

    def concatenate_register_dataframe(
        self,
        bie_register_type_enum: BieEnums,
        dataframe: DataFrame,
    ) -> None:
        bie_register = (
            self.__register_dictionary[
                bie_register_type_enum
            ]
        )

        bie_register.concatenate_dataframe(
            dataframe=dataframe
        )

    def register_bie_id_if_required(
        self,
        bie_item_id: BieIds,
        bie_sequence_name: BSequenceNames,
        bie_id_type_id: BieIds,
        is_preferred_b_sequence_name: bool = False,
    ) -> None:
        bie_id_targeted_register = self._get_appropriate_targeted_id_register(
            bie_id_type_id=bie_id_type_id
        )

        bie_id_register_dataframe = (
            bie_id_targeted_register.get_bie_register_dataframe()
        )

        registered_bie_ids = bie_id_register_dataframe[
            BieColumnNames.BIE_IDS.b_enum_item_name
        ].values

        if (
            bie_item_id
            in registered_bie_ids
        ):
            return

        register_bie_id(
            bie_id_register=bie_id_targeted_register,
            bie_item_id=bie_item_id,
            b_sequence_name=bie_sequence_name,
            is_preferred_b_sequence_name=is_preferred_b_sequence_name,
            bie_id_type_id=bie_id_type_id,
        )

    def register_bie_id_and_type_instance(
        self,
        bie_item_id: BieIds,
        bie_sequence_name: BSequenceNames,
        bie_id_type_id: BieIds,
        is_preferred_b_sequence_name: bool = False,
    ) -> None:
        bie_id_targeted_register = self._get_appropriate_targeted_id_register(
            bie_id_type_id=bie_id_type_id
        )

        register_bie_id(
            bie_id_register=bie_id_targeted_register,
            bie_item_id=bie_item_id,
            b_sequence_name=bie_sequence_name,
            is_preferred_b_sequence_name=is_preferred_b_sequence_name,
            bie_id_type_id=bie_id_type_id,
        )

        register_bie_type_instance_relation(
            bie_place_1_id=bie_item_id,
            bie_place_2_id=bie_id_type_id,
            calling_bie_id_relations_register=self.__bie_relations_register,
        )

    def register_bie_object_and_type_instance(
        self, bie_object: BieObjects
    ) -> None:
        bie_sequence_name = BSequenceNames(
            initial_b_sequence_name_list=[
                bie_object.base_hr_name
            ]
        )

        self.register_bie_id_and_type_instance(
            bie_item_id=bie_object.bie_id,
            bie_sequence_name=bie_sequence_name,
            bie_id_type_id=bie_object.bie_type.item_bie_identity,
        )

    def register_bie_whole_part_in_bie_infrastructure_registry(
        self,
        bie_object_whole: BieObjects,
        bie_object_part: BieObjects,
    ) -> None:
        self.register_bie_relation(
            bie_place_1_id=bie_object_part.bie_id,
            bie_place_2_id=bie_object_whole.bie_id,
            bie_relation_type_id=BieCoreRelationTypes.BIE_WHOLES_PARTS.item_bie_identity,
        )

    def register_bie_id_type_instance(
        self,
        bie_type_id: BieIds,
        bie_instance_id: BieIds,
    ) -> None:
        register_bie_type_instance_relation(
            bie_place_1_id=bie_instance_id,
            bie_place_2_id=bie_type_id,
            calling_bie_id_relations_register=self.__bie_relations_register,
        )

    def register_bie_relation(
        self,
        bie_place_1_id: BieIds,
        bie_place_2_id: BieIds,
        bie_relation_type_id: BieIds,
    ) -> None:
        self.__bie_relations_register.register_bie_relation_if_valid(
            bie_place_1_id=bie_place_1_id,
            bie_place_2_id=bie_place_2_id,
            bie_relation_type_id=bie_relation_type_id,
        )

    def get_bie_relation_register_as_dataframe(
        self,
    ) -> DataFrame:
        return (
            self.__bie_relations_register.get_bie_relation_register_as_dataframe()
        )

    @abstractmethod
    def _get_appropriate_targeted_id_register(
        self, bie_id_type_id: BieIds
    ):
        raise (NotImplemented())

    @abstractmethod
    def _get_appropriate_targeted_relations_register(
        self,
    ):
        raise (NotImplemented())

    def register_objects(
        self,
        not_yet_registered_objects: DataFrame,
    ) -> None:
        register_objects_in_bie_registry(
            bie_registry=self,
            not_yet_registered_objects=not_yet_registered_objects,
        )

    def check_type_instances_registration(
        self, type_instances: DataFrame
    ) -> dict:
        return check_bie_registry_for_type_instances_registration(
            bie_registry=self,
            type_instances=type_instances,
        )

    def register_type_instances(
        self,
        not_yet_registered_type_instances: DataFrame,
    ) -> None:
        bie_relations_register = (
            self._get_appropriate_targeted_relations_register()
        )

        register_type_instances_in_bie_registry(
            bie_registry=self,
            bie_relations_register=bie_relations_register,
            not_yet_registered_type_instances=not_yet_registered_type_instances,
        )
