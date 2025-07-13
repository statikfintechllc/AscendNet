from scraper.playwright_handler import get_dom_tree


def run_crash_scraper():
    html = get_dom_tree("https://unstable.example.com")
    if not html:
        raise RuntimeError("DOM is empty, crash triggered")
    return html
