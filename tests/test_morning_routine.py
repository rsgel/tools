"""Tests for morning-routine.html"""
from playwright.sync_api import Page, expect


def test_initial_state(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/morning-routine.html")
    expect(page.locator("h1")).to_have_text("Morning Routine Simulator")


def test_default_profiles_exist(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/morning-routine.html")
    # Clear localStorage first to get defaults
    page.evaluate("localStorage.clear()")
    page.reload()
    profile_buttons = page.locator("#profile-bar button:not(.add-profile)")
    expect(profile_buttons).to_have_count(2)
    expect(profile_buttons.nth(0)).to_have_text("Commute Day")
    expect(profile_buttons.nth(1)).to_have_text("WFH Day")


def test_wake_time_calculates(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/morning-routine.html")
    page.evaluate("localStorage.clear()")
    page.reload()
    # Default deadline is 09:00, default blocks sum should produce a wake time
    wake_text = page.locator("#wake-time").text_content()
    assert wake_text != "—", "Wake time should be calculated"
    assert "AM" in wake_text or "PM" in wake_text, "Wake time should show AM/PM"


def test_deadline_change_updates_wake(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/morning-routine.html")
    page.evaluate("localStorage.clear()")
    page.reload()
    wake_before = page.locator("#wake-time").text_content()
    page.fill("#deadline-input", "10:00")
    page.locator("#deadline-input").dispatch_event("input")
    wake_after = page.locator("#wake-time").text_content()
    assert wake_before != wake_after, "Wake time should change when deadline changes"


def test_toggle_block_off(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/morning-routine.html")
    page.evaluate("localStorage.clear()")
    page.reload()
    wake_before = page.locator("#wake-time").text_content()
    # Toggle off the first block checkbox
    first_toggle = page.locator(".block-toggle").first
    first_toggle.uncheck()
    wake_after = page.locator("#wake-time").text_content()
    assert wake_before != wake_after, "Wake time should change when a block is toggled off"


def test_add_block(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/morning-routine.html")
    page.evaluate("localStorage.clear()")
    page.reload()
    initial_count = page.locator(".block-item").count()
    page.fill("#new-block-name", "Yoga")
    page.click("#add-block-btn")
    expect(page.locator(".block-item")).to_have_count(initial_count + 1)


def test_delete_block(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/morning-routine.html")
    page.evaluate("localStorage.clear()")
    page.reload()
    initial_count = page.locator(".block-item").count()
    page.locator(".block-delete").first.click()
    expect(page.locator(".block-item")).to_have_count(initial_count - 1)


def test_sleep_calculator(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/morning-routine.html")
    page.evaluate("localStorage.clear()")
    page.reload()
    page.fill("#sleep-hours", "8")
    page.locator("#sleep-hours").dispatch_event("input")
    bedtime_text = page.locator("#bedtime-display").text_content()
    assert "Bedtime:" in bedtime_text, "Should display bedtime when sleep hours set"


def test_switch_profile(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/morning-routine.html")
    page.evaluate("localStorage.clear()")
    page.reload()
    # Click second profile tab
    page.locator("#profile-bar button:not(.add-profile)").nth(1).click()
    # Check that active profile changed - WFH Day has 09:30 deadline
    expect(page.locator("#deadline-input")).to_have_value("09:30")


def test_weekly_view_toggle(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/morning-routine.html")
    page.click("#view-toggle button[data-view='weekly']")
    expect(page.locator("#weekly-view")).to_have_class("weekly-section active")
    expect(page.locator("#daily-view")).not_to_have_class("daily-section active")


def test_timeline_rendered(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/morning-routine.html")
    page.evaluate("localStorage.clear()")
    page.reload()
    # Timeline should have segments for each block
    segments = page.locator(".timeline-segment")
    assert segments.count() > 0, "Timeline should have segments"
    # Should have wake and deadline boundaries
    expect(page.locator(".wake-boundary")).to_be_visible()
    expect(page.locator(".deadline-boundary")).to_be_visible()


def test_total_duration_displayed(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/morning-routine.html")
    page.evaluate("localStorage.clear()")
    page.reload()
    total_text = page.locator("#total-duration").text_content()
    assert total_text.endswith("total"), "Should display total duration with 'total' suffix"
    assert "min" in total_text or "h" in total_text, "Should include time unit"


def test_slider_updates_wake_time(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/morning-routine.html")
    page.evaluate("localStorage.clear()")
    page.reload()
    wake_before = page.locator("#wake-time").text_content()
    # Set slider to minimum value
    first_slider = page.locator(".block-slider-row input[type='range']").first
    first_slider.fill("5")
    first_slider.dispatch_event("input")
    wake_after = page.locator("#wake-time").text_content()
    assert wake_before != wake_after, "Wake time should update when slider changes"
