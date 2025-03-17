import asyncio
import importlib
import os
import random
import shutil
import string
from datetime import datetime

DEVELOPER_MODE = 1 # It should be 0 or 1
USERNAME = "zuck" # Target UserName

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

resources_path = "resources"
modules = {}

if os.path.exists(resources_path) and os.path.isdir(resources_path):
    module_names = [name for name in os.listdir(resources_path) if os.path.isdir(os.path.join(resources_path, name))]

    for module_name in module_names:
        try:
            module_path = f"resources.{module_name}.main"
            osint_module = importlib.import_module(module_path)
            modules[module_name] = getattr(osint_module, "osint")
        except ModuleNotFoundError:
            print(f"Module {module_name} not found or missing 'main.py'. Skipping...")
        except AttributeError:
            print(f"Module {module_name} does not have 'osint'. Skipping...")

token = ''.join(random.choices(string.ascii_letters + string.digits, k=36))

async def run_modules(target):
    print(f"\nModule Verification Token: {token}\n")

    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{start_time} - Scan Started\n")

    total_modules = len(modules)
    count = 0

    for index, (module_name, module_func) in enumerate(modules.items(), start=1):
        status1, link1 = await module_func(token)
        if status1 == 200:
            print(f"{module_name} [X] Module Outdated")
            await module_func(token, debug=DEVELOPER_MODE)
        elif status1 == 404:
            status2, link2 = await module_func(target)
            count += 1
            if status2 == 200:
                print(f"({count}/{total_modules}) [{target}] Found at {link2}")
            elif status2 == 404:
                print(f"({count}/{total_modules}) [{target}] Not Found at [{module_name.upper()}]")

    print(f"\nScan Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


delete_pycache_()
if len(USERNAME) > 0:
    asyncio.run(run_modules(USERNAME))
else:
    print("Any Valid Username Required !")
delete_pycache_()
