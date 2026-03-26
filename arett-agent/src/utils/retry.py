from tenacity import retry, stop_after_attempt, wait_exponential


def default_retry(fn):
    """Applies standard retry policy for external API calls."""
    return retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))(fn)
