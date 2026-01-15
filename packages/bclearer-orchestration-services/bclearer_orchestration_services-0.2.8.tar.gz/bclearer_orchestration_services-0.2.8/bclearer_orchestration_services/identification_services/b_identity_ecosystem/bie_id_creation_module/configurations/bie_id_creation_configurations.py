from bclearer_orchestration_services.identification_services.b_identity_ecosystem.bie_id_creation_module.common_knowledge.types.hashing_algorithm_types import (
    HashingAlgorithmTypes,
)
from bclearer_orchestration_services.identification_services.b_identity_ecosystem.common_knowledge.data_type_recognition import (
    DataTypeRecognition,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.null_type_recognition import (
    NullTypeRecognition,
)
from bclearer_orchestration_services.identification_services.pandas_null_values.string_based_null_type_recognition import (
    StringBasedNullTypeRecognition,
)


class BieIdCreationConfigurations:
    BIE_ID_DIGEST_SIZE = 8

    HASHING_ALGORITHM_TYPE = (
        HashingAlgorithmTypes.BLAKE2B
    )

    NULL_TYPE_RECOGNITION = (
        NullTypeRecognition.COARSE_GRAINED_SINGLE_VALUE
    )

    STRING_BASED_NULL_TYPE_RECOGNITION = (
        StringBasedNullTypeRecognition.DO_NOT_RECOGNISE_STRING_BASED_NULL_AS_NULL
    )

    DATA_TYPE_RECOGNITION = (
        DataTypeRecognition.DO_NOT_INCLUDE_DATA_TYPES_IN_BIE_CALCULATION
    )
