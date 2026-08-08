"""Entry point for research-timeline CLI."""
from .cli import app

if __name__ == "__main__":
    import sys
    sys.exit(app())