import sys
import os
import time
import logging
from abc import ABC, abstractmethod
import pandas as pd

# Ajout du chemin racine pour éviter le ModuleNotFoundError
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# Maintenant on peut importer BasePipelineStep
try:
    from src.core.metaclasses import BasePipelineStep
except ImportError:
    # Fallback si tu n'as pas encore déplacé BasePipelineStep dans src.core
    # ou pour les tests locaux
    BasePipelineStep = object

# --- Interface de l'Observateur ---
class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, data: dict):
        pass

# --- Sujet (Le Pipeline ou les Steps) ---
class PipelineSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event_type: str, data: dict):
        for observer in self._observers:
            observer.update(event_type, data)

# --- Observateurs Concrets ---

class LoggingObserver(Observer):
    def __init__(self, log_file="pipeline.log"):
        logging.basicConfig(filename=log_file, level=logging.INFO, 
                            format='%(asctime)s - %(message)s')

    def update(self, event_type: str, data: dict):
        msg = f"[{event_type}] Step: {data.get('name')} | Status: {data.get('status')}"
        logging.info(msg)
        print(f"📝 Logged: {msg}")

class MetricsObserver(Observer):
    def update(self, event_type: str, data: dict):
        if event_type == "after_run":
            duration = data.get('duration')
            rows = data.get('row_count')
            cols = data.get('col_count')
            print(f"📊 Metrics: {data.get('name')} took {duration:.4f}s | Shape: ({rows}, {cols})")

class AlertObserver(Observer):
    def update(self, event_type: str, data: dict):
        if event_type == "after_run":
            prev_rows = data.get('prev_row_count')
            curr_rows = data.get('row_count')
            
            if prev_rows and curr_rows:
                loss = (prev_rows - curr_rows) / prev_rows
                if loss > 0.30:
                    print(f"⚠️ ALERT: {data.get('name')} lost {loss:.1%} of data!")

if __name__ == "__main__":
    # La classe DummyStep doit accepter les arguments ou utiliser ceux de son parent
    class DummyStep(BasePipelineStep):
        def run(self, df: pd.DataFrame = None) -> pd.DataFrame:
            print(f"   [Action] {self.name} est en train de travailler...")
            time.sleep(0.5)
            # On simule un DataFrame en sortie
            return pd.DataFrame({"col": [1, 2, 3]})

    # Maintenant, l'instanciation fonctionnera car BasePipelineStep possède un __init__(self, name)
    try:
        step = DummyStep(name="TestStep")
        
        # Attacher les observateurs
        step.attach(LoggingObserver())
        step.attach(MetricsObserver())
        
        print("--- Début du test ---")
        # On passe un DataFrame vide pour simuler l'entrée
        df_input = pd.DataFrame({"data": [1, 2, 3, 4, 5]})
        step.execute(df_input)
        print("--- Fin du test ---")
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")