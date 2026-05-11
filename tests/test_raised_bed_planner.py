"""Tests for raised-bed-planner.html"""
from playwright.sync_api import Page, expect


URL = "http://127.0.0.1:8123/raised-bed-planner.html"


def test_initial_state(page: Page, static_server):
    page.goto(URL)
    expect(page.locator("h1")).to_have_text("Raised Bed Planner")
    expect(page.locator(".bed-cell")).to_have_count(16)
    expect(page.locator("#summary")).to_contain_text("No plants placed yet.")


def test_apply_changes_grid_size(page: Page, static_server):
    page.goto(URL)
    page.locator("#bedW").fill("2")
    page.locator("#bedH").fill("3")
    page.locator("#applyBtn").click()

    expect(page.locator(".bed-cell")).to_have_count(6)


def test_place_plant_updates_grid_and_summary(page: Page, static_server):
    page.goto(URL)
    page.locator(".pal-btn[data-id='tomato']").click()
    page.locator(".bed-cell").first.click()

    expect(page.locator(".bed-cell").first).to_contain_text("Tomato")
    expect(page.locator("#summary")).to_contain_text("Tomato")
    expect(page.locator("#summary")).to_contain_text("1 of 16 squares used")


def test_export_markdown_includes_planted_crop(page: Page, static_server):
    page.goto(URL)
    page.locator(".pal-btn[data-id='tomato']").click()
    page.locator(".bed-cell").first.click()

    markdown = page.evaluate("exportMarkdown()")
    assert "Raised Bed Layout" in markdown
    assert "Tomato" in markdown

