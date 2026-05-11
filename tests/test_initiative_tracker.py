"""Tests for initiative-tracker.html"""
from playwright.sync_api import Page, expect


URL = "http://127.0.0.1:8123/initiative-tracker.html"


def test_initial_state(page: Page, static_server):
    page.goto(URL)
    expect(page.locator("h1")).to_have_text("Initiative Tracker")
    expect(page.locator("#empty-state")).to_be_visible()
    expect(page.locator("#controls")).not_to_be_visible()


def test_add_combatant_shows_controls(page: Page, static_server):
    page.goto(URL)
    page.locator("#name-input").fill("Goblin")
    page.locator("#init-input").fill("14")
    page.locator("#hp-input").fill("7")
    page.locator("#add-form button[type='submit']").click()

    expect(page.locator(".combatant")).to_have_count(1)
    expect(page.locator(".combatant")).to_contain_text("Goblin")
    expect(page.locator(".initiative-badge")).to_have_text("14")
    expect(page.locator("#controls")).to_be_visible()


def test_combatants_sort_by_initiative(page: Page, static_server):
    page.goto(URL)
    page.locator("#name-input").fill("Slow")
    page.locator("#init-input").fill("5")
    page.locator("#add-form button[type='submit']").click()
    page.locator("#name-input").fill("Fast")
    page.locator("#init-input").fill("18")
    page.locator("#add-form button[type='submit']").click()

    expect(page.locator(".combatant").first).to_contain_text("Fast")


def test_next_turn_advances_round(page: Page, static_server):
    page.goto(URL)
    page.locator("#name-input").fill("Hero")
    page.locator("#init-input").fill("10")
    page.locator("#add-form button[type='submit']").click()
    page.locator("#next-btn").click()

    expect(page.locator("#round-display")).to_have_text("Round 2")

