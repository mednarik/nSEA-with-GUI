import requests
from bs4 import BeautifulSoup
def get_session_cookie(username, password):
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}
    login_url = "https://elearning.tgm.ac.at/login/index.php"

    response = session.get(login_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    logintoken_input = soup.find("input", {"name": "logintoken"})
    if not logintoken_input:
        return None

    logintoken = logintoken_input.get("value", "")

    post_response = session.post(login_url, headers=headers, data={
        "username": username,
        "password": password,
        "logintoken": logintoken
    })

    if "login" in post_response.url:
        return None

    return session.cookies.get("MoodleSessionmdl4")


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