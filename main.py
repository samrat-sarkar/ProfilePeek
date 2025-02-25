import random
import string
import asyncio
from tqdm.asyncio import tqdm
from resources.facebook.main import osint as facebook
from resources.instagram.main import osint as instagram
from resources.x.main import osint as x
from resources.youtube.main import osint as youtube


def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=36))


async def check_module(name, func, token, progress):
    status = await func(token)
    progress.update(1)
    return name, status


async def check_modules():
    token = generate_token()
    tasks = {
        "Facebook": facebook,
        "X": x,
        "YouTube": youtube,
        "Instagram": instagram
    }

    with tqdm(total=len(tasks), desc="Checking Modules", unit="module") as progress:
        coroutines = [check_module(name, func, token, progress) for name, func in tasks.items()]
        results = await asyncio.gather(*coroutines)

    for module, status in results:
        if status == 200:
            print(f"{module} Module Outdated")
        elif status == 404:
            print(f"{module} Module Up-to-date")

#asyncio.run(check_modules())# Call This Function When You Want To Check That Module is Working Properly Or Not

# print(asyncio.run(facebook("zuck")))
# print(asyncio.run(instagram("zuck")))
#print(asyncio.run(x("zuck")))
#print(asyncio.run(youtube("zuck")))