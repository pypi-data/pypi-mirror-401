"""Browser capture module using Playwright."""

import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, Page


VIDEOS_DIR = Path(__file__).parent.parent / "videos"
VIDEOS_DIR.mkdir(exist_ok=True)


async def capture_browser_session(
    url: str,
    mode: str = "manual",
    timeout_seconds: int = 180,
) -> str:
    """
    Launch browser, capture video of session, return video path.

    Args:
        url: URL to navigate to
        mode: "manual" (user browses) or "auto" (automated exploration)
        timeout_seconds: How long to wait in manual mode

    Returns:
        Path to the recorded video file
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(VIDEOS_DIR),
            record_video_size={"width": 1920, "height": 1080},
        )

        page = await context.new_page()
        await page.goto(url)

        if mode == "manual":
            # User browses manually - wait for timeout
            try:
                await asyncio.wait_for(
                    page.wait_for_timeout(timeout_seconds * 1000),
                    timeout=timeout_seconds + 5,
                )
            except asyncio.TimeoutError:
                pass
        else:
            await _auto_explore(page)

        video_path = await page.video.path()
        await context.close()
        await browser.close()

        return video_path


async def _auto_explore(page: Page) -> None:
    """Automatically explore the page."""
    # Scroll through the page
    await page.evaluate(
        """async () => {
            const scroll = async () => {
                window.scrollBy(0, window.innerHeight);
                await new Promise(r => setTimeout(r, 500));
                if (window.scrollY + window.innerHeight < document.body.scrollHeight) {
                    await scroll();
                }
            };
            await scroll();
        }"""
    )
    await page.wait_for_timeout(1000)

    # Try clicking navigation links
    nav_selectors = ["nav a", "header a", ".nav-link", "[role='navigation'] a"]

    for selector in nav_selectors:
        try:
            links = await page.query_selector_all(selector)
            for link in links[:3]:  # Click up to 3 links
                try:
                    await link.click()
                    await page.wait_for_timeout(1000)
                except Exception:
                    pass
        except Exception:
            pass


if __name__ == "__main__":
    # Quick test
    asyncio.run(capture_browser_session("https://example.com", mode="manual"))
