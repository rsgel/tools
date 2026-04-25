"""Tests for running-planner.html"""
from playwright.sync_api import Page, expect


def open_planner(page: Page):
    page.goto("http://127.0.0.1:8123/running-planner.html")
    page.evaluate("localStorage.clear()")
    page.reload()


def save_workout(page: Page, day_index: int, text: str):
    day = page.locator(f'.day-cell[data-index="{day_index}"]')
    day.click()
    day.locator("input").fill(text)
    day.locator("input").press("Enter")
    return day


def test_initial_state(page: Page, static_server):
    open_planner(page)
    expect(page.locator("h1")).to_have_text("Running Planner")
    expect(page.locator(".day-cell")).to_have_count(7)


def test_editing_existing_typed_run_does_not_duplicate_type(page: Page, static_server):
    open_planner(page)

    day = save_workout(page, 0, "10 long run")
    expect(day.locator(".workout-type-pill")).to_have_text("Long Run")
    expect(day.locator(".workout-distance")).to_contain_text("10")
    expect(day.locator(".workout-notes")).to_have_count(0)

    for _ in range(2):
        day.click()
        expect(day.locator("input")).to_have_value("10mi long run")
        day.locator("input").press("Enter")
        expect(day.locator(".workout-type-pill")).to_have_text("Long Run")
        expect(day.locator(".workout-notes")).to_have_count(0)


def test_editing_existing_run_keeps_real_notes_once(page: Page, static_server):
    open_planner(page)

    day = save_workout(page, 1, "8 easy strides")
    expect(day.locator(".workout-type-pill")).to_have_text("Easy")
    expect(day.locator(".workout-notes")).to_have_text("strides")

    day.click()
    expect(day.locator("input")).to_have_value("8mi easy strides")
    day.locator("input").press("Enter")

    expect(day.locator(".workout-type-pill")).to_have_text("Easy")
    expect(day.locator(".workout-notes")).to_have_text("strides")