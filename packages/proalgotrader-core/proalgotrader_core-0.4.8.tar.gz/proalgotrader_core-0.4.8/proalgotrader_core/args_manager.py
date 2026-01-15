import argparse
import os

from logzero import logger


def parse_arguments() -> argparse.Namespace:
    try:
        parser = argparse.ArgumentParser(
            description="ProAlgoTrader - Algorithmic Trading Framework",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s                                                              Run with default strategy
  %(prog)s --environment=development                                     Run in development mode (no SSL verification)
  %(prog)s --environment=production                                      Run in production mode (SSL verification enabled)
            """,
        )

        parser.add_argument(
            "--environment",
            default=os.getenv("ENVIRONMENT", "development"),
        )

        parser.add_argument(
            "--algo_session_key",
            default=os.getenv("ALGO_SESSION_KEY", None),
        )

        parser.add_argument(
            "--algo_session_secret",
            default=os.getenv("ALGO_SESSION_SECRET", None),
        )

        parser.add_argument(
            "--api_url",
            default=os.getenv("API_URL", "https://proalgotrader.com"),
        )

        return parser.parse_args()
    except Exception as e:
        logger.debug(e)
        raise Exception(e)


class ArgsManager:
    def __init__(self) -> None:
        self.arguments = parse_arguments()

        self.algo_session_key = self.arguments.algo_session_key

        self.algo_session_secret = self.arguments.algo_session_secret

        self.api_url = self.arguments.api_url

        self.environment = self.arguments.environment

    def validate_arguments(self) -> None:
        if not self.arguments.environment:
            raise Exception("Environment is required")

        if not self.arguments.algo_session_key:
            raise Exception("Algo Session Key is required")

        if not self.arguments.algo_session_secret:
            raise Exception("Algo Session Secret is required")

        if self.arguments.environment not in ["development", "production"]:
            raise Exception(
                f"Invalid Environment '{self.arguments.environment}', Choose between 'development' or 'production'"
            )
