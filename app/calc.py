# Example: can raise TypeError (good for testing)
def add(a: int, b: int) -> int:
    return a + b
# Example: can raise OverflowError (good for testing)
def div(a: float, b: float) -> float:
    # Example: can raise ZeroDivisionError (good for testing)
    return a / b