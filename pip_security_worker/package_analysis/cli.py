"""Code to capture imports and cli access."""

from pip_security_worker.package_analysis.analyse import Analyse


def run() -> None:
    """Run the analysis application."""
    Analyse()


if __name__ == '__main__':
    """Capture standard import for package analyse."""
    run()
