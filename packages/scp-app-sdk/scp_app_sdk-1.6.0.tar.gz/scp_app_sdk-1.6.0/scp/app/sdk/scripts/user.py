import os

class InvalidUserInfoException(Exception):
    pass

def get_env_variable(name: str) -> str:
    """
    Get an environment variable by name

    :param name: Name of the environment variable
    :return: Value of the environment variable or None if not set
    """
    value = os.environ.get(name)
    if not value:
        raise InvalidUserInfoException(f"Environment variable {name} is not set.")
    return value

def get_user_id() -> str:
    """
    Get the user ID from the environment variable USER_ID

    :return: User ID as a string
    """
    return get_env_variable("USER_ID")

def get_iss() -> str:
    """
    Get the issuer (iss) from the environment variable ISS

    :return: Issuer as a string
    """

    return get_env_variable("ISS")
