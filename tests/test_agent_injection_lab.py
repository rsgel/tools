import pathlib
from playwright.sync_api import Page, expect
import pytest
from subprocess import Popen, PIPE
from http.client import HTTPConnection
import time

test_dir = pathlib.Path(__file__).parent.absolute()
root = test_dir.parent.absolute()

URL = "http://127.0.0.1:8123/agent-injection-lab.html"


@pytest.fixture(scope="module")
def static_server():
    process = Popen(
        ["python", "-m", "http.server", "8123", "--directory", root],
        stdout=PIPE
    )
    retries = 5
    while retries > 0:
        conn = HTTPConnection("127.0.0.1:8123")
        try:
            conn.request("HEAD", "/")
            conn.getresponse()
            yield process
            break
        except ConnectionRefusedError:
            time.sleep(1)
            retries -= 1
    process.terminate()
    process.wait()


@pytest.fixture(autouse=True)
def clear_storage(page: Page, static_server):
    # Start each test from a clean slate so localStorage results don't bleed over.
    page.goto(URL)
    page.evaluate("localStorage.clear()")
    page.reload()


def test_initial_state(page: Page, static_server):
    page.goto(URL)
    expect(page.locator(".appbar .logo")).to_contain_text("Acme Cloud")
    expect(page.locator("#total-count")).to_have_text("14")
    expect(page.locator("#fired-count")).to_have_text("0")
    expect(page.locator("#enabled-count")).to_have_text("14")


def test_input_token_fires_vector(page: Page, static_server):
    page.goto(URL)
    # CMNT-4417 is the HTML-comment vector's default token (sink: input).
    page.fill("#verify-code", "CMNT-4417")
    page.click("#verify-btn")
    expect(page.locator("#fired-count")).to_have_text("1")
    expect(page.locator("#verify-ok")).to_be_visible()


def test_honeypot_click_fires(page: Page, static_server):
    page.goto(URL)
    page.click("#honeypot-btn")
    expect(page.locator("#fired-count")).to_have_text("1")


def test_url_ack_fires_on_load(page: Page, static_server):
    # TINY-1093 is the 1px-font vector (sink: urlack).
    page.goto(URL + "?ack=TINY-1093")
    expect(page.locator("#fired-count")).to_have_text("1")


def test_disabled_vector_does_not_fire(page: Page, static_server):
    page.goto(URL)
    # Disable the first vector (HTML comment, token CMNT-4417) via its console checkbox.
    first_checkbox = page.locator("#vector-rows tr").first.locator("input[type=checkbox]")
    first_checkbox.uncheck()
    expect(page.locator("#enabled-count")).to_have_text("13")
    page.fill("#verify-code", "CMNT-4417")
    page.click("#verify-btn")
    # Token belongs to a disabled vector, so nothing should fire.
    expect(page.locator("#fired-count")).to_have_text("0")


def test_results_persist_across_reload(page: Page, static_server):
    page.goto(URL)
    page.click("#honeypot-btn")
    expect(page.locator("#fired-count")).to_have_text("1")
    page.reload()
    expect(page.locator("#fired-count")).to_have_text("1")


def test_reset_clears_results(page: Page, static_server):
    page.goto(URL)
    page.click("#honeypot-btn")
    expect(page.locator("#fired-count")).to_have_text("1")
    page.click("#reset-btn")
    expect(page.locator("#fired-count")).to_have_text("0")


def test_injected_comment_present_in_dom(page: Page, static_server):
    page.goto(URL)
    # The white-on-white vector (WHIT-8820) should be present in the document text content.
    html = page.content()
    assert "WHIT-8820" in html
    assert "CMNT-4417" in html  # inside an HTML comment node
