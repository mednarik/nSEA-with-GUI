import tkinter as tk
from bs4 import BeautifulSoup
from nsea import *
import requests

def get_session_cookie(username, password):
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}
    login_url = "https://elearning.tgm.ac.at/login/index.php"

    response = session.get(login_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    logintoken_input = soup.find("input", {"name": "logintoken"})
    if not logintoken_input:
        print("[DEBUG] No logintoken found!")
        return None

    logintoken = logintoken_input.get("value", "")
    print(f"[DEBUG] Found logintoken: {logintoken}")

    post_response = session.post(login_url, headers=headers, data={
        "username": username,
        "password": password,
        "logintoken": logintoken
    })
    print(f"[DEBUG] POST status: {post_response.status_code}")
    print(f"[DEBUG] POST url: {post_response.url}")
    print(f"[DEBUG] Cookies: {session.cookies.get_dict()}")
    return session.cookies.get("MoodleSessionmdl4")

def load_credentials(path="credentials.txt"):
    username = None
    password = None

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue 
            if line.startswith("username"):
                username = line.split("=", 1)[1].strip()
            elif line.startswith("password"):
                password = line.split("=", 1)[1].strip()

                if username is None or password is None:
                    raise ValueError("Credentials file is missing username or password")
        return username, password

def get_download_page(cookie, url):
    session = requests.Session()
    session.cookies.set("MoodleSessionmdl4", cookie)

    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a", class_="btn btn-secondary")
    for link in links:
        href = link.get("href", "")
        if "config.php" in href:
            return href
    return None

def download_file(cookie, url, save_path="config.seb"):
    session = requests.Session()
    session.cookies.set("MoodleSessionmdl4", cookie)

    response = session.get(url, stream=True)
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            print(f"Downloaded to {save_path}")

def enter():
    url = entry.get()
    if not url:
        print("No URL entered")
        return
    credentials = load_credentials()
    cookie = get_session_cookie(credentials[0], credentials[1])
    if not cookie:
        print("Login failed — check credentials")
        return
    download_link = "https://" + get_download_page(cookie, url)[7:]
    if download_link:
        print(f"download link: {download_link}")
    else:
        print("No matching link found")
        
    download_file(cookie, download_link)
    output = seb_hash_from_config("config.seb")
    output_label.insert(0, output)

if __name__ == "__main__":

    root = tk.Tk()
    root.title("nSEA with GUI")
    root.minsize(400, 100)

    info_label = tk.Label(root, text="Paste URL")
    info_label.pack()

    entry = tk.Entry(root)
    entry.pack()
    
    button = tk.Button(root, text="Enter", command=enter)
    button.pack()
    
    output_label = tk.Entry(root, width=100)
    output_label.pack()

    root.mainloop()
