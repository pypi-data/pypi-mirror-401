import json
import sys

# deprecated function for configuration, kept for backward compatibility used in user.py
from scp.app.sdk.scripts.user import get_user_id  # type: ignore

# deprecated function for configuration, kept for backward compatibility used in migrate.py
from scp.app.sdk.scripts.migrate import get_migrate_versions  # type: ignore

_APP_CONFIGURATOR_MARKER = "###APP_CONFIG_OVERWRITE = "


def get_inputs():
    """
    Get the provided configuration as a Python object
    ( ie like json.load(sys.stdin) )

    :return: A python object representing the application configuration
    """
    return json.load(sys.stdin)


def set_configuration(config):
    """
    Allows you to set configuration for the application on installation.

    Prints the config to sys.stdout in a special format for detection.

    :param config: A python object representing the application configuration
    """
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a dictionary.")

    print(f"{_APP_CONFIGURATOR_MARKER}{json.dumps(config)}", file=sys.stdout)
