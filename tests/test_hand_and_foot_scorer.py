"""Tests for hand-and-foot-scorer.html"""
from playwright.sync_api import Page, expect


URL = "http://127.0.0.1:8123/hand-and-foot-scorer.html"


def test_initial_state(page: Page, static_server):
    page.goto(URL)
    expect(page.locator("h1")).to_have_text("Hand and Foot Scorer")


def test_two_teams_displayed(page: Page, static_server):
    page.goto(URL)
    expect(page.locator("#team-0")).to_be_visible()
    expect(page.locator("#team-1")).to_be_visible()


def test_scoreboard_shows_zeros(page: Page, static_server):
    page.goto(URL)
    rows = page.locator("#scoreboard-body tr")
    expect(rows).to_have_count(2)
    expect(rows.nth(0)).to_contain_text("Team 1")
    expect(rows.nth(1)).to_contain_text("Team 2")


def test_submit_round_updates_scoreboard(page: Page, static_server):
    page.goto(URL)
    panel = page.locator("#team-0")
    # Enter 1 red book = 500 points
    panel.locator("input[data-key='red']").fill("1")
    panel.locator("button[data-action='submit']").click()
    # Scoreboard should show 500 for R1
    row = page.locator("#scoreboard-body tr").nth(0)
    expect(row).to_contain_text("500")


def test_edit_button_re_enables_inputs(page: Page, static_server):
    page.goto(URL)
    panel = page.locator("#team-0")
    panel.locator("input[data-key='red']").fill("1")
    panel.locator("button[data-action='submit']").click()
    # Input should be disabled
    expect(panel.locator("input[data-key='red']")).to_be_disabled()
    # Click edit
    panel.locator("button[data-action='edit']").click()
    expect(panel.locator("input[data-key='red']")).to_be_enabled()


def test_round_tabs_switch(page: Page, static_server):
    page.goto(URL)
    panel = page.locator("#team-0")
    # Click round 2 tab
    panel.locator("button.round-tab", has_text="R2").click()
    # Should show meld 90
    expect(panel.locator(".meld-req")).to_contain_text("90")


def test_scoring_calculation(page: Page, static_server):
    page.goto(URL)
    panel = page.locator("#team-0")
    # 1 sevens book = 5000
    panel.locator("input[data-key='sevens']").fill("1")
    # 200 melded card points
    panel.locator("input[data-cat='meldedCards']").fill("200")
    # Going out bonus
    panel.locator("button[data-toggle='goingOut']").click()
    # Live score should be 5000 + 200 + 100 = 5300
    expect(panel.locator(".live-score")).to_contain_text("5,300")


def test_penalty_scoring(page: Page, static_server):
    page.goto(URL)
    panel = page.locator("#team-0")
    # 2 black threes = -200
    panel.locator("input[data-key='blackThrees']").fill("2")
    expect(panel.locator(".live-score")).to_contain_text("-200")


def test_rules_toggle(page: Page, static_server):
    page.goto(URL)
    rules = page.locator("#rules-content")
    expect(rules).not_to_be_visible()
    page.locator("#rules-toggle").click()
    expect(rules).to_be_visible()


def test_red_threes_bonus_with_all_seven(page: Page, static_server):
    page.goto(URL)
    panel = page.locator("#team-0")
    # 7 red threes = 700 + 300 extra = 1000
    panel.locator("input[data-cat='bonuses'][data-key='redThrees']").fill("7")
    expect(panel.locator(".live-score")).to_contain_text("1,000")
