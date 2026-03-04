import os


def is_cloud():
    """
    Check if the application is running in a cloud environment.
    """

    return "GITHUB_RUN_ID" in os.environ
