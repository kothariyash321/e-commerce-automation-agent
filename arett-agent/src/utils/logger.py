import logging


def get_logger(name: str) -> logging.Logger:
    """Creates a basic structured logger for the agent."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
    )
    return logging.getLogger(name)
