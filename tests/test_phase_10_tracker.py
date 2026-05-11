"""Tests for phase-10-tracker.html"""
from playwright.sync_api import Page, expect


URL = "http://127.0.0.1:8123/phase-10-tracker.html"


def test_initial_state(page: Page, static_server):
    page.goto(URL)
    expect(page.locator("h1")).to_have_text("Phase 10 Tracker")
    expect(page.locator(".player")).to_have_count(4)
    expect(page.locator(".player").first).to_contain_text("Player 1")


def test_advance_player_phase(page: Page, static_server):
    page.goto(URL)
    first_player = page.locator(".player").first
    first_player.locator("[data-action='plus']").click()

    expect(first_player.locator(".phase-number")).to_have_text("2")


def test_add_player(page: Page, static_server):
    page.goto(URL)
    page.locator("#add-player-btn").click()

    expect(page.locator(".player")).to_have_count(5)
    expect(page.locator(".player").last).to_contain_text("Player 5")


def test_score_tracking_toggle_shows_score_inputs(page: Page, static_server):
    page.goto(URL)
    page.locator("#track-scores-toggle").check()

    expect(page.locator(".score-input")).to_have_count(4)

