from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.datastructure.bie_registries_registers_types import (
    BieRegistriesRegistersTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.enums.datastructure.bie_infrastructure_registry_registers_columns_dictionary import (
    BIE_INFRASTRUCTURE_REGISTRY_REGISTERS_COLUMNS_DICTIONARY,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registries import (
    BieIdRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.registers_factory.bie_registry_register_factories import (
    BieRegistryRegisterFactories,
)


class BieInfrastructureRegistries(
    BieIdRegistries
):
    def __init__(self) -> None:
        super().__init__()

        #     #TODO: check this is not needed
        bie_infrastructure_registry_register_factory = BieRegistryRegisterFactories(
            register_column_names_dictionary=BIE_INFRASTRUCTURE_REGISTRY_REGISTERS_COLUMNS_DICTIONARY,
            bie_registry=self,
        )

        bie_infrastructure_registry_register_factory.create_bie_registry_registers()

    def _get_appropriate_targeted_id_register(
        self, bie_id_type_id: BieIds
    ):
        bie_id_targeted_register = self.get_bie_register(
            bie_register_type_enum=BieRegistriesRegistersTypes.BIE_OBJECTS_REGISTER
        )

        return bie_id_targeted_register

    def _get_appropriate_targeted_relations_register(
        self,
    ):
        targeted_relations_register = self.get_bie_register(
            bie_register_type_enum=BieRegistriesRegistersTypes.BIE_RELATIONS_REGISTER
        )

        return (
            targeted_relations_register
        )

    # @run_and_log_function
    # def register_bie_identity_digital_twin_registry_signature(
    #         self) \
    #         -> None:
    #     register_bie_identity_digital_twin_register_signature(
    #         bie_registry=self)
