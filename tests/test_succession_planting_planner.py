"""Tests for succession-planting-planner.html"""
from playwright.sync_api import Page, expect


def test_initial_state(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    expect(page.locator("h1")).to_have_text("Succession Planting Planner")


def test_default_frost_dates(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    last_frost = page.locator("#last-frost")
    first_frost = page.locator("#first-frost")
    # Should have default PNW dates (April 15 and Oct 20 of current year)
    expect(last_frost).not_to_have_value("")
    expect(first_frost).not_to_have_value("")


def test_crops_preselected(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    selected = page.locator(".crop-btn.selected")
    # First 8 crops should be pre-selected
    expect(selected).to_have_count(8)


def test_select_all(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    page.click("#select-all-btn")
    selected = page.locator(".crop-btn.selected")
    total = page.locator(".crop-btn")
    expect(selected).to_have_count(16)
    expect(total).to_have_count(16)


def test_clear_selection(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    page.click("#clear-btn")
    selected = page.locator(".crop-btn.selected")
    expect(selected).to_have_count(0)


def test_toggle_crop(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    page.click("#clear-btn")
    # Click lettuce (first crop)
    first_crop = page.locator(".crop-btn").first
    first_crop.click()
    expect(first_crop).to_have_class("crop-btn selected")
    # Click again to deselect
    first_crop.click()
    expect(first_crop).to_have_class("crop-btn")


def test_generate_schedule(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    page.click("#clear-btn")
    # Select just lettuce
    page.locator(".crop-btn").first.click()
    page.click("#generate-btn")
    results = page.locator("#results")
    expect(results).to_have_class("results visible")
    # Should show a crop schedule card
    expect(page.locator(".crop-schedule")).to_have_count(1)
    expect(page.locator(".crop-schedule h3")).to_contain_text("Lettuce")


def test_generate_multiple_crops(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    # Default has 8 selected, generate
    page.click("#generate-btn")
    expect(page.locator(".crop-schedule")).to_have_count(8)


def test_sowing_table_has_rows(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    page.click("#clear-btn")
    page.locator(".crop-btn").first.click()
    page.click("#generate-btn")
    # Lettuce should have multiple sowing rows
    rows = page.locator(".sow-table tbody tr")
    count = rows.count()
    assert count >= 3, f"Expected at least 3 sowings for lettuce, got {count}"


def test_summary_bar_shows(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    page.click("#generate-btn")
    summary = page.locator("#summary-bar")
    expect(summary).to_contain_text("crops selected")
    expect(summary).to_contain_text("total sowings")


def test_no_generate_without_selection(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    page.click("#clear-btn")
    page.click("#generate-btn")
    # Results should not be visible
    results = page.locator("#results")
    expect(results).not_to_have_class("results visible")


def test_gap_shown_for_lettuce(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    page.click("#clear-btn")
    page.locator(".crop-btn").first.click()
    page.click("#generate-btn")
    # Lettuce has a midsummer gap
    gap = page.locator(".gap-region")
    expect(gap).to_have_count(1)
    expect(page.locator(".gap-label")).to_have_text("too hot")


def test_no_gap_for_carrots(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    page.click("#clear-btn")
    # Carrots is the 7th crop (index 6)
    page.locator(".crop-btn").nth(6).click()
    page.click("#generate-btn")
    gap = page.locator(".gap-region")
    expect(gap).to_have_count(0)


def test_crop_note_displayed(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/succession-planting-planner.html")
    page.click("#clear-btn")
    page.locator(".crop-btn").first.click()
    page.click("#generate-btn")
    note = page.locator(".crop-note")
    expect(note).to_have_count(1)
    expect(note).to_contain_text("bolts")
