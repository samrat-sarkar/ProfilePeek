import os
import random
import shutil
import string
import asyncio

from resources.facebook.main import osint as facebook
from resources.instagram.main import osint as instagram
from resources.x.main import osint as x
from resources.youtube.main import osint as youtube
from resources.snapchat.main import osint as snapchat
from resources.reddit.main import osint as reddit
from resources.pinterest.main import osint as pinterest
from resources.twitch.main import osint as twitch
from resources.quora.main import osint as quora
from resources.medium.main import osint as medium
from resources.mastodon.main import osint as mastodon

def delete_pycache_():
    resources_path = "resources"
    if not os.path.exists(resources_path):
        return
    for root, dirs, files in os.walk(resources_path):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(pycache_path)
            except Exception as e:
                return

def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=36))

module_functions = {
    "facebook": facebook,
    "x": x,
    "youtube": youtube,
    "snapchat": snapchat,
    "reddit": reddit,
    "pinterest": pinterest,
    "twitch": twitch,
    "quora": quora,
    "instagram": instagram
}

outdated_module = []

async def check_modules():
    print("📁 Module Inspection Started")
    token = generate_token()
    tasks = {
        "Facebook": facebook,
        "X": x,
        "YouTube": youtube,
        "Snapchat": snapchat,
        "Reddit": reddit,
        "Instagram": instagram,
        "Pinterest": pinterest,
        "Quora": quora,
        "Medium": medium,
        "Mastodon": mastodon,
    }

    with tqdm(total=len(tasks), desc="Checking Modules", unit="module") as progress:
        coroutines = [check_module(name, func, token, progress) for name, func in tasks.items()]
        results = await asyncio.gather(*coroutines, return_exceptions=False)

    for module, status in results:
        if status == 200:
            print(f"{module} Module Outdated")
        elif status == 404:
            print(f"{module} Module Up-to-date")


asyncio.run(check_modules()) # Call This Function When You Want To Check That Module is Working Properly Or Not

#print(asyncio.run(facebook("zuck")))
#print(asyncio.run(instagram("zuck")))
#print(asyncio.run(x("zuck")))
#print(asyncio.run(youtube("zuck")))
#print(asyncio.run(snapchat("zuck")))
#print(asyncio.run(reddit("zuck")))
#print(asyncio.run(pinterest("zuck")))
#print(asyncio.run(quora("Joshua-N-Marron")))
#print(asyncio.run(medium("realalexnguyen")))
print(asyncio.run(mastodon("nixCraftgvhvghgv")))
#print(asyncio.run(twitch("zuck")))
#print(asyncio.run(quora("zuck")))

delete_pycache_()