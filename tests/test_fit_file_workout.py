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


def test_summary_section_hidden_initially(page: Page, static_server):
    page.goto(BASE_URL)
    expect(page.locator("#summary-section")).to_be_hidden()


def test_splits_section_hidden_initially(page: Page, static_server):
    page.goto(BASE_URL)
    expect(page.locator("#splits-section")).to_be_hidden()


def test_download_md_btn_exists(page: Page, static_server):
    page.goto(BASE_URL)
    expect(page.locator("#download-md-btn")).to_be_attached()


def test_summary_displays_with_session_data(page: Page, static_server):
    """Test that summary section shows when session data is injected."""
    page.goto(BASE_URL)
    page.evaluate("""() => {
        const messages = {
            session: [{
                total_distance: 804670,
                total_elapsed_time: 1800000,
                avg_speed: 4472,
                avg_heart_rate: 155,
                max_heart_rate: 178,
                avg_cadence: 88,
                total_ascent: 120,
                total_descent: 115,
                total_calories: 450
            }],
            record: []
        };
        displaySummary(messages);
    }""")
    expect(page.locator("#summary-section")).to_be_visible()
    # Check that summary stats rendered
    expect(page.locator(".summary-stat")).to_have_count(7)


def test_splits_display_with_lap_data(page: Page, static_server):
    """Test that splits section shows when lap data is injected."""
    page.goto(BASE_URL)
    page.evaluate("""() => {
        const messages = {
            lap: [
                { total_distance: 160934, total_elapsed_time: 420000, avg_speed: 3832, avg_heart_rate: 150, max_heart_rate: 165, avg_cadence: 86, total_ascent: 15, total_descent: 12 },
                { total_distance: 160934, total_elapsed_time: 410000, avg_speed: 3925, avg_heart_rate: 158, max_heart_rate: 172, avg_cadence: 88, total_ascent: 20, total_descent: 18 },
                { total_distance: 160934, total_elapsed_time: 430000, avg_speed: 3744, avg_heart_rate: 162, max_heart_rate: 180, avg_cadence: 90, total_ascent: 25, total_descent: 22 }
            ]
        };
        displaySplits(messages);
    }""")
    expect(page.locator("#splits-section")).to_be_visible()
    # Should have a splits table with 3 body rows
    rows = page.locator(".splits-table tbody tr")
    expect(rows).to_have_count(3)


def test_splits_table_has_headers(page: Page, static_server):
    """Test that splits table headers include expected columns."""
    page.goto(BASE_URL)
    page.evaluate("""() => {
        const messages = {
            lap: [
                { total_distance: 160934, total_elapsed_time: 420000, avg_speed: 3832, avg_heart_rate: 150, max_heart_rate: 165 },
                { total_distance: 160934, total_elapsed_time: 410000, avg_speed: 3925, avg_heart_rate: 158, max_heart_rate: 172 }
            ]
        };
        displaySplits(messages);
    }""")
    headers = page.locator(".splits-table th")
    header_texts = headers.all_text_contents()
    assert "Split" in header_texts
    assert "Distance" in header_texts
    assert "Pace" in header_texts
    assert "Avg HR" in header_texts


def test_splits_fastest_slowest_highlight(page: Page, static_server):
    """Test that fastest and slowest splits are highlighted."""
    page.goto(BASE_URL)
    page.evaluate("""() => {
        const messages = {
            lap: [
                { total_distance: 160934, avg_speed: 3832 },
                { total_distance: 160934, avg_speed: 4500 },
                { total_distance: 160934, avg_speed: 3200 }
            ]
        };
        displaySplits(messages);
    }""")
    expect(page.locator(".splits-table .fastest")).to_have_count(1)
    expect(page.locator(".splits-table .slowest")).to_have_count(1)


def test_markdown_generation(page: Page, static_server):
    """Test that markdown summary is generated correctly."""
    page.goto(BASE_URL)
    md = page.evaluate("""() => {
        parsedData = { messages: {
            session: [{
                total_distance: 804670,
                total_elapsed_time: 1800000,
                avg_speed: 4472,
                avg_heart_rate: 155,
                max_heart_rate: 178,
                avg_cadence: 88,
                total_ascent: 120,
                total_descent: 115,
                timestamp: 1150000000
            }],
            record: [
                { heart_rate: 130 },
                { heart_rate: 155 },
                { heart_rate: 178 }
            ],
            lap: [
                { total_distance: 160934, total_elapsed_time: 420000, avg_speed: 3832, avg_heart_rate: 150 },
                { total_distance: 160934, total_elapsed_time: 410000, avg_speed: 3925, avg_heart_rate: 158 }
            ]
        }};
        return generateMarkdownSummary(parsedData.messages);
    }""")
    assert "# Workout Summary" in md
    assert "## Overall" in md
    assert "## Splits" in md
    assert "Distance" in md
    assert "Avg Heart Rate" in md
    assert "155 bpm" in md
    assert "Elevation Gain" in md
    assert "120 m" in md


def test_no_splits_when_no_laps(page: Page, static_server):
    """Splits section stays hidden when there are no lap messages."""
    page.goto(BASE_URL)
    page.evaluate("""() => {
        displaySplits({ record: [{ heart_rate: 150 }] });
    }""")
    expect(page.locator("#splits-section")).to_be_hidden()


def test_summary_with_records_only(page: Page, static_server):
    """Summary computes HR from records when session is missing HR."""
    page.goto(BASE_URL)
    result = page.evaluate("""() => {
        const messages = {
            session: [{ total_distance: 500000 }],
            record: [
                { heart_rate: 120 },
                { heart_rate: 140 },
                { heart_rate: 160 },
                { heart_rate: 180 }
            ]
        };
        displaySummary(messages);
        return {
            visible: document.getElementById('summary-section').style.display !== 'none',
            statCount: document.querySelectorAll('.summary-stat').length
        };
    }""")
    assert result["visible"] is True
    assert result["statCount"] >= 2  # distance + avg HR at minimum
