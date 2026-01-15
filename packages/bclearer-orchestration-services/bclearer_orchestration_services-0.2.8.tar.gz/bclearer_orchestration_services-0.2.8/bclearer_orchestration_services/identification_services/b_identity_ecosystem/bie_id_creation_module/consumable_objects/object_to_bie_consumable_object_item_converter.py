from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.consumable_objects.non_null_object_to_bie_consumable_object_item_converter import (
    _convert_non_null_object_to_bie_consumable_object_item,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.consumable_objects.null_processed_input_object_getter import (
    _get_null_processed_input_object,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.cell_pandas_null_value_type_getter import (
    get_cell_pandas_null_value_type,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.pandas_null_value_types import (
    PandasNullValueTypes,
)


def _convert_object_to_bie_consumable_object_item(
    input_object: object,
) -> object:
    if isinstance(input_object, BieIds):
        return input_object

    cell_pandas_null_value_type = (
        get_cell_pandas_null_value_type(
            cell=input_object
        )
    )

    if (
        cell_pandas_null_value_type
        == PandasNullValueTypes.NOT_SET
    ):
        return _convert_non_null_object_to_bie_consumable_object_item(
            input_object=input_object
        )

    null_processed_input_object = _get_null_processed_input_object(
        input_object=input_object,
        cell_pandas_null_value_type=cell_pandas_null_value_type,
    )

    return null_processed_input_object


def convert_object_to_bie_consumable_object_item(
    input_object: object,
) -> object:
    # Public wrapper
    return _convert_object_to_bie_consumable_object_item(
        input_object
    )
