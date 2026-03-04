import os


def is_cloud():
    """
    Check if the application is running in a cloud environment.
    """

    return "WEBSITE_SITE_NAME" in os.environ
