from resources.facebook.main import osint as facebook
from resources.instagram.main import osint as instagram
import asyncio

print("Facebook :",asyncio.run(facebook("zuck")))
print("Instagram :",asyncio.run(instagram("zuck")))