import os
import pytest
import base64
import pytest_html
from pytest_metadata.plugin import metadata_key
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()

# Get Percy token
percy_token = os.getenv("PERCY_TOKEN")

if not percy_token:
    raise RuntimeError("❌ Percy token not found! Please set it in .env")


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser type: chromium, firefox, or webkit",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )


def pytest_configure(config):
    browser = config.getoption("--browser").lower()
    headless = config.getoption("--headless")

    config.stash[metadata_key]["Project"] = "playwright_try"
    config.stash[metadata_key]["Browser"] = browser
    if headless:
        config.stash[metadata_key]["Mode"] = "headless"

    # Ensure the screenshots folder exists
    os.makedirs("screenshots", exist_ok=True)


def pytest_html_report_title(report):
    report.title = "Automation Report"


@pytest.fixture(scope="session")
def browser_type(request):
    return request.config.getoption("--browser").lower()


@pytest.fixture(scope="session")
def headless_mode(request):
    return request.config.getoption("--headless")


@pytest.fixture(scope="session")
def browser_context(browser_type, headless_mode):
    with sync_playwright() as p:
        # Browser launcher map using lambda functions
        browser_launcher = {
            "chromium": lambda: p.chromium.launch(
                headless=headless_mode, args=["--start-maximized"]
            ),
            "firefox": lambda: p.firefox.launch(headless=headless_mode),
            "webkit": lambda: p.webkit.launch(headless=headless_mode),
        }

        browser = browser_launcher.get(browser_type)
        if not browser:
            raise ValueError("Invalid browser type! Use chromium, firefox, or webkit.")

        browser_instance = browser()

        # Viewport setup
        if headless_mode:
            context = browser_instance.new_context(viewport={"width": 1920, "height": 1080})
        else:
            context = (
                browser_instance.new_context(no_viewport=True)
                if browser_type == "chromium"
                else browser_instance.new_context(viewport={"width": 1920, "height": 1080})
            )

        yield context
        browser_instance.close()


@pytest.fixture(scope="function")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.wait_for_timeout(2000)
    page.close()


# This hook adds screenshots and page URL to the HTML report on test failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute other hooks to get the report object
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            page = item.funcargs.get("page", None)
            if page:
                # Save screenshot
                screenshot_path = os.path.join("screenshots", f"{item.name}.png")
                page.screenshot(path=screenshot_path, full_page=True)

                # Read and encode the image in base64
                with open(screenshot_path, "rb") as f:
                    encoded_image = base64.b64encode(f.read()).decode()

                # Embed screenshot into report using base64
                html_img = f'<div><img src="data:image/png;base64,{encoded_image}" alt="screenshot" style="max-width:600px; max-height:400px;" /></div>'
                extras.append(pytest_html.extras.html(html_img))

                # Optionally add the page URL
                extras.append(pytest_html.extras.url(page.url))

        report.extras = extras
