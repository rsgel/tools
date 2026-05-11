"""Tests for tip-calculator.html"""
from playwright.sync_api import Page, expect


URL = "http://127.0.0.1:8123/tip-calculator.html"


def test_initial_state(page: Page, static_server):
    page.goto(URL)
    expect(page.locator("h1")).to_have_text("Tip Calculator")
    expect(page.locator("#tipAmount")).to_have_text("$0.00")
    expect(page.locator("#totalAmount")).to_have_text("$0.00")
    expect(page.locator("#perPerson")).to_have_text("$0.00")


def test_calculates_tip_and_split(page: Page, static_server):
    page.goto(URL)
    page.locator("#billAmount").fill("100")
    page.locator("#tipPercent").fill("20")
    page.locator("#numPeople").fill("4")

    expect(page.locator("#tipAmount")).to_have_text("$20.00")
    expect(page.locator("#totalAmount")).to_have_text("$120.00")
    expect(page.locator("#perPerson")).to_have_text("$30.00")


def test_tip_preset_button_updates_percentage(page: Page, static_server):
    page.goto(URL)
    page.locator("#billAmount").fill("80")
    page.locator(".tip-buttons button[data-tip='25']").click()

    expect(page.locator("#tipPercent")).to_have_value("25")
    expect(page.locator(".tip-buttons button[data-tip='25']")).to_have_attribute("aria-pressed", "true")
    expect(page.locator("#tipAmount")).to_have_text("$20.00")

