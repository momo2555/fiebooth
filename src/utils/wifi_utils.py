from pathlib import Path
from .file_utils import FileUtils
from errors.errors import MissingWifiConfiguration


class WifiUtils:
    @staticmethod
    def get_ssid() -> str:
        ssid_config_path = Path(FileUtils.get_config_folder(), ".ssid")
        if ssid_config_path.exists():
            with open(ssid_config_path, "rt") as f:
                return f.read()
        else:
            raise MissingWifiConfiguration(".ssid file not found !")

    @staticmethod
    def get_password() -> str:
        return "fiebooth"