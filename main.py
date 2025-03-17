import asyncio
import os
import random
import shutil
import string
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

modules = [facebook, instagram, x, youtube, snapchat, reddit,
           pinterest, twitch, quora, medium, mastodon]

token = ''.join(random.choices(string.ascii_letters + string.digits, k=36))

async def run_modules(target):
    print(f"Module Verification Token: {token}")
    for module in modules:
        module_name = module.__module__.split(".")[1]
        request1 = await module(token)
        if request1 == 200:
            print(f"{module_name} [X] Module Outdated")
            await module(token, debug=1)
        elif request1 == 404:
            request2 = await module(target)
            if request2 == 200:
                print(f"[{target}] Found at [{module_name.upper()}]")
            elif request2 == 404:
                print(f"[{target}] Not Found [{module_name.upper()}]")

asyncio.run(run_modules("zuck"))
delete_pycache_()