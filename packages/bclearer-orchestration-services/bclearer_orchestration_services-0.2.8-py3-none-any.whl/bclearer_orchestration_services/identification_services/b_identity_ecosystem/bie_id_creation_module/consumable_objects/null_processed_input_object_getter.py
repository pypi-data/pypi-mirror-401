from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.configurations.bie_id_creation_configurations import (
    BieIdCreationConfigurations,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.consumable_objects.non_null_object_to_bie_consumable_object_item_converter import (
    _convert_non_null_object_to_bie_consumable_object_item,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.cell_is_string_based_null_value_checker import (
    check_cell_is_string_based_null_value,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.null_type_recognition import (
    NullTypeRecognition,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_null_value_types import (
    PandasNullValueTypes,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.string_based_null_type_recognition import (
    StringBasedNullTypeRecognition,
)


def _get_null_processed_input_object(
    input_object: object,
    cell_pandas_null_value_type: PandasNullValueTypes,
) -> str:
    if (
        BieIdCreationConfigurations.STRING_BASED_NULL_TYPE_RECOGNITION
        is StringBasedNullTypeRecognition.DO_NOT_RECOGNISE_STRING_BASED_NULL_AS_NULL
    ):
        cell_pandas_is_null_based_string = check_cell_is_string_based_null_value(
            cell=input_object
        )

        if cell_pandas_is_null_based_string:
            bie_consumable_object = _convert_non_null_object_to_bie_consumable_object_item(
                input_object=input_object
            )

            return bie_consumable_object

    bie_consumable_string = __get_bie_consumable_string(
        cell_pandas_null_value_type=cell_pandas_null_value_type
    )

    return bie_consumable_string


def __get_bie_consumable_string(
    cell_pandas_null_value_type: PandasNullValueTypes,
):
    null_conversion_prefix = (
        "<RECOGNISED AS NULL OBJECT>"
    )

    if (
        BieIdCreationConfigurations.NULL_TYPE_RECOGNITION
        is NullTypeRecognition.FINE_GRAINED
    ):
        return (
            null_conversion_prefix
            + str(
                cell_pandas_null_value_type
            )
        )

    else:
        return (
            null_conversion_prefix
            + str(
                NullTypeRecognition.COARSE_GRAINED_SINGLE_VALUE
            )
        )
