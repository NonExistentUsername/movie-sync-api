import re


def is_slug(username: str, min_length: int, max_length: int) -> bool:
    regex_name = re.compile(rf"^(?=.{min_length,max_length}$)[a-zA-Z_]\w*$", re.IGNORECASE)
    result = regex_name.search(username)
    if result and result.string == username:
        return True
    return False
