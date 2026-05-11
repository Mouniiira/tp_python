from typing import Any, Tuple

class DescriptorBase:
    """Classe de base pour automatiser la gestion du nom de l'attribut."""
    def __set_name__(self, owner: type, name: str):
        self.name = name

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

class Positive(DescriptorBase):
    def __init__(self, min_value: float = 0):
        self.min_value = min_value

    def __set__(self, instance: Any, value: float):
        if not (isinstance(value, (int, float)) and value > self.min_value):
            raise ValueError(f"'{self.name}' doit être > {self.min_value} (reçu: {value})")
        instance.__dict__[self.name] = value

class OneOf(DescriptorBase):
    def __init__(self, *choices: Any):
        self.choices = choices

    def __set__(self, instance: Any, value: Any):
        if value not in self.choices:
            raise ValueError(f"'{self.name}' doit être l'un de {self.choices} (reçu: {value})")
        instance.__dict__[self.name] = value

class TypedAttr(DescriptorBase):
    def __init__(self, expected_type: type):
        self.expected_type = expected_type

    def __set__(self, instance: Any, value: Any):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"'{self.name}' doit être de type {self.expected_type.__name__} (reçu: {type(value).__name__})")
        instance.__dict__[self.name] = value

class BoundedFloat(DescriptorBase):
    def __init__(self, low: float, high: float):
        self.low = low
        self.high = high

    def __set__(self, instance: Any, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError(f"'{self.name}' doit être un nombre")
        if not (self.low <= float(value) <= self.high):
            raise ValueError(f"'{self.name}' doit être dans [{self.low}, {self.high}] (reçu: {value})")
        instance.__dict__[self.name] = float(value)

class ModelConfig:
    learning_rate = BoundedFloat(0.0, 1.0)
    n_estimators = Positive(min_value=10)
    objective = OneOf("regression", "binary", "multiclass")
    max_depth = TypedAttr(int)

    def __init__(self, lr, n_est, obj, depth):
        self.learning_rate = lr
        self.n_estimators = n_est
        self.objective = obj
        self.max_depth = depth

# Smoke test
if __name__ == "__main__":
    config = ModelConfig(0.1, 100, "regression", 5)
    print("✅ Configuration initiale valide.")

    print("\n--- Test des rejets ---")

    # Test BoundedFloat
    try:
        config.learning_rate = 1.5
    except ValueError as e:
        print(f"❌ learning_rate rejeté : {e}")

    # Test Positive
    try:
        config.n_estimators = 5
    except ValueError as e:
        print(f"❌ n_estimators rejeté : {e}")

    # Test OneOf
    try:
        config.objective = "clustering"
    except ValueError as e:
        print(f"❌ objective rejeté : {e}")

    # Test TypedAttr
    try:
        config.max_depth = 5.5
    except TypeError as e:
        print(f"❌ max_depth rejeté : {e}")