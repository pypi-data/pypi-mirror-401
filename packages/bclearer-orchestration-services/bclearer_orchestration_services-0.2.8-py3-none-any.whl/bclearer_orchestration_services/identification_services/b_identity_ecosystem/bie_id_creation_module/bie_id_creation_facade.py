from typing import List

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.common_knowledge.types.bie_vector_structure_types import (
    BieVectorStructureTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.general_objects.bie_id_from_type_and_vector_creator import (
    create_bie_id_from_type_and_vector,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


class BieIdCreationFacade:
    @staticmethod
    def create_empty_untyped_bie_id() -> (
        BieIds
    ):
        return (
            BieIdCreationFacade.__create_identity_element_bie_id()
        )

    @staticmethod
    def create_bie_id_for_single_object(
        input_object: object,
        bie_domain_type: BieEnums = None,
    ) -> BieIds:
        return create_bie_id_from_type_and_vector(
            input_objects_vector=[
                input_object
            ],
            bie_vector_structure_type=BieVectorStructureTypes.SINGLE_DIMENSIONAL,
            bie_domain_type=bie_domain_type,
        )

    @staticmethod
    def create_order_sensitive_bie_id_for_multiple_objects(
        input_objects: List[object],
        bie_domain_type: BieEnums = None,
    ) -> BieIds:
        return create_bie_id_from_type_and_vector(
            input_objects_vector=input_objects,
            bie_vector_structure_type=BieVectorStructureTypes.MULTI_DIMENSIONAL_ORDER_SENSITIVE,
            bie_domain_type=bie_domain_type,
        )

    @staticmethod
    def create_order_insensitive_bie_id_for_multiple_objects(
        input_objects: List[object],
        bie_domain_type: BieEnums = None,
    ) -> BieIds:
        return create_bie_id_from_type_and_vector(
            input_objects_vector=input_objects,
            bie_vector_structure_type=BieVectorStructureTypes.MULTI_DIMENSIONAL_ORDER_INSENSITIVE,
            bie_domain_type=bie_domain_type,
        )

    @staticmethod
    def __create_identity_element_bie_id() -> (
        BieIds
    ):
        return BieIds(int_value=0)
