from resources.facebook.main import osint as facebook
from resources.instagram.main import osint as instagram
from resources.x.main import osint as x
from resources.youtube.main import osint as youtube
import asyncio

#print("Facebook : ",asyncio.run(facebook("zuck")))
#print("instagram : ",asyncio.run(instagram("zuck")))
#print("X : ",asyncio.run(x("finkd")))
print("youtube : ",asyncio.run(youtube("tseries")))