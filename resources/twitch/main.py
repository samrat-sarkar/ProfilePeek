import asyncio
import os
import random
import shutil
from pyppeteer import launch
from pyppeteer_stealth import stealth
from bs4 import BeautifulSoup

async def osint(target, debug=0):
    url = f'https://www.twitch.tv/{target}'

    try:
        with open("ua.txt", "r", encoding="utf-8") as file:
            user_agents = [line.strip() for line in file if line.strip()]
        if user_agents:
            user_agent = random.choice(user_agents)
        else:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.71"
    except FileNotFoundError:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.71"

    paths = [
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    ]

    chrome_path = next((path for path in paths if os.path.exists(path)), None)
    if not chrome_path:
        chrome_path = shutil.which("chrome") or shutil.which("chrome.exe")

    if not chrome_path:
        print("❌ Google Chrome Not Found")
        exit()

    browser = await launch(
        headless=True,
        executablePath=chrome_path,
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )

    page = await browser.newPage()

    await stealth(page)

    await page.setUserAgent(user_agent)

    await page.evaluateOnNewDocument(
        "() => { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }) }"
    )

    await page.goto(url, {"waitUntil": "networkidle0", "timeout": 60000})


    content = await page.content()
    await browser.close()

    soup = BeautifulSoup(content, 'html.parser')

    title = soup.title.string if soup.title else "N/A"
    body = soup.body.get_text(separator="\n", strip=True) if soup.body else "N/A"

    if debug == 1:
        print(f"Title:-->{title}<--")
        print(f"Body:-->{body}<--")

    await browser.close()

    try:
        with open("resources/twitch/tags.txt", "r", encoding="utf-8") as file:
            titles = {line.strip() for line in file}

        if any(title in body for title in titles):
            return 404, None
        else:
            return 200, url

    except Exception as e:
        if "'NoneType' object has no attribute 'strip'" in str(e):
            return 404, None
        else:
            print(f"Error : {e}")

