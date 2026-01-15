from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_id_registries import (
    BieIdRegistries,
)


class BieSubRegistries(BieIdRegistries):
    def __init__(self) -> None:
        super().__init__()

    def _get_appropriate_targeted_id_register(
        self, bie_id_type_id
    ):
        # Subclasses must provide the concrete targeted ID register
        raise NotImplementedError()

    def _get_appropriate_targeted_relations_register(
        self,
    ):
        # Subclasses must provide the concrete targeted relations register
        raise NotImplementedError()
