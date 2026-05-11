import pytest
import pandas as pd
from src.core.metaclasses import BasePipelineStep

def test_valid_pipeline_step():
    """Vérifie qu'une classe bien définie ne lève aucune erreur."""
    try:
        class ValidStep(BasePipelineStep):
            name = "valid_step"
            def run(self, df: pd.DataFrame) -> pd.DataFrame:
                return df
    except TypeError as e:
        pytest.fail(f"La définition d'une classe valide a échoué : {e}")

def test_missing_name_attribute():
    """Vérifie que l'absence de 'name' lève une TypeError."""
    # On simplifie le match pour ne pas bloquer sur les guillemets ou le ': str'
    with pytest.raises(TypeError, match="doit définir un attribut de classe 'name"):
        class MissingNameStep(BasePipelineStep):
            def run(self, df: pd.DataFrame) -> pd.DataFrame:
                return df

def test_missing_run_method():
    """Vérifie que l'absence de 'run' lève une TypeError."""
    # On utilise un point '.' pour dire 'n'importe quel caractère' 
    # ou on s'arrête juste avant les parenthèses pour éviter les soucis de Regex
    with pytest.raises(TypeError, match="doit implémenter la méthode 'run"):
        class MissingRunStep(BasePipelineStep):
            name = "incomplete_step"

def test_invalid_name_type():
    """Vérifie que 'name' doit être une chaîne de caractères."""
    with pytest.raises(TypeError, match="doit définir un attribut de classe 'name: str'"):
        class WrongNameTypeStep(BasePipelineStep):
            name = 123  # Devrait être str
            def run(self, df: pd.DataFrame) -> pd.DataFrame:
                return df