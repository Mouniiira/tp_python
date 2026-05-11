from typing import List
from src.core.mixins import LoggableMixin, SerializableMixin, ValidatableMixin
from src.core.metaclasses import BasePipelineStep

class Pipeline(LoggableMixin, SerializableMixin, ValidatableMixin):
    def __init__(self, steps: List[BasePipelineStep] = None):
        self.steps = steps or []
        self.log_info(f"Pipeline initialisé avec {len(self.steps)} étapes.")

    def add_step(self, step: BasePipelineStep):
        self.steps.append(step)
        self.log_info(f"Étape ajoutée : {step.name}")

    def run(self, df: pd.DataFrame = None) -> pd.DataFrame:
        self.log_info("Démarrage de l'exécution du pipeline...")
        current_df = df

        for step in self.steps:
            self.log_info(f"Exécution de l'étape : {step.name}")
            # Rappel : on appelle .execute() pour activer les Observers !
            current_df = step.execute(current_df)
            
            # Validation automatique après chaque étape via le Mixin
            self.validate(current_df)
            
        self.log_info("Pipeline terminé avec succès.")
        return current_df