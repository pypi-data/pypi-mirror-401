from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_enums import (
    BieEnums,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registers import (
    BieIdRegisters,
)
from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
    log_inspection_message,
)


class BieRegistryRegisterFactories:
    def __init__(
        self,
        register_column_names_dictionary: dict,
        bie_registry,
    ) -> None:
        self.__register_column_names_dictionary = register_column_names_dictionary

        self.bie_registry = bie_registry

    def create_bie_registry_registers(
        self,
    ) -> None:
        message = "Creating registers for registry: {}".format(
            self.bie_registry.bie_registry_name
        )

        log_inspection_message(
            message=message,
            logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.VERBOSE,
        )

        for (
            bie_register_type_enum
        ) in (
            self.__register_column_names_dictionary.keys()
        ):
            self.create_bie_registry_register(
                bie_register_type_enum=bie_register_type_enum
            )

    def create_bie_registry_register(
        self,
        bie_register_type_enum: BieEnums,
    ) -> BieIdRegisters:
        message = "Creating register: {}".format(
            bie_register_type_enum.b_enum_item_name
        )

        log_inspection_message(
            message=message,
            logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.VERBOSE,
        )

        bie_register_columns = self.__register_column_names_dictionary[
            bie_register_type_enum
        ]

        bie_register = BieIdRegisters(
            bie_register_type_enum=bie_register_type_enum,
            bie_register_columns=bie_register_columns,
            owning_bie_registry=self.bie_registry,
        )

        registry_dictionary_entry = {
            bie_register.bie_register_type_enum: bie_register
        }

        self.bie_registry.update_register_dictionary(
            dictionary_update=registry_dictionary_entry
        )

        return bie_register

    def get_register_column_names_dictionary(
        self,
    ) -> dict:
        return (
            self.__register_column_names_dictionary
        )
