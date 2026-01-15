from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.consumable_objects.object_to_bie_consumable_object_item_converter import (
    convert_object_to_bie_consumable_object_item,
)


class BieConsumableObjects:
    def __init__(self) -> None:
        self.bie_consumable_object_list = (
            list()
        )

    def add_to_bie_consumable_object(
        self, input_object: object
    ) -> None:
        # TODO: Log info if not string (i.e. BieId)
        # TODO: check if bie_id or string - if not log warning
        bie_consumable_object_item = convert_object_to_bie_consumable_object_item(
            input_object=input_object
        )

        self.bie_consumable_object_list.append(
            bie_consumable_object_item
        )
