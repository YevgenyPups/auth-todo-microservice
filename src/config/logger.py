import logging


def setup_logger() -> None:
    """
    Configure the root logger with DEBUG level
    and structured format.
    """

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
