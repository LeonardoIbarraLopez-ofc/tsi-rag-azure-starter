import os

import pytest


pytestmark = pytest.mark.skipif(
    not os.getenv("E2E_BASE_URL"),
    reason="Defina E2E_BASE_URL con la API en ejecucion para habilitar Playwright.",
)


def test_main_flow():
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import sync_playwright

    base_url = os.environ["E2E_BASE_URL"]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(base_url)
        page.fill("#query", "¿Como deben gestionarse los secretos?")
        page.click("#ask")
        page.wait_for_function("document.querySelector('#answer').textContent !== 'Consultando...'")
        answer = page.locator("#answer").inner_text()
        meta = page.locator("#meta").inner_text()
        assert len(answer) > 20
        assert "Fuentes:" in meta
        browser.close()
