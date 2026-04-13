"""Tests for ultra-race-planner.html"""
from playwright.sync_api import Page, expect


URL = "http://127.0.0.1:8123/ultra-race-planner.html"


def test_initial_state(page: Page, static_server):
    page.goto(URL)
    expect(page.locator("h1")).to_have_text("Ultra Race Planner")


def test_tab_switching(page: Page, static_server):
    page.goto(URL)
    # Click each tab and verify its panel is visible
    for tab_id in ["stations", "inventory", "segments", "dashboard", "export"]:
        page.click(f"button[data-tab='{tab_id}']")
        expect(page.locator(f"#tab-{tab_id}")).to_have_class("tab-panel active")
    # Switch back to setup
    page.click("button[data-tab='setup']")
    expect(page.locator("#tab-setup")).to_have_class("tab-panel active")


def test_race_setup_fields(page: Page, static_server):
    page.goto(URL)
    page.fill("#race-name", "Western States 100")
    page.fill("#race-distance", "100.2")
    page.fill("#race-goal-time", "24:00:00")
    expect(page.locator("#race-name")).to_have_value("Western States 100")
    expect(page.locator("#race-distance")).to_have_value("100.2")
    expect(page.locator("#race-goal-time")).to_have_value("24:00:00")


def test_nutrition_targets(page: Page, static_server):
    page.goto(URL)
    page.fill("#target-carbs", "80")
    page.fill("#target-sodium", "700")
    page.fill("#target-caffeine", "50")
    expect(page.locator("#target-carbs")).to_have_value("80")
    expect(page.locator("#target-sodium")).to_have_value("700")
    expect(page.locator("#target-caffeine")).to_have_value("50")


def test_add_aid_station(page: Page, static_server):
    page.goto(URL)
    page.click("button[data-tab='stations']")
    page.click("#add-station-btn")
    # Should show a table row
    rows = page.locator("#stations-list table tbody tr")
    expect(rows).to_have_count(1)
    # Empty state should be hidden
    expect(page.locator("#stations-empty")).not_to_be_visible()


def test_add_multiple_stations(page: Page, static_server):
    page.goto(URL)
    page.click("button[data-tab='stations']")
    page.click("#add-station-btn")
    page.click("#add-station-btn")
    page.click("#add-station-btn")
    rows = page.locator("#stations-list table tbody tr")
    expect(rows).to_have_count(3)


def test_edit_aid_station(page: Page, static_server):
    page.goto(URL)
    page.click("button[data-tab='stations']")
    page.click("#add-station-btn")
    row = page.locator("#stations-list table tbody tr").first
    row.locator("input[data-field='name']").fill("Robinson Flat")
    row.locator("input[data-field='distance']").fill("30.3")
    expect(row.locator("input[data-field='name']")).to_have_value("Robinson Flat")
    expect(row.locator("input[data-field='distance']")).to_have_value("30.3")


def test_remove_aid_station(page: Page, static_server):
    page.goto(URL)
    page.click("button[data-tab='stations']")
    page.click("#add-station-btn")
    page.click("#add-station-btn")
    # Remove first station
    page.locator("#stations-list table tbody tr").first.locator("button[data-action='remove']").click()
    rows = page.locator("#stations-list table tbody tr")
    expect(rows).to_have_count(1)


def test_toggle_crew_access(page: Page, static_server):
    page.goto(URL)
    page.click("button[data-tab='stations']")
    page.click("#add-station-btn")
    toggle = page.locator("#stations-list .toggle-btn[data-field='crewAccess']").first
    expect(toggle).to_have_text("No")
    toggle.click()
    expect(toggle).to_have_text("Yes")
    expect(toggle).to_have_class("toggle-btn on")


def test_toggle_drop_bag_shows_contents(page: Page, static_server):
    page.goto(URL)
    page.click("button[data-tab='stations']")
    page.click("#add-station-btn")
    toggle = page.locator("#stations-list .toggle-btn[data-field='hasDropBag']").first
    toggle.click()
    # Should show drop bag contents row
    expect(page.locator(".dropbag-row")).to_have_count(1)


def test_add_product(page: Page, static_server):
    page.goto(URL)
    page.click("button[data-tab='inventory']")
    page.click("#add-product-btn")
    rows = page.locator("#products-list table tbody tr")
    expect(rows).to_have_count(1)
    expect(page.locator("#products-empty")).not_to_be_visible()


def test_edit_product(page: Page, static_server):
    page.goto(URL)
    page.click("button[data-tab='inventory']")
    page.click("#add-product-btn")
    row = page.locator("#products-list table tbody tr").first
    row.locator("input[data-field='name']").fill("SiS Beta Fuel Gel")
    row.locator("input[data-field='carbsPerServing']").fill("40")
    row.locator("input[data-field='sodiumPerServing']").fill("20")
    row.locator("input[data-field='caffeinePerServing']").fill("75")
    row.locator("input[data-field='caloriesPerServing']").fill("160")
    expect(row.locator("input[data-field='name']")).to_have_value("SiS Beta Fuel Gel")
    expect(row.locator("input[data-field='carbsPerServing']")).to_have_value("40")


def test_remove_product(page: Page, static_server):
    page.goto(URL)
    page.click("button[data-tab='inventory']")
    page.click("#add-product-btn")
    page.click("#add-product-btn")
    page.locator("#products-list table tbody tr").first.locator("button[data-action='remove']").click()
    rows = page.locator("#products-list table tbody tr")
    expect(rows).to_have_count(1)


def test_segments_generated(page: Page, static_server):
    page.goto(URL)
    # Set up race
    page.fill("#race-distance", "100")
    page.fill("#race-goal-time", "24:00:00")
    # Add an aid station
    page.click("button[data-tab='stations']")
    page.click("#add-station-btn")
    row = page.locator("#stations-list table tbody tr").first
    row.locator("input[data-field='name']").fill("Halfway")
    row.locator("input[data-field='distance']").fill("50")
    # Switch to segments tab
    page.click("button[data-tab='segments']")
    # Should have 2 segment cards (Start→Halfway, Halfway→Finish)
    expect(page.locator(".segment-card")).to_have_count(2)


def test_segment_shows_distance_and_time(page: Page, static_server):
    page.goto(URL)
    page.fill("#race-distance", "100")
    page.fill("#race-goal-time", "24:00:00")
    page.click("button[data-tab='stations']")
    page.click("#add-station-btn")
    row = page.locator("#stations-list table tbody tr").first
    row.locator("input[data-field='name']").fill("Halfway")
    row.locator("input[data-field='distance']").fill("50")
    page.click("button[data-tab='segments']")
    first_card = page.locator(".segment-card").first
    expect(first_card).to_contain_text("50 mi")
    expect(first_card).to_contain_text("12:00")


def test_add_nutrition_to_segment(page: Page, static_server):
    page.goto(URL)
    page.fill("#race-distance", "100")
    page.fill("#race-goal-time", "24:00:00")
    # Add a product
    page.click("button[data-tab='inventory']")
    page.click("#add-product-btn")
    row = page.locator("#products-list table tbody tr").first
    row.locator("input[data-field='name']").fill("Gel")
    row.locator("input[data-field='carbsPerServing']").fill("25")
    row.locator("input[data-field='caloriesPerServing']").fill("100")
    # Add an aid station
    page.click("button[data-tab='stations']")
    page.click("#add-station-btn")
    page.locator("#stations-list table tbody tr").first.locator("input[data-field='name']").fill("Mid")
    page.locator("#stations-list table tbody tr").first.locator("input[data-field='distance']").fill("50")
    # Go to segments tab
    page.click("button[data-tab='segments']")
    first_card = page.locator(".segment-card").first
    # Add a planned nutrition item
    first_card.locator("button[data-action='add-item'][data-list='plannedNutrition']").click()
    # Select the product
    first_card.locator(".nutrition-row select").first.select_option(label="Gel")
    first_card.locator(".nutrition-row input[data-field='quantity']").first.fill("4")
    # Should show carbs total = 100g
    expect(first_card).to_contain_text("100g")


def test_dashboard_shows_summary(page: Page, static_server):
    page.goto(URL)
    page.fill("#race-name", "Test Race")
    page.fill("#race-distance", "50")
    page.fill("#race-goal-time", "10:00:00")
    page.click("button[data-tab='dashboard']")
    expect(page.locator(".dashboard-inner")).to_be_visible()
    expect(page.locator(".dashboard-inner")).to_contain_text("50 mi")
    expect(page.locator(".dashboard-inner")).to_contain_text("10:00:00")


def test_export_buttons_exist(page: Page, static_server):
    page.goto(URL)
    page.click("button[data-tab='export']")
    expect(page.locator("#export-yaml-btn")).to_be_visible()
    expect(page.locator("#export-md-btn")).to_be_visible()


def test_yaml_import_zone_exists(page: Page, static_server):
    page.goto(URL)
    page.click("button[data-tab='export']")
    expect(page.locator("#yaml-drop-zone")).to_be_visible()


def test_markdown_export_content(page: Page, static_server):
    page.goto(URL)
    page.fill("#race-name", "Western States")
    page.fill("#race-distance", "100")
    page.fill("#race-goal-time", "24:00:00")
    page.fill("#target-carbs", "80")
    # Add a station
    page.click("button[data-tab='stations']")
    page.click("#add-station-btn")
    page.locator("#stations-list table tbody tr").first.locator("input[data-field='name']").fill("Robinson Flat")
    page.locator("#stations-list table tbody tr").first.locator("input[data-field='distance']").fill("30.3")
    # Switch to segments to generate them
    page.click("button[data-tab='segments']")
    # Get markdown content via JS
    md = page.evaluate("generateMarkdown()")
    assert "Western States" in md
    assert "100 miles" in md
    assert "24:00:00" in md
    assert "Robinson Flat" in md
    assert "30.3" in md
    assert "Carbs" in md


def test_gpx_drop_zone_exists(page: Page, static_server):
    page.goto(URL)
    expect(page.locator("#gpx-drop-zone")).to_be_visible()


def test_empty_states_shown(page: Page, static_server):
    page.goto(URL)
    page.click("button[data-tab='stations']")
    expect(page.locator("#stations-empty")).to_be_visible()
    page.click("button[data-tab='inventory']")
    expect(page.locator("#products-empty")).to_be_visible()
