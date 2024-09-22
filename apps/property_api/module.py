from .service import PropertyService

from lib.secrets.dot_secret_manager import DotEnvSecretManager
from lib.repository.property_repository import PropertyRepository


class PropertyModule:
    service: PropertyService

    def __init__(self) -> None:
        sm = DotEnvSecretManager()
        property_repository = PropertyRepository(sm)

        self.service = PropertyService(property_repository)
