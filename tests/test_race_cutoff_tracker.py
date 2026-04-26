"""Tests for race-cutoff-tracker.html"""
from playwright.sync_api import Page, expect


URL = "http://127.0.0.1:8123/race-cutoff-tracker.html"


def open_tracker(page: Page):
    page.goto(URL)
    page.evaluate("localStorage.clear()")
    page.reload()


def add_station(page: Page, name: str, distance: str, cutoff: str, actual: str = ""):
    page.click("#add-station-btn")
    row = page.locator("#station-rows tr").last
    row.locator("input[data-field='name']").fill(name)
    row.locator("input[data-field='distance']").fill(distance)
    row.locator("input[data-field='cutoff']").fill(cutoff)
    page.click("#edit-stations-btn")
    row = page.locator("#station-rows tr").last
    if actual:
        actual_input = row.locator("input[data-field='actual']")
        actual_input.fill(actual)
        actual_input.press("Tab")
        row = page.locator("#station-rows tr").last
    return row


def test_initial_state(page: Page, static_server):
    open_tracker(page)
    expect(page.locator("h1")).to_have_text("Race Cutoff Tracker")
    expect(page.locator("#empty-state")).to_be_visible()
    expect(page.locator("#paste-input")).not_to_be_visible()
    expect(page.locator("#edit-stations-btn")).to_be_visible()
    expect(page.locator("#stations-actions #add-station-btn")).to_be_visible()


def test_add_station_row(page: Page, static_server):
    open_tracker(page)
    page.click("#add-station-btn")
    expect(page.locator("#station-rows tr")).to_have_count(1)
    expect(page.locator("#edit-stations-btn")).to_have_text("Done Editing")
    expect(page.locator("#station-rows input[data-field='distance']")).to_be_visible()
    expect(page.locator("#empty-state")).not_to_be_visible()


def test_remove_station_lives_in_global_edit_mode(page: Page, static_server):
    open_tracker(page)
    add_station(page, "Ridge Aid", "12", "3:30")
    expect(page.locator("#station-rows button[data-action='remove']")).to_have_count(0)
    page.click("#edit-stations-btn")
    expect(page.locator("#station-rows button[data-action='remove']")).to_be_visible()


def test_distance_typing_is_not_replaced_by_rerender(page: Page, static_server):
    open_tracker(page)
    page.click("#add-station-btn")
    distance_input = page.locator("#station-rows input[data-field='distance']").last
    distance_input.type("15.8")
    expect(distance_input).to_have_value("15.8")


def test_elapsed_actual_margin(page: Page, static_server):
    open_tracker(page)
    row = add_station(page, "Ridge Aid", "12", "3:30", "3:05")
    expect(row.locator(".status-cell")).to_contain_text("25m ahead")
    expect(row.locator(".status-cell .pill")).to_have_class("pill pill-good")
    expect(row.locator(".pace-cell")).to_contain_text("15:25 / mi")


def test_predictions_show_recent_and_overall(page: Page, static_server):
    open_tracker(page)
    add_station(page, "Start", "0", "0:00", "0:00")
    add_station(page, "River", "10", "3:00", "2:00")
    future = add_station(page, "High Camp", "20", "5:00")
    expect(future.locator(".prediction-cell")).to_contain_text("Recent: 1h 0m ahead")
    expect(future.locator(".prediction-cell")).to_contain_text("Overall: 1h 0m ahead")
    expect(future.locator(".prediction-cell")).to_contain_text("ETA 4:00")
    expect(future.locator(".pace-cell")).to_contain_text("Recent 12:00 / mi")
    expect(future.locator(".pace-cell")).to_contain_text("Overall 12:00 / mi")


def test_paste_import_replaces_rows(page: Page, static_server):
    open_tracker(page)
    page.click("#paste-toggle")
    page.fill(
        "#paste-input",
        "Aid Station\tDistance\tCutoff\tActual\nStart\t0\t0:00\t0:00\nRidge\t12\t3:30\t3:05",
    )
    page.click("#import-btn")
    expect(page.locator("#station-rows tr")).to_have_count(2)
    expect(page.locator("#station-rows tr").nth(1)).to_contain_text("25m ahead")


def test_clock_mode_margin(page: Page, static_server):
    open_tracker(page)
    page.select_option("#time-mode", "clock")
    page.fill("#race-start-time", "06:00")
    row = add_station(page, "Meadow", "18", "12:00", "11:30")
    expect(row.locator(".status-cell")).to_contain_text("30m ahead")
    expect(row.locator(".status-cell")).to_contain_text("Arrived 11:30")


def test_sample_data_draws_chart(page: Page, static_server):
    open_tracker(page)
    page.click("#sample-btn")
    expect(page.locator("#station-rows tr")).to_have_count(5)
    expect(page.locator("#chart-empty")).not_to_be_visible()


def test_clear_resets_tracker(page: Page, static_server):
    open_tracker(page)
    add_station(page, "Ridge Aid", "12", "3:30", "3:05")
    page.click("#clear-btn")
    expect(page.locator("#station-rows tr")).to_have_count(0)
    expect(page.locator("#empty-state")).to_be_visible()


def test_mobile_viewport_does_not_overflow_page(page: Page, static_server):
    page.set_viewport_size({"width": 600, "height": 900})
    open_tracker(page)
    page.click("#sample-btn")
    overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
    assert overflow is False
