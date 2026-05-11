import pandas as pd
from typing import Any, Dict, Tuple, Type

class PipelineStepMeta(type):
    """
    Métaclasse garantissant que chaque étape du pipeline possède 
    un nom et une méthode d'exécution valide.
    """
    def __new__(mcs, name: str, bases: Tuple[type, ...], attrs: Dict[str, Any]) -> Type:
        # On ne vérifie pas la classe de base elle-même
        if name == "BasePipelineStep":
            return super().__new__(mcs, name, bases, attrs)

        # 1. Vérification de l'attribut 'name'
        if "name" not in attrs or not isinstance(attrs["name"], str):
            raise TypeError(f"La classe {name} doit définir un attribut de classe 'name: str'")

        # 2. Vérification de la méthode 'run'
        if "run" not in attrs or not callable(attrs["run"]):
            raise TypeError(f"La classe {name} doit implémenter la méthode 'run(self, df: pd.DataFrame)'")

        # Note : Pour une vérification stricte de la signature (arguments), 
        # on pourrait utiliser le module 'inspect', mais la présence du callable 
        # est la contrainte principale demandée ici.

        return super().__new__(mcs, name, bases, attrs)


class BasePipelineStep(PipelineSubject):
    def __init__(self, name: str = None):
        # Initialise la liste des observateurs dans PipelineSubject
        super().__init__() 
        self.name = name or self.__class__.__name__
    pass

if __name__ == "__main__":
    print("=== Test de validation de la Métaclasse ===\n")

    # Cas 1 : Tentative de définition d'une classe SANS attribut 'name'
    print("Tentative de définition de 'IncompleteStep' (sans attribut name)...")
    try:
        class IncompleteStep(BasePipelineStep):
            def run(self, df: pd.DataFrame):
                return df
    except TypeError as e:
        print(f"❌ ERREUR CAPTURÉE : {e}")

    print("-" * 50)

    # Cas 2 : Tentative de définition d'une classe SANS méthode 'run'
    print("Tentative de définition de 'NoRunStep' (sans méthode run)...")
    try:
        class NoRunStep(BasePipelineStep):
            name = "test_step"
    except TypeError as e:
        print(f"❌ ERREUR CAPTURÉE : {e}")

    print("-" * 50)

    # Cas 3 : Définition d'une classe valide
    print("Tentative de définition de 'PerfectStep' (classe complète)...")
    try:
        class PerfectStep(BasePipelineStep):
            name = "clean_data"
            def run(self, df: pd.DataFrame):
                return df
        print("✅ SUCCÈS : La classe PerfectStep a été définie sans erreur.")
    except TypeError as e:
        print(f"❌ ERREUR INATTENDUE : {e}")

    print("\nNote : Aucune instance n'a été créée, l'erreur survient à la définition.")