from selenium import webdriver
import geckodriver_autoinstaller


def firefox_option() -> webdriver.FirefoxOptions:
    """
    Specific feature for running Firefox driver, compatible with Google Colab.

    - Run in headless mode, i.e., without a UI or display server dependencies.

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
