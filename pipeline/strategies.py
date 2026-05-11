from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class EncodingStrategy(ABC):
    """Interface abstraite pour toutes les stratégies d'encodage."""
    
    @abstractmethod
    def encode(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        pass

class OneHotStrategy(EncodingStrategy):
    """Encodage One-Hot (crée une colonne par catégorie)."""
    
    def encode(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        print(f"🛠️  Application One-Hot sur '{column}'")
        return pd.get_dummies(df, columns=[column], prefix=column)

class FrequencyEncodingStrategy(EncodingStrategy):
    """Remplace la catégorie par sa fréquence d'apparition (utile pour haute cardinalité)."""
    
    def encode(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        print(f"🛠️  Application Frequency Encoding sur '{column}'")
        freq = df[column].value_counts(normalize=True)
        df_copy = df.copy()
        df_copy[f"{column}_freq"] = df_copy[column].map(freq)
        return df_copy

class TargetEncodingStrategy(EncodingStrategy):
    """
    Remplace la catégorie par la moyenne de la cible (version simplifiée).
    Note : Dans un cas réel, on utiliserait le 'total_amount' comme cible.
    """
    
    def encode(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        print(f"🛠️  Application Target Encoding sur '{column}'")
        target = "total_amount"
        if target not in df.columns:
            # Fallback si la cible n'existe pas pour la démo
            df[target] = np.random.randint(10, 100, size=len(df))
            
        means = df.groupby(column)[target].mean()
        df_copy = df.copy()
        df_copy[f"{column}_target"] = df_copy[column].map(means)
        return df_copy
    
# FeatureEngineer et Injection de Dépendance
class FeatureEngineer:
    """
    Le Contexte : il utilise une stratégie mais ne sait pas comment elle fonctionne.
    """
    def __init__(self, strategy: EncodingStrategy):
        self._strategy = strategy

    @property
    def strategy(self) -> EncodingStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: EncodingStrategy):
        """Permet de changer de stratégie à chaud (Runtime)."""
        self._strategy = strategy

    def process(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        # Délégation de la responsabilité à la stratégie
        return self._strategy.encode(df, column)
    
if __name__ == "__main__":
    # Création d'un mini DataFrame de test (PULocationID)
    data = pd.DataFrame({
        'PULocationID': [10, 20, 10, 30, 20, 10],
        'total_amount': [15.5, 20.0, 12.0, 45.0, 18.5, 14.0]
    })

    print("🚀 Début de la démonstration du Strategy Pattern\n")

    # 1. Initialisation avec One-Hot
    engineer = FeatureEngineer(OneHotStrategy())
    df_oh = engineer.process(data, 'PULocationID')
    print(f"Colonnes après One-Hot : {df_oh.columns.tolist()}\n")

    # 2. Changement à chaud vers Frequency Encoding
    engineer.strategy = FrequencyEncodingStrategy()
    df_freq = engineer.process(data, 'PULocationID')
    print(f"Nouvelle colonne : {df_freq[['PULocationID_freq']].head(2)}\n")

    # 3. Changement à chaud vers Target Encoding
    engineer.strategy = TargetEncodingStrategy()
    df_target = engineer.process(data, 'PULocationID')
    print(f"Nouvelle colonne : {df_target[['PULocationID_target']].head(2)}")