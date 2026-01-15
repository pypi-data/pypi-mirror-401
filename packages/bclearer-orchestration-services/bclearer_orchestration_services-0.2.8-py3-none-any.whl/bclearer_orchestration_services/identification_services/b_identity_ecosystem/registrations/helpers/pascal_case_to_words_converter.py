import re


# TODO: Move to nf_common
def convert_pascal_case_to_words(
    pascal_case_string: str,
) -> str:
    words = re.findall(
        r"[A-Z][^A-Z]*",
        pascal_case_string,
    )

    word_string = " ".join(words)

    return word_string
