import os
import requests
import time
import subprocess
import glob
import ctypes
from colorama import init, Fore
from art import text2art
init()
print(Fore.GREEN + text2art('neoneko', font='banner3') + Fore.LIGHTBLUE_EX)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)    
kernel32.GetCurrentProcess()
mutexes = [
    "ROBLOX_singletonMutex",
    "ROBLOX_singletonEvent",
    "ROBLOX_SingletonEvent",
    "RobloxMultiplayerPipe",
    "RobloxGameExplorer"
]   
for mutex_name in mutexes:
    mutex = kernel32.CreateMutexW(None, False, mutex_name)
    if mutex == 0:
        continue
def find_roblox_path():
        base_path = r"C:\Program Files (x86)\Roblox\Versions"
        if not os.path.exists(base_path):
            base_path = r"C:\Program Files\Roblox\Versions"
        versions = glob.glob(os.path.join(base_path, "*"))
        for version in versions:
            player_path = os.path.join(version, "RobloxPlayerBeta.exe")
            if os.path.exists(player_path):
                return player_path
def read_place_id():
    with open("place_id.txt", "r") as f:
                return f.read().strip()
roblox_player_path = find_roblox_path()
place_id = read_place_id()
def get_username(cookie):
    headers = {
        "Cookie": f".ROBLOSECURITY={cookie}",
        "User-Agent": "Roblox/WinInet"
    }
    response = requests.get("https://users.roblox.com/v1/users/authenticated", headers=headers)
    return response.json()["name"]
def read_cookies():
    cookies = []
    if os.path.exists("cookies.txt"):
        with open("cookies.txt", "r") as f:
            for line in f:
                cookie = line.strip()
                if cookie:
                    username = get_username(cookie)
                    cookies.append({"cookie": cookie, "username": username})
    return cookies
def get_auth_ticket(cookie):
    auth_url = "https://auth.roblox.com/v1/authentication-ticket"
    headers = {
        "Cookie": f".ROBLOSECURITY={cookie}",
        "Referer": "https://www.roblox.com/",
        "X-CSRF-TOKEN": "",
        "Content-Type": "application/json",
        "User-Agent": "Roblox/WinInet",
        "Origin": "https://www.roblox.com",
        "RBXAuthenticationNegotiation": "1"
    }
    response = requests.post(auth_url, headers=headers)
    headers["X-CSRF-TOKEN"] = response.headers.get("x-csrf-token")
    response = requests.post(auth_url, headers=headers)
    return response.headers.get("rbx-authentication-ticket")
def launch_roblox_with_place_id(place_id, cookie=None):
    launch_time = int(time.time() * 1000)
    join_script_url = (
        f"https://assetgame.roblox.com/game/PlaceLauncher.ashx"
        f"?request=RequestGame"
        f"&browserTrackerId={int(time.time())}"
        f"&placeId={place_id}"
        f"&isPlayTogetherGame=false"
        f"&launchTime={launch_time}"
        f"&gameId="
    )
    args = [
        roblox_player_path,
        "--app",
        "-t", get_auth_ticket(cookie),
        "--browser",
        "--launchtime={0}".format(launch_time),
        "--rloc", "en_us",
        "--gloc", "en_us",
        "-j", join_script_url,
        "--mutexhandle", "0",
        "--no-mutex-check"
    ]
    time.sleep(3)
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.Popen(args, startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE)
cookies = read_cookies()
while True:
    for i, cookie_data in enumerate(cookies, 1):
        print(f"{i}. {cookie_data['username']}")
    print("")
    print("1. Launch all accounts")
    print("2. Launch a specific account")
    choice = input()
    if choice == "1":
        print("\nLaunching all accounts...")
        for cookie_data in cookies:
            print(f"\nLaunching an Account: {cookie_data['username']}")
            launch_roblox_with_place_id(place_id, cookie_data['cookie'])
    elif choice == "2":
        acc_num = int(input("Id Account: "))
        cookie_data = cookies[acc_num - 1]
        print(f"\nLaunching an Account: {cookie_data['username']}")
        launch_roblox_with_place_id(place_id, cookie_data['cookie'])