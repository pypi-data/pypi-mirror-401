__version__ = "0.0.6"

def hello() -> None:
    """
    A simple hello function to demonstrate the package is working.
    """
    print("docmood: hello from the package v0.0.2!")

__all__ = ["__version__", "hello"]
