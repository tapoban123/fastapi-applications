def is_file_within_5mb(file_bytes: int):
    if file_bytes <= 5242880:
        return True
    return False
