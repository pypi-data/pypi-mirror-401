"""Configuration for HTTP retry behaviour with exponential backoff"""

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


class RetryConfig:
    """Configuration for HTTP retry behaviour with exponential backoff

    This class configures retry logic for HTTP requests using urllib3's Retry
    mechanism with exponential backoff. It handles transient failures like
    server errors, timeouts, and connection issues.

    Attributes:
        max_retries: Maximum number of retry attempts (default: 3)
        backoff_factor: Multiplier for exponential backoff in seconds (default: 1.0)
        total_timeout: Total timeout for requests in seconds (default: 30)
        status_forcelist: HTTP status codes that trigger retries (default: 408, 429, 500, 502, 503, 504)
        allowed_methods: HTTP methods that support retries (default: GET, POST, PUT)

    Example:
        >>> config = RetryConfig(max_retries=5, backoff_factor=2.0)
        >>> session = config.create_session()
        >>> response = session.get('https://api.example.com/data')
    """

    def __init__(
        self,
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        total_timeout: int = 30,
        status_forcelist: tuple = (408, 429, 500, 502, 503, 504),
        allowed_methods: tuple = ("GET", "POST", "PUT")
    ):
        """Initialise retry configuration

        Args:
            max_retries: Maximum number of retry attempts
            backoff_factor: Base delay in seconds for exponential backoff
                           (delay = backoff_factor * (2 ^ (retry_number - 1)))
            total_timeout: Maximum time to wait for a response in seconds
            status_forcelist: Tuple of HTTP status codes that should trigger retries
            allowed_methods: Tuple of HTTP methods that support retries
        """
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.total_timeout = total_timeout
        self.status_forcelist = status_forcelist
        self.allowed_methods = allowed_methods

    def get_retry_strategy(self) -> Retry:
        """Create urllib3 Retry strategy with configured parameters

        Returns:
            Retry: Configured urllib3 Retry object with exponential backoff
        """
        return Retry(
            total=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
            allowed_methods=self.allowed_methods,
            raise_on_status=False
        )

    def create_session(self) -> requests.Session:
        """Create requests Session with retry adapter mounted

        Creates a requests.Session object with the retry strategy applied
        to both HTTP and HTTPS endpoints.

        Returns:
            requests.Session: Session object with retry adapter configured
        """
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=self.get_retry_strategy())
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
