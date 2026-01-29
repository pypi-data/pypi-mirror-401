def get_migrate_versions():
    """
    Get version information during up/down-grading of an application.

    :return: A dictionary containing from_build_version and to_build_version
    """
    return {key.lower(): value for key, value in dict(os.environ).items() if key in ["FROM_BUILD_VERSION", "TO_BUILD_VERSION"]}
