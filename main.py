import customtkinter as ctk
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
        status_label.configure(text="Please enter a URL", text_color="red")
        return
    status_label.configure(text="Logging in...", text_color="gray")
    root.update()

    credentials = load_credentials()
    cookie = get_session_cookie(credentials[0], credentials[1])
    if not cookie:
        status_label.configure(text="Login failed — check credentials.txt", text_color="red")
        return

    status_label.configure(text="Fetching download link...", text_color="gray")
    root.update()

    download_link = get_download_page(cookie, url)[7:]
    if not download_link:
        status_label.configure(text="No config file found", text_color="red")
        return
    download_link = "https://" + download_link

    status_label.configure(text="Downloading config...", text_color="gray")
    root.update()

    download_file(cookie, download_link)
    output = seb_hash_from_config("config.seb")

    output_label.delete(0, "end")
    output_label.configure(state="normal")
    output_label.insert(0, output)
    output_label.configure(state="readonly")
    status_label.configure(text="Done!", text_color="green")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("nSEA")
    root.iconbitmap("icon.ico")
    root.geometry("600x400")
    root.minsize(600, 420)
    root.configure(fg_color="#111111")

    # main container
    home_frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#1a1a1a")
    home_frame.pack(padx=30, pady=30, fill="both", expand=True)

    # title
    title_label = ctk.CTkLabel(home_frame, text="nSEA", font=ctk.CTkFont(size=40, weight="bold"))
    title_label.pack(pady=(30, 5))

    subtitle_label = ctk.CTkLabel(home_frame, text="Safe Exam Browser Config Key Generator", font=ctk.CTkFont(size=15, weight="bold"), text_color="#aaaaaa")
    subtitle_label.pack(pady=(0, 25))

    # url input
    entry = ctk.CTkEntry(home_frame, width=400, height=50, placeholder_text="Paste Moodle exam URL here", corner_radius=10,
                         font=ctk.CTkFont(size=14, weight="bold"),
                         fg_color="#2a2a2a", border_width=2, text_color="white")
    entry.pack(pady=(0, 15))

    # enter button
    button = ctk.CTkButton(home_frame, text="Generate Key", command=enter, width=400, height=50, corner_radius=10,
                           font=ctk.CTkFont(size=16, weight="bold"))
    button.pack(pady=(0, 15))

    # output field
    output_label = ctk.CTkEntry(home_frame, width=400, height=50, corner_radius=10,
                                placeholder_text="Output will appear here",
                                font=ctk.CTkFont(size=14, weight="bold"),
                                fg_color="#2a2a2a", border_width=2, 
                                text_color="white", state="readonly")
    output_label.pack(pady=(0, 10))

    # status label
    status_label = ctk.CTkLabel(home_frame, text="", font=ctk.CTkFont(size=13, weight="bold"), text_color="gray")
    status_label.pack()


    root.mainloop()
