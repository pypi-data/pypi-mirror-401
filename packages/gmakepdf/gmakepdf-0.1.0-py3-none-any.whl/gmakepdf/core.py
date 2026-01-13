# core.py
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser
from threading import Lock

# -------------------------
# Global browser (singleton)
# -------------------------
_playwright = None
_browser: Browser | None = None
_lock = Lock()


def _get_browser() -> Browser:
    """
    Start Playwright + Chromium once and reuse it.
    Thread-safe.
    """
    global _playwright, _browser

    if _browser is None:
        with _lock:
            if _browser is None:  # double-check
                _playwright = sync_playwright().start()
                _browser = _playwright.chromium.launch(headless=True)
    return _browser


# -------------------------
# Core functions
# -------------------------
def html_to_pdf(html: str) -> bytes:
    """
    Convert HTML string to PDF bytes.
    Browser is reused after first call.
    """
    if not html or not html.strip():
        raise ValueError("HTML content is empty")

    browser = _get_browser()
    page = browser.new_page()

    try:
        page.set_content(html, wait_until="load")
        pdf_bytes = page.pdf(format="A4", print_background=True)
        return pdf_bytes
    finally:
        page.close()


def html_file_to_pdf(input_path: str, output_path: str):
    """
    Convert HTML file to PDF file.
    Raises clear errors if file does not exist.
    """
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"HTML source file not found: {input_path}")

    if not input_file.is_file():
        raise ValueError(f"Input path is not a file: {input_path}")

    html = input_file.read_text(encoding="utf-8")

    pdf_bytes = html_to_pdf(html)

    output_file = Path(output_path)
    output_file.write_bytes(pdf_bytes)
