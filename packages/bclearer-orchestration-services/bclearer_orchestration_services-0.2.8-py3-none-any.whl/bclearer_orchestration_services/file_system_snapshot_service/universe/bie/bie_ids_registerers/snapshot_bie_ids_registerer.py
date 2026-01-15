from bclearer_core.bie.domain.bie_domain_objects import (
    BieDomainObjects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.common_knowledge.bie_file_system_snapshot_domain_types import (
    BieFileSystemSnapshotDomainTypes,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.file_system_snapshot_objects import (
    FileSystemSnapshotObjects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_folders import (
    IndividualFileSystemSnapshotFolders,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.snapshots.individual_file_system_snapshot_objects import (
    IndividualFileSystemSnapshotObjects,
)
from bclearer_orchestration_services.file_system_snapshot_service.universe.objects.verses.file_system_snapshot_universe_registries import (
    FileSystemSnapshotUniverseRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.bie_id_creation_facade import (
    BieIdCreationFacade,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_core_relation_types import (
    BieCoreRelationTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.bie_domain_types import (
    BieDomainTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.infrastructure.registrations.bie_infrastructure_registries import (
    BieInfrastructureRegistries,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)
from bclearer_orchestration_services.identification_services.naming_service.b_sequence_names import (
    BSequenceNames,
)
from bclearer_orchestration_services.snapshot_universe_service.objects.sum_objects import (
    SumObjects,
)


def register_snapshot_bie_ids(
    bie_infrastructure_registry: BieInfrastructureRegistries,
    file_system_snapshot_universe_registry: FileSystemSnapshotUniverseRegistries,
) -> None:
    __register_file_system_snapshot_object_in_bie_infrastructure_registry(
        bie_infrastructure_registry=bie_infrastructure_registry,
        file_system_snapshot_object=file_system_snapshot_universe_registry.root_relative_path.snapshot,
    )


def __register_file_system_snapshot_object_in_bie_infrastructure_registry(
    bie_infrastructure_registry: BieInfrastructureRegistries,
    file_system_snapshot_object: IndividualFileSystemSnapshotObjects,
) -> None:
    __register_bie_object_and_type_instance(
        bie_infrastructure_registry=bie_infrastructure_registry,
        bie_domain_object=file_system_snapshot_object,
    )

    __register_bie_whole_part_in_bie_infrastructure_registry(
        bie_infrastructure_registry=bie_infrastructure_registry,
        bie_domain_object_whole=file_system_snapshot_object.owning_snapshot_domain,
        bie_domain_object_part=file_system_snapshot_object,
    )

    __register_bie_sums(
        bie_infrastructure_registry=bie_infrastructure_registry,
        file_system_snapshot_object=file_system_snapshot_object,
    )

    __register_extended_objects_in_bie_infrastructure_registry(
        bie_infrastructure_registry=bie_infrastructure_registry,
        file_system_snapshot_object=file_system_snapshot_object,
    )

    if isinstance(
        file_system_snapshot_object,
        IndividualFileSystemSnapshotFolders,
    ):
        for (
            snapshot_part
        ) in (
            file_system_snapshot_object.parts
        ):
            __register_bie_whole_part_in_bie_infrastructure_registry(
                bie_infrastructure_registry=bie_infrastructure_registry,
                bie_domain_object_whole=file_system_snapshot_object.extended_objects[
                    BieFileSystemSnapshotDomainTypes.BIE_RELATIVE_PATHS
                ],
                bie_domain_object_part=snapshot_part.extended_objects[
                    BieFileSystemSnapshotDomainTypes.BIE_RELATIVE_PATHS
                ],
            )

            __register_file_system_snapshot_object_in_bie_infrastructure_registry(
                bie_infrastructure_registry=bie_infrastructure_registry,
                file_system_snapshot_object=snapshot_part,
            )


def __register_extended_objects_in_bie_infrastructure_registry(
    bie_infrastructure_registry: BieInfrastructureRegistries,
    file_system_snapshot_object: IndividualFileSystemSnapshotObjects,
) -> None:
    for (
        extended_object_bie_id,
        extended_object,
    ) in (
        file_system_snapshot_object.extended_objects.items()
    ):
        __register_bie_object_and_type_instance(
            bie_infrastructure_registry=bie_infrastructure_registry,
            bie_domain_object=extended_object,
        )

        __register_bie_whole_part_in_bie_infrastructure_registry(
            bie_infrastructure_registry=bie_infrastructure_registry,
            bie_domain_object_whole=extended_object,
            bie_domain_object_part=file_system_snapshot_object,
        )


def __register_bie_object_and_type_instance(
    bie_infrastructure_registry: BieInfrastructureRegistries,
    bie_domain_object: BieDomainObjects,
) -> None:
    # TODO: ... remove type from name - for debug only
    # bie_sequence_name = \
    #     BSequenceNames(
    #         initial_b_sequence_name_list=[bie_domain_object.bie_type.b_enum_item_name + '::' + bie_domain_object.base_hr_name])

    bie_sequence_name = BSequenceNames(
        initial_b_sequence_name_list=[
            bie_domain_object.base_hr_name
        ]
    )

    bie_infrastructure_registry.register_bie_id_and_type_instance(
        bie_item_id=bie_domain_object.bie_id,
        bie_sequence_name=bie_sequence_name,
        bie_id_type_id=bie_domain_object.bie_type.item_bie_identity,
    )


def __register_bie_whole_part_in_bie_infrastructure_registry(
    bie_infrastructure_registry: BieInfrastructureRegistries,
    bie_domain_object_whole: BieDomainObjects,
    bie_domain_object_part: IndividualFileSystemSnapshotObjects,
) -> None:
    bie_infrastructure_registry.register_bie_relation(
        bie_place_1_id=bie_domain_object_part.bie_id,
        bie_place_2_id=bie_domain_object_whole.bie_id,
        bie_relation_type_id=BieCoreRelationTypes.BIE_WHOLES_PARTS.item_bie_identity,
    )


def __register_bie_sums(
    bie_infrastructure_registry: BieInfrastructureRegistries,
    file_system_snapshot_object: FileSystemSnapshotObjects,
) -> None:
    for (
        extended_object_type,
        sum_object,
    ) in (
        file_system_snapshot_object.inclusive_ancestor_sum_objects.items()
    ):
        __register_bie_sum(
            bie_infrastructure_registry=bie_infrastructure_registry,
            sum_object=sum_object,
            extended_object_type=extended_object_type,
            inclusivity_type=BieFileSystemSnapshotDomainTypes.INCLUSIVE,
            owning_file_system_snapshot_object_bie_id=file_system_snapshot_object.bie_id,
        )

    for (
        extended_object_type,
        sum_object,
    ) in (
        file_system_snapshot_object.inclusive_descendant_sum_objects.items()
    ):
        __register_bie_sum(
            bie_infrastructure_registry=bie_infrastructure_registry,
            sum_object=sum_object,
            extended_object_type=extended_object_type,
            inclusivity_type=BieFileSystemSnapshotDomainTypes.INCLUSIVE,
            owning_file_system_snapshot_object_bie_id=file_system_snapshot_object.bie_id,
        )

    for (
        extended_object_type,
        sum_object,
    ) in (
        file_system_snapshot_object.exclusive_ancestor_sum_objects.items()
    ):
        __register_bie_sum(
            bie_infrastructure_registry=bie_infrastructure_registry,
            sum_object=sum_object,
            extended_object_type=extended_object_type,
            inclusivity_type=BieFileSystemSnapshotDomainTypes.EXCLUSIVE,
            owning_file_system_snapshot_object_bie_id=file_system_snapshot_object.bie_id,
        )

    for (
        extended_object_type,
        sum_object,
    ) in (
        file_system_snapshot_object.exclusive_descendant_sum_objects.items()
    ):
        __register_bie_sum(
            bie_infrastructure_registry=bie_infrastructure_registry,
            sum_object=sum_object,
            extended_object_type=extended_object_type,
            inclusivity_type=BieFileSystemSnapshotDomainTypes.EXCLUSIVE,
            owning_file_system_snapshot_object_bie_id=file_system_snapshot_object.bie_id,
        )


def __register_bie_sum(
    bie_infrastructure_registry: BieInfrastructureRegistries,
    sum_object: SumObjects,
    extended_object_type: BieDomainTypes,
    inclusivity_type: BieFileSystemSnapshotDomainTypes,
    owning_file_system_snapshot_object_bie_id: BieIds,
) -> None:
    bie_sequence_name = BSequenceNames(
        initial_b_sequence_name_list=[
            sum_object.base_hr_name
        ]
    )

    bie_infrastructure_registry.register_bie_id_if_required(
        bie_item_id=sum_object.bie_id,
        bie_sequence_name=bie_sequence_name,
        bie_id_type_id=sum_object.bie_type.item_bie_identity,
    )

    bie_infrastructure_registry.register_bie_id_type_instance(
        bie_instance_id=sum_object.bie_id,
        bie_type_id=sum_object.bie_type.item_bie_identity,
    )

    input_objects = [
        sum_object.bie_id,
        owning_file_system_snapshot_object_bie_id,
        inclusivity_type.item_bie_identity,
        sum_object.direction_type.item_bie_identity,
    ]

    relation_bie_id = BieIdCreationFacade.create_order_sensitive_bie_id_for_multiple_objects(
        input_objects=input_objects
    )

    relation_bie_sequence_name = BSequenceNames(
        initial_b_sequence_name_list=[
            "sum couple"
        ]
    )

    bie_infrastructure_registry.register_bie_id_and_type_instance(
        bie_item_id=relation_bie_id,
        bie_sequence_name=relation_bie_sequence_name,
        bie_id_type_id=extended_object_type.item_bie_identity,
    )

    bie_infrastructure_registry.register_bie_id_type_instance(
        bie_instance_id=relation_bie_id,
        bie_type_id=sum_object.direction_type.item_bie_identity,
    )

    bie_infrastructure_registry.register_bie_id_type_instance(
        bie_instance_id=relation_bie_id,
        bie_type_id=inclusivity_type.item_bie_identity,
    )

    bie_infrastructure_registry.register_bie_id_type_instance(
        bie_instance_id=relation_bie_id,
        bie_type_id=inclusivity_type.item_bie_identity,
    )

    bie_infrastructure_registry.register_bie_relation(
        bie_place_1_id=relation_bie_id,
        bie_place_2_id=owning_file_system_snapshot_object_bie_id,
        bie_relation_type_id=BieCoreRelationTypes.BIE_SUMMED.item_bie_identity,
    )

    bie_infrastructure_registry.register_bie_relation(
        bie_place_1_id=relation_bie_id,
        bie_place_2_id=sum_object.bie_id,
        bie_relation_type_id=BieCoreRelationTypes.BIE_SUMMING.item_bie_identity,
    )
