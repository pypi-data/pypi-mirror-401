import os
from configparser import ConfigParser, NoSectionError, NoOptionError


class KuukConfig:
    def __init__(self, filename='kuuk.cfg'):
        self.conf = ConfigParser()

        # Default Section Name (ConfigParser requires sections like [server])
        self.DEFAULT_SECTION = 'server'

        # ---------------------------------------------------------
        # 1. Define Defaults
        # ---------------------------------------------------------
        self.defaults = {
            self.DEFAULT_SECTION: {
                'sql_alchemy_conn': 'sqlite:///db.db',
                'database_url': 'sqlite:///db.db', # Added this to match your request
                'port': '8000'
            }
        }
        self.conf.read_dict(self.defaults)

        # ---------------------------------------------------------
        # 2. Locate and Read Config File
        # ---------------------------------------------------------
        # Prioritize env var, else use current working directory
        config_dir = os.environ.get('KUUK_HOME', os.getcwd())
        self.config_path = os.path.join(config_dir, filename)

        if os.path.exists(self.config_path):
            # print(f"Loading config from: {self.config_path}")
            self.conf.read(self.config_path)
        else:
            # print(f"No config file found at {self.config_path}. Using defaults.")
            pass

    def get(self, key, fallback=None):
        # 1. Check Environment Variable
        env_var_name = f"KUUK_{key.upper()}"
        if env_var_name in os.environ:
            return os.environ[env_var_name]

        # 2. Check Config File (in the default section)
        try:
            return self.conf.get(self.DEFAULT_SECTION, key)
        except (NoSectionError, NoOptionError):
            return fallback

    def getint(self, key, fallback=None):
        try:
            val = self.get(key, fallback)
            return int(val) if val is not None else None
        except (ValueError, TypeError):
            return fallback


# Instantiate once
settings = KuukConfig()