import os
import requests
import time
import subprocess
import glob
import ctypes
from art import text2art
import tkinter as tk
from tkinter import messagebox

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

root = tk.Tk()
root.title("neoneko Launcher")

title_label = tk.Label(root, text=text2art('neoneko', font='banner3'), font=("Courier", 10), fg="green", justify=tk.LEFT)
title_label.pack(pady=5)

listbox = tk.Listbox(root, width=40, height=10)
listbox.pack(padx=10, pady=10)

for cookie_data in cookies:
    listbox.insert(tk.END, cookie_data['username'])

def launch_selected():
    selection = listbox.curselection()
    if not selection:
        messagebox.showinfo("Select Account", "Please select an account.")
        return
    cookie_data = cookies[selection[0]]
    launch_roblox_with_place_id(place_id, cookie_data['cookie'])

def launch_all():
    for cookie_data in cookies:
        launch_roblox_with_place_id(place_id, cookie_data['cookie'])

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

launch_sel_btn = tk.Button(button_frame, text="Launch Selected", command=launch_selected)
launch_sel_btn.pack(side=tk.LEFT, padx=5)

launch_all_btn = tk.Button(button_frame, text="Launch All", command=launch_all)
launch_all_btn.pack(side=tk.LEFT, padx=5)

root.mainloop()
