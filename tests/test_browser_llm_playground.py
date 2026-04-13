"""Tests for browser-llm-playground.html"""
from playwright.sync_api import Page, expect


def test_initial_state(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/browser-llm-playground.html")
    expect(page.locator("h1")).to_have_text("Browser LLM Playground")
    expect(page.locator("#load-button")).to_have_text("Load model")
    expect(page.locator("#run-button")).to_be_disabled()
    expect(page.locator("#status-box")).to_have_text("Waiting to load a model.")
    expect(page.locator("#raw-toggle")).to_have_text("Raw")


def test_capability_labels_and_model_options(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/browser-llm-playground.html")
    expect(page.locator("#capability-summary")).to_contain_text("browser")
    expect(page.locator("#model-select")).to_contain_text("Qwen2 0.5B Instruct")
    expect(page.locator("#model-select")).to_contain_text("Qwen2 1.5B Instruct")
    expect(page.locator("#custom-model")).to_have_attribute(
        "placeholder",
        "Leave blank to use the suggested model",
    )


def test_raw_toggle_switches_label(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/browser-llm-playground.html")
    toggle = page.locator("#raw-toggle")
    expect(toggle).to_have_text("Raw")
    toggle.click()
    expect(toggle).to_have_text("Rendered")
    expect(page.locator("#response-box")).to_have_class("response-box raw")
    toggle.click()
    expect(toggle).to_have_text("Raw")
