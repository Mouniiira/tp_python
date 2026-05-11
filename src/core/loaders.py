import pandas as pd
import os
from typing import Dict, Type
from src.core.metaclasses import BasePipelineStep

# Registre global pour stocker les classes de chargement
LOADER_REGISTRY: Dict[str, Type["BaseLoader"]] = {}

def register_loader(extension: str):
    """Décorateur pour enregistrer automatiquement un loader dans la factory."""
    def decorator(cls):
        if not extension.startswith('.'):
            ext = f".{extension}"
        else:
            ext = extension
        LOADER_REGISTRY[ext] = cls
        return cls
    return decorator

class BaseLoader(BasePipelineStep):
    """Classe de base spécifique aux loaders pour gérer le chemin du fichier."""
    def __init__(self, path: str):
        self.path = path

@register_loader(extension=".parquet")
class ParquetLoader(BaseLoader):
    name = "parquet_loader"
    
    def run(self, df: pd.DataFrame = None) -> pd.DataFrame:
        # On ignore le df en entrée car le loader initialise le pipeline
        return pd.read_parquet(self.path, engine="pyarrow")

@register_loader(extension=".csv")
class CSVLoader(BaseLoader):
    name = "csv_loader"
    
    def run(self, df: pd.DataFrame = None) -> pd.DataFrame:
        return pd.read_csv(self.path)

@register_loader(extension=".json")
class JSONLoader(BaseLoader):
    name = "json_loader"
    
    def run(self, df: pd.DataFrame = None) -> pd.DataFrame:
        return pd.read_json(self.path)

class LoaderFactory:
    """Factory utilisant le registre pour instancier le bon loader."""
    @staticmethod
    def create(path: str) -> BaseLoader:
        _, ext = os.path.splitext(path.lower())
        
        loader_class = LOADER_REGISTRY.get(ext)
        if not loader_class:
            supported = ", ".join(LOADER_REGISTRY.keys())
            raise ValueError(f"Format '{ext}' non supporté. Formats valides : {supported}")
        
        return loader_class(path)