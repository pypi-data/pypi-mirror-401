import os


def get_posix_file_reference_number(
    file_path_as_string: str,
) -> int:
    file_reference_number = os.stat(
        file_path_as_string,
        follow_symlinks=True,
    ).st_ino

    return file_reference_number
