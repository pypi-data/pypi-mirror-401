"""Example package published with markpact"""

__version__ = "0.1.0"

def hello(name: str = "World") -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b