import pathlib
from playwright.sync_api import Page, expect
import pytest
from subprocess import Popen, PIPE
from http.client import HTTPConnection
import time

test_dir = pathlib.Path(__file__).parent.absolute()
root = test_dir.parent.absolute()


@pytest.fixture(scope="module")
def static_server():
    process = Popen(
        ["python", "-m", "http.server", "8124", "--directory", root],
        stdout=PIPE,
    )
    try:
        retries = 5
        while retries > 0:
            conn = HTTPConnection("127.0.0.1:8124")
            try:
                conn.request("HEAD", "/")
                conn.getresponse()
                break
            except ConnectionRefusedError:
                time.sleep(1)
                retries -= 1
        yield process
    finally:
        process.terminate()
        process.wait()


BASE_URL = "http://127.0.0.1:8124/fit-file-workout.html"


def test_page_title(page: Page, static_server):
    page.goto(BASE_URL)
    expect(page).to_have_title("FIT File Workout Creator")


def test_heading(page: Page, static_server):
    page.goto(BASE_URL)
    expect(page.locator("h1")).to_have_text("FIT File Workout Creator")


def test_tabs_exist(page: Page, static_server):
    page.goto(BASE_URL)
    expect(page.locator('[data-tab="viewer"]')).to_be_visible()
    expect(page.locator('[data-tab="creator"]')).to_be_visible()


def test_viewer_tab_active_by_default(page: Page, static_server):
    page.goto(BASE_URL)
    expect(page.locator("#tab-viewer")).to_have_class("tab-content active")
    expect(page.locator("#tab-creator")).not_to_have_class("tab-content active")


def test_switch_to_creator_tab(page: Page, static_server):
    page.goto(BASE_URL)
    page.click('[data-tab="creator"]')
    expect(page.locator("#tab-creator")).to_have_class("tab-content active")
    expect(page.locator("#tab-viewer")).not_to_have_class("tab-content active")


def test_creator_input_visible(page: Page, static_server):
    page.goto(BASE_URL)
    page.click('[data-tab="creator"]')
    expect(page.locator("#workout-input")).to_be_visible()
    expect(page.locator("#parse-btn")).to_be_visible()
    expect(page.locator("#download-btn")).to_be_visible()


def test_parse_empty_shows_error(page: Page, static_server):
    page.goto(BASE_URL)
    page.click('[data-tab="creator"]')
    page.locator("#workout-input").fill("")
    page.click("#parse-btn")
    expect(page.locator("#parse-error")).to_be_visible()


def test_parse_simple_workout(page: Page, static_server):
    page.goto(BASE_URL)
    page.click('[data-tab="creator"]')
    page.locator("#workout-input").fill("warmup 10 minutes\nrun 3 miles\ncooldown 5 minutes")
    page.click("#parse-btn")
    expect(page.locator("#preview-section")).to_be_visible()
    # Should have 3 step cards
    step_cards = page.locator(".step-card")
    expect(step_cards).to_have_count(3)


def test_parse_enables_download(page: Page, static_server):
    page.goto(BASE_URL)
    page.click('[data-tab="creator"]')
    page.locator("#workout-input").fill("run 5 km")
    page.click("#parse-btn")
    expect(page.locator("#download-btn")).to_be_enabled()


def test_parse_intervals(page: Page, static_server):
    page.goto(BASE_URL)
    page.click('[data-tab="creator"]')
    page.locator("#workout-input").fill("3x800m with 400m recovery")
    page.click("#parse-btn")
    # 3 active + 3 recovery = 6 steps
    step_cards = page.locator(".step-card")
    expect(step_cards).to_have_count(6)


def test_drop_zone_visible(page: Page, static_server):
    page.goto(BASE_URL)
    expect(page.locator("#drop-zone")).to_be_visible()


def test_download_btn_disabled_initially(page: Page, static_server):
    page.goto(BASE_URL)
    page.click('[data-tab="creator"]')
    expect(page.locator("#download-btn")).to_be_disabled()


def test_workout_name_input(page: Page, static_server):
    page.goto(BASE_URL)
    page.click('[data-tab="creator"]')
    name_input = page.locator("#workout-name")
    expect(name_input).to_be_visible()
    expect(name_input).to_have_value("My Workout")


def test_sport_select(page: Page, static_server):
    page.goto(BASE_URL)
    page.click('[data-tab="creator"]')
    sport_select = page.locator("#workout-sport")
    expect(sport_select).to_be_visible()
    # Default is running
    expect(sport_select).to_have_value("1")


def test_unit_select(page: Page, static_server):
    page.goto(BASE_URL)
    page.click('[data-tab="creator"]')
    unit_select = page.locator("#workout-unit")
    expect(unit_select).to_be_visible()
    expect(unit_select).to_have_value("mi")


def test_intensity_types_displayed(page: Page, static_server):
    page.goto(BASE_URL)
    page.click('[data-tab="creator"]')
    page.locator("#workout-input").fill(
        "warmup 5 minutes\nrun 3 miles\nrest 2 minutes\ncooldown 10 minutes"
    )
    page.click("#parse-btn")
    # Check intensity labels exist
    expect(page.locator(".type-warmup")).to_have_count(1)
    expect(page.locator(".type-active")).to_have_count(1)
    expect(page.locator(".type-rest")).to_have_count(1)
    expect(page.locator(".type-cooldown")).to_have_count(1)
