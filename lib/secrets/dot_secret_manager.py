from lib.interface.secret_manager import ISecretManager
from lib.utils.singleton import SingletonBase
from dotenv import dotenv_values


# Using singleton here allows to use the secrets everywhere in the app just spawning a new class
# This secret manager uses the .env file variables :).
class DotEnvSecretManager(ISecretManager, SingletonBase):
    variables: dict[str, str] = {}

    def __init__(self) -> None:
        all_vars = dotenv_values()

        for k, v in all_vars.items():
            normalized_key = k.strip().lower()
            self.variables[normalized_key] = v

    def get(self, key: str, default_value: str) -> str:
        normalized_key = key.strip().lower()

        return self.variables.get(normalized_key, default_value)
