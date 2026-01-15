import blake3
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.configurations.bie_id_creation_configurations import (
    BieIdCreationConfigurations,
)


def _hash_bie_encoding_using_blake3(
    bie_encoding: bytes,
) -> str:
    blake3_hasher = blake3.blake3(
        bie_encoding
    )

    hash_as_hex_string = blake3_hasher.hexdigest(
        length=BieIdCreationConfigurations.BIE_ID_DIGEST_SIZE
    )

    return hash_as_hex_string
