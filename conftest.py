import os
import pytest
import allure
from playwright.sync_api import sync_playwright

# ========================================================================
# PYTEST + PLAYWRIGHT TEST CONFIGURATION FILE
# ========================================================================
# This file provides:
# 1. Command-line options (browser, base URL, video, screenshots, etc.)
# 2. Hooks to track test results (needed so fixtures know pass/fail)
# 3. Fixtures for browser/context/page setup and teardown
# 4. Screenshot, video, and trace attachments to Allure reports
# ========================================================================

# ----------------------------------------------------------------------------
# STEP 1: ADD COMMAND LINE OPTIONS
# ----------------------------------------------------------------------------


def pytest_addoption(parser):
    parser.addoption("--browser", default="chromium", help="Browser: chromium, firefox, webkit")
    parser.addoption("--headed", action="store_true", help="Run in headed (visible) mode")
    parser.addoption("--base-url", default="https://tutorialsninja.com/demo/", help="Base URL for tests")
    parser.addoption("--video", default="retain-on-failure", help="Record video: on, off, retain-on-failure")
    parser.addoption("--screenshot", default="only-on-failure", help="Take screenshot: on, off, only-on-failure")
    parser.addoption("--tracing", default="retain-on-failure", help="Tracing: on, off, retain-on-failure")


# ----------------------------------------------------------------------------
# STEP 2: GET CONFIGURATION VALUE (CMDLINE OR pytest.ini)
# ----------------------------------------------------------------------------
def get_config_value(config, option_name):
    """
    Helper to read configuration values.
    Tries to get from command line first, otherwise from pytest.ini.
    Supports both string and boolean options.
    """
    cmd_value = config.getoption(option_name)

    if cmd_value is not None:
        return cmd_value

    if option_name == "headed":
        ini_value = config.getini(option_name)
        return ini_value.lower() == "true" if isinstance(ini_value, str) else ini_value
    else:
        return config.getini(option_name)


# ----------------------------------------------------------------------------
# STEP 3: TRACK TEST RESULTS (so fixtures know if a test passed/failed)
# ----------------------------------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # Store the report on the item for each phase (setup/call/teardown)
    setattr(item, f"rep_{report.when}", report)


# ----------------------------------------------------------------------------
# STEP 4: SESSION-LEVEL PLAYWRIGHT INSTANCE
# ----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


# ----------------------------------------------------------------------------
# STEP 5: BROWSER FIXTURE (one browser instance per test session)
# ----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def browser(playwright_instance, request):
    browser_name = get_config_value(request.config, "browser")
    headed = get_config_value(request.config, "headed")

    browser_type = getattr(playwright_instance, browser_name)
    browser_obj = browser_type.launch(headless=not headed)

    yield browser_obj

    browser_obj.close()


# ----------------------------------------------------------------------------
# STEP 6: CONTEXT FIXTURE (new browser context per test = isolated storage)
# ----------------------------------------------------------------------------
@pytest.fixture()
def context(browser, request):
    video_mode = get_config_value(request.config, "video")
    record_video_dir = "reports/videos" if video_mode != "off" else None

    context_args = {}
    if record_video_dir:
        os.makedirs(record_video_dir, exist_ok=True)
        context_args["record_video_dir"] = record_video_dir

    ctx = browser.new_context(**context_args)

    tracing_mode = get_config_value(request.config, "tracing")
    if tracing_mode != "off":
        ctx.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield ctx

    if tracing_mode != "off":
        os.makedirs("reports/traces", exist_ok=True)
        trace_path = f"reports/traces/{request.node.name}.zip"
        should_save = tracing_mode == "on" or (
            tracing_mode == "retain-on-failure" and getattr(request.node, "rep_call", None)
            and request.node.rep_call.failed
        )
        ctx.tracing.stop(path=trace_path if should_save else None)
        if should_save and os.path.exists(trace_path):
            allure.attach.file(trace_path, name="trace", extension="zip")

    ctx.close()


# ----------------------------------------------------------------------------
# STEP 7: PAGE FIXTURE (this is what every Page Object receives)
# ----------------------------------------------------------------------------
@pytest.fixture()
def page(context, request):
    pg = context.new_page()
    # Auto-accept any unexpected browser dialogs (alert/confirm) once per page,
    # instead of registering a listener inside individual page-object methods.
    pg.on("dialog", lambda dialog: dialog.accept())
    base_url = get_config_value(request.config, "base_url")
    if not base_url.startswith("http"):
        base_url = f"https://{base_url}"
    pg.goto(base_url)

    yield pg

    # ----- Screenshot on failure -----
    screenshot_mode = get_config_value(request.config, "screenshot")
    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    if screenshot_mode == "on" or (screenshot_mode == "only-on-failure" and failed):
        try:
            allure.attach(
                pg.screenshot(full_page=True),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
        except Exception as e:
            print(f"Could not capture screenshot: {e}")

    pg.close()

    # ----- Video attachment -----
    video_mode = get_config_value(request.config, "video")
    video_should_attach = video_mode == "on" or (video_mode == "retain-on-failure" and failed)
    if video_should_attach and pg.video:
        try:
            video_path = pg.video.path()
            allure.attach.file(video_path, name="video", extension="webm")
        except Exception as e:
            print(f"Could not attach video: {e}")
