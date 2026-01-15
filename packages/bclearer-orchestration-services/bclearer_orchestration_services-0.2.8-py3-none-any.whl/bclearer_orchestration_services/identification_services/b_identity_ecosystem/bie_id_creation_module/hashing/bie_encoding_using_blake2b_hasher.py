import hashlib

from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.configurations.bie_id_creation_configurations import (
    BieIdCreationConfigurations,
)


def _hash_bie_encoding_using_blake2b(
    bie_encoding: bytes,
) -> str:
    hash_blake2b = hashlib.blake2b(
        bie_encoding,
        digest_size=BieIdCreationConfigurations.BIE_ID_DIGEST_SIZE,
    )

    hash_as_hex_string = (
        hash_blake2b.hexdigest()
    )

    return hash_as_hex_string
