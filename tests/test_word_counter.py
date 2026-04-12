"""Tests for word-counter.html"""
from playwright.sync_api import Page, expect


def test_initial_state(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/word-counter.html")
    expect(page.locator("h1")).to_have_text("Word Counter")


def test_counts_words(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/word-counter.html")
    page.locator("#text-input").fill("Hello world this is a test")
    expect(page.locator("#word-count")).to_have_text("6")
    expect(page.locator("#char-count")).to_have_text("26")
