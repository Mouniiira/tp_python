import yaml
import os
from typing import Any, Dict

class SingletonMeta(type):
    _instances: Dict[type, Any] = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Config(metaclass=SingletonMeta):
    def __init__(self, config_name: str = "config.yaml"):
        if hasattr(self, "_initialized") and self._initialized:
            return
        
        # On cherche le fichier dans le même dossier que ce script
        base_path = os.path.dirname(__file__)
        config_path = os.path.join(base_path, config_name)
            
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"⚠️ Fichier introuvable à : {config_path}")
            
        with open(config_path, "r") as f:
            self._settings = yaml.safe_load(f) or {}
        
        self._initialized = True

    @property
    def raw_data_path(self) -> str:
        # .get() sécurisé pour éviter des plantages si la clé manque dans le YAML
        return self._settings.get("paths", {}).get("raw_data")

    @property
    def seed(self) -> int:
        return self._settings.get("reproducibility", {}).get("seed", 42)

# --- Script de test ---
if __name__ == "__main__":
    try:
        c1 = Config()
        c2 = Config()
        print(f"Même instance ? {c1 is c2}")

        print(f"Path : {c1.raw_data_path}")
        
        # Test de lecture seule
        c1.raw_data_path = "test"
    except AttributeError as e:
        print(f"✅ Protection lecture seule active : {e}")
    except Exception as e:
        print(f"❌ Erreur : {e}")
    
# Method A:
class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
def setup_function():
    # Pour la méthode B (Métaclasse)
    SingletonMeta._instances.clear()
