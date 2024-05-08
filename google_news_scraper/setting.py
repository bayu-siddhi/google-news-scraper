from selenium import webdriver


def chrome_option() -> webdriver.ChromeOptions:
    """
    Specific feature for running Google Chrome driver, compatible with Google Colab.
    - Run in headless mode, i.e., without a UI or display server dependencies.
    - Disables the sandbox for all process types that are normally sandboxed. Meant to be used as a browser-level switch for testing purposes only.
    - The /dev/shm partition is too small in certain VM environments, causing Chrome to fail or crash (see http://crbug.com/715363). Use this flag to work-around this issue (a temporary directory will always be used to create anonymous shared memory files).
    For more feature, see https://peter.sh/experiments/chromium-command-line-switches/

    Returns:
        selenium.webdriver.ChromeOptions
    """    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return chrome_options
