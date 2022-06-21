import toml


def parse_config(path):
    """Парсит конфиг инстансов."""
    return toml.load(path)
