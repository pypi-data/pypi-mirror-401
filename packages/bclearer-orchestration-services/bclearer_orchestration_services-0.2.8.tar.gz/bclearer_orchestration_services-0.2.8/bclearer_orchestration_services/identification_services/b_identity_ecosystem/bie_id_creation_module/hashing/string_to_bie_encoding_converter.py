from bclearer_core.constants.standard_constants import (
    UTF_8_ENCODING_NAME,
)


def convert_string_to_bie_encoding(
    input_string: str,
) -> bytes:
    # Public wrapper for external use (avoids accessing protected function)
    return __convert_string_to_bie_encoding(
        input_string
    )


def __convert_string_to_bie_encoding(
    input_string: str,
) -> bytes:
    bie_encoding = input_string.encode(
        UTF_8_ENCODING_NAME
    )

    return bie_encoding
