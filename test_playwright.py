from percy import percy_snapshot


def test_failed(page):
    page.goto("https://www.google.com")
    assert "Bing" in page.title()


def test_passed(page):
    page.goto("https://www.google.com")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    percy_snapshot(page, name="Google_Test")  # Percy snapshot
    assert "Google" in page.title()
