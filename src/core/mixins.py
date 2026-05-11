import pandas as pd
import logging
import pickle
import os

class LoggableMixin:
    """Ajoute des capacités de logging standardisées."""
    def log_info(self, message):
        logging.info(f"[{self.__class__.__name__}] {message}")

    def log_warning(self, message):
        logging.warning(f"[{self.__class__.__name__}] {message}")

class SerializableMixin:
    """Permet de sauvegarder/charger l'état de l'objet ou ses données."""
    def to_pickle(self, df, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(df, f)
        print(f"💾 Données persistées vers {path}")

    def from_pickle(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)

class ValidatableMixin:
    """Interface pour la validation de données."""
    def validate(self, df: pd.DataFrame):
        if df is None or df.empty:
            raise ValueError("Le DataFrame est vide ou nul.")
        return True