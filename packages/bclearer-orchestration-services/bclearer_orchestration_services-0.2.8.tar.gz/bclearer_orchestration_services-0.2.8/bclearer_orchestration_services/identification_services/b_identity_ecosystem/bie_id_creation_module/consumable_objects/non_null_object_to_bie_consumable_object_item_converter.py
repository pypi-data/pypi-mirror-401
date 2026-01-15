from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.configurations.bie_id_creation_configurations import (
    BieIdCreationConfigurations,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.data_type_recognition import (
    DataTypeRecognition,
)


def _convert_non_null_object_to_bie_consumable_object_item(
    input_object: object,
) -> str:
    object_type = type(input_object)

    input_object_as_string = str(
        input_object
    )

    match BieIdCreationConfigurations.DATA_TYPE_RECOGNITION:
        case (
            DataTypeRecognition.DO_NOT_INCLUDE_DATA_TYPES_IN_BIE_CALCULATION
        ):
            return (
                input_object_as_string
            )

        case (
            DataTypeRecognition.INCLUDE_DATA_TYPES_IN_BIE_CALCULATION
        ):
            object_as_concatenated_type_and_content_string = (
                str(object_type)
                + input_object_as_string
            )

            return object_as_concatenated_type_and_content_string

        case _:
            raise NotImplementedError()
