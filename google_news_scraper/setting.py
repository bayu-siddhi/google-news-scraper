from selenium import webdriver
import geckodriver_autoinstaller


def firefox_option() -> webdriver.FirefoxOptions:
    """
    Specific feature for running Firefox driver, compatible with Google Colab.
    - Run in headless mode, i.e., without a UI or display server dependencies.
    - Disables the sandbox for all process types that are normally sandboxed. Meant to be used as a browser-level switch for testing purposes only.
    - The /dev/shm partition is too small in certain VM environments, causing Chrome to fail or crash (see http://crbug.com/715363). Use this flag to work-around this issue (a temporary directory will always be used to create anonymous shared memory files).

    For more options, see
    - https://www.selenium.dev/documentation/webdriver/browsers/firefox/
    - https://developer.mozilla.org/en-US/docs/Web/WebDriver/Capabilities/firefoxOptions

    Returns:
        selenium.webdriver.FirefoxOptions
    """    
    geckodriver_autoinstaller.install()
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('-headless')
    # Add your own options here
    return firefox_options
