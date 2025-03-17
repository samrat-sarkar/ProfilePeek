import asyncio
import random
from pyppeteer import launch
from pyppeteer_stealth import stealth
from bs4 import BeautifulSoup

async def osint(target, debug=0):
    url = f'https://mastodon.social/@{target}'

    try:
        with open("ua.txt", "r", encoding="utf-8") as file:
            user_agents = [line.strip() for line in file if line.strip()]
        if user_agents:
            user_agent = random.choice(user_agents)
        else:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.71"
    except FileNotFoundError:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.71"

    browser = await launch(
        headless=True,
        executablePath ="C:/Program Files/Google/Chrome/Application/chrome.exe",
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )

    page = await browser.newPage()

    await stealth(page)

    await page.setUserAgent(user_agent)

    await page.evaluateOnNewDocument(
        "() => { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) }"
    )

    await page.goto(url, {"waitUntil": "domcontentloaded"})

    content = await page.content()
    await browser.close()

    soup = BeautifulSoup(content, 'html.parser')

    title = soup.title.string if soup.title else "N/A"
    body = soup.body.get_text(separator="\n", strip=True) if soup.body else "N/A"

    if debug == 1:
        print(f"Title:-->{title}<--")
        print(f"Body:-->{body}<--")

    try:
        with open("resources/mastodon/tags.txt", "r", encoding="utf-8") as file:
            titles = {line.strip() for line in file}

        if body.strip() in titles:
            return 404, None
        else:
            return 200, url

    except Exception as e:
        print(f"Error : {e}")

