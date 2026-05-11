"""Tests for pace-calculator.html"""
from playwright.sync_api import Page, expect


URL = "http://127.0.0.1:8123/pace-calculator.html"


def test_initial_state(page: Page, static_server):
    page.goto(URL)
    expect(page.locator("h1")).to_have_text("Pace Calculator")
    expect(page.locator("#race-tbody tr")).to_have_count(8)


def test_pace_input_updates_speed_and_race_table(page: Page, static_server):
    page.goto(URL)
    page.locator("#pace-min").fill("10")
    page.locator("#pace-sec").fill("0")

    expect(page.locator("#pace-speed")).to_have_text("6.0 mph")
    expect(page.locator("#pace-alt")).to_have_text("6:13")
    expect(page.locator("#race-tbody tr").first).to_contain_text("31:04")


def test_time_tab_calculates_pace(page: Page, static_server):
    page.goto(URL)
    page.locator("#tab-bar button[data-tab='time']").click()
    page.locator("#time-distance").select_option(label="Marathon")
    page.locator("#time-hr").fill("4")
    page.locator("#time-min").fill("22")

    expect(page.locator("#time-pace")).to_have_text("10:00")
    expect(page.locator("#time-speed")).to_have_text("6.0 mph")


def test_speed_tab_calculates_pace(page: Page, static_server):
    page.goto(URL)
    page.locator("#tab-bar button[data-tab='speed']").click()
    page.locator("#speed-input").fill("6")

    expect(page.locator("#speed-pace")).to_have_text("10:00")
    expect(page.locator("#speed-alt")).to_have_text("9.7 km/h")

