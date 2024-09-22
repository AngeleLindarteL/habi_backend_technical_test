from lib.secrets.dot_secret_manager import DotEnvSecretManager


def test_getting_inexistent_key() -> None:
    """Test getting an inexistent key from env secret manager using empty string"""
    # Clear singleton instances first
    DotEnvSecretManager().clear_instance()

    assert DotEnvSecretManager().get("inexistent_key", "") == ""


def test_getting_existent_key() -> None:
    """Test getting an inexistent key from env secret manager"""
    # Clear singleton instances first
    DotEnvSecretManager().clear_instance()

    with open("./.env", "a+") as env_file:
        env_file.write('\nHeLLo_WoRlD="hello!"')
        env_file.close()

    assert DotEnvSecretManager().get("hello_world", "") == "hello!"
