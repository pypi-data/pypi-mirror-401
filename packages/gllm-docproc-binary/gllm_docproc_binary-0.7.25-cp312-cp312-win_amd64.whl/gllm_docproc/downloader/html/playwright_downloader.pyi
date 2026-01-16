from _typeshed import Incomplete
from gllm_docproc.downloader import BaseDownloader as BaseDownloader
from gllm_docproc.downloader.html.utils import generate_filename_from_url as generate_filename_from_url
from gllm_docproc.model.element_metadata import ElementMetadata as ElementMetadata, HTML as HTML
from gllm_docproc.utils.file_utils import save_to_json as save_to_json
from typing import Any

DEFAULT_TIMEOUT: int
DEFAULT_WAIT_UNTIL: str
DEFAULT_MAX_RETRIES: int
DEFAULT_BACKOFF_FACTOR: int
NON_RETRYABLE_ERROR_PATTERNS: Incomplete

class PlaywrightDownloader(BaseDownloader):
    """A class for downloading web pages using Playwright to the defined output directory.

    This downloader uses Playwright to render JavaScript-heavy web pages and save them as JSON files.
    It supports waiting for page load, custom user agents, and timeout configuration.
    """
    headless: Incomplete
    timeout: Incomplete
    wait_until: Incomplete
    user_agent: Incomplete
    max_retries: Incomplete
    backoff_factor: Incomplete
    logger: Incomplete
    def __init__(self, headless: bool = True, timeout: int = ..., wait_until: str = ..., user_agent: str | None = None, max_retries: int = ..., backoff_factor: float = ...) -> None:
        '''Initialize the PlaywrightDownloader.

        Args:
            headless (bool, optional): Whether to run the browser in headless mode. Defaults to True.
            timeout (int, optional): Navigation timeout in milliseconds. Defaults to 5000 (5 seconds).
            wait_until (str, optional): When to consider navigation succeeded. Options:
                - "commit": Returns immediately after response headers (fastest, page may not be fully rendered).
                - "domcontentloaded": Waits until HTML document is parsed (stylesheets/images may still load).
                - "load": Waits until all resources finish loading (images, stylesheets, scripts).
                - "networkidle": Waits until network is idle for 500ms (best for JavaScript-heavy pages/SPAs).
                Defaults to "networkidle".
            user_agent (str | None, optional): Custom user agent string. Defaults to None (uses Playwright default).
            max_retries (int, optional): The maximum number of retries for failed downloads. Defaults to 2.
            backoff_factor (float, optional): Base backoff factor in seconds for exponential backoff. Defaults to 1.
        '''
    def download(self, source: str, output: str, **kwargs: Any) -> list[str]:
        """Download web page from source URL and save as JSON file.

        Args:
            source (str): The URL of the web page to download.
            output (str): The output directory where the downloaded JSON file will be saved.
            **kwargs (Any): Additional keyword arguments.

        kwargs:
            wait_for_selector (str, optional): CSS selector to wait for before saving. Defaults to None.
            wait_timeout (int, optional): Timeout in milliseconds for waiting for selector. Defaults to None.

        Returns:
            list[str]: A list containing the file path of the successfully downloaded JSON file.

        Raises:
            Exception: If any exception occurs during the download process.
        """
