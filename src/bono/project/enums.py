from src.bono.enums import AppEnum


class ProjectType(AppEnum):
    """Project type enum."""

    WEB = "web"
    MOBILE = "mobile"
    DESKTOP = "desktop"
    OTHER = "other"