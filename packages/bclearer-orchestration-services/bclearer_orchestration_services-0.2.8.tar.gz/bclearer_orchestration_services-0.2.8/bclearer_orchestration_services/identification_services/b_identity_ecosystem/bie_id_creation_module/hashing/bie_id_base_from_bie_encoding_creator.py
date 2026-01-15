from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.common_knowledge.types.hashing_algorithm_types import (
    HashingAlgorithmTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.configurations.bie_id_creation_configurations import (
    BieIdCreationConfigurations,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.hashing.bie_encoding_using_blake2b_hasher import (
    _hash_bie_encoding_using_blake2b,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.objects.bie_ids import (
    BieIds,
)


def __create_bie_id_base_from_bie_encoding(
    bie_encoding: bytes,
) -> BieIds:
    hash_as_hex_string = (
        __create_hash_as_hex_string(
            bie_encoding
        )
    )

    hash_as_integer = int(
        hash_as_hex_string, 16
    )

    bie_id = BieIds(
        int_value=hash_as_integer
    )

    return bie_id


def __create_hash_as_hex_string(
    bie_encoding: bytes,
) -> str:
    match BieIdCreationConfigurations.HASHING_ALGORITHM_TYPE:
        case (
            HashingAlgorithmTypes.BLAKE2B
        ):
            return _hash_bie_encoding_using_blake2b(
                bie_encoding=bie_encoding
            )

        case (
            HashingAlgorithmTypes.BLAKE3
        ):
            return _hash_bie_encoding_using_blake2b(
                bie_encoding=bie_encoding
            )

        case _:
            raise NotImplementedError()


def create_bie_id_base_from_bie_encoding(
    bie_encoding: bytes,
) -> BieIds:
    # Public wrapper for external use (avoids accessing protected function)
    return __create_bie_id_base_from_bie_encoding(
        bie_encoding
    )
