import customtkinter as ctk
from nsea import *
from network import *

def enter():
    url = entry.get()
    if not url:
        status_label.configure(text="Please enter a URL", text_color="red")
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

def show_frame(frame):
    frame.tkraise()

def login(cookie):
    login_status.configure(text="Logging in...", text_color="gray")
    root.update()
    cookie = get_session_cookie(username_entry.get(), password_entry.get())
    if not cookie:
        login_status.configure(text="Login failed — check your credentials", text_color="red")
        return
    show_frame(home_frame)

if __name__ == "__main__":
    
    cookie = None
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("nSEA")
    root.iconbitmap("icon.ico")
    root.geometry("600x420")
    root.minsize(600, 420)
    root.configure(fg_color="#111111")

    # --- login frame ---
    login_frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#1a1a1a")
    login_frame.place(relwidth=1, relheight=1)

    login_title = ctk.CTkLabel(login_frame, text="nSEA", font=ctk.CTkFont(size=40, weight="bold"))
    login_title.pack(pady=(40, 5))

    login_subtitle = ctk.CTkLabel(login_frame, text="Login with your Moodle credentials", font=ctk.CTkFont(size=15, weight="bold"), text_color="#aaaaaa")
    login_subtitle.pack(pady=(0, 25))

    username_entry = ctk.CTkEntry(login_frame, width=400, height=50, placeholder_text="Username", corner_radius=10,
                                  font=ctk.CTkFont(size=14, weight="bold"),
                                  fg_color="#2a2a2a", border_width=2, text_color="white")
    username_entry.pack(pady=(0, 15))

    password_entry = ctk.CTkEntry(login_frame, width=400, height=50, placeholder_text="Password", corner_radius=10,
                                  font=ctk.CTkFont(size=14, weight="bold"),
                                  fg_color="#2a2a2a", border_width=2, text_color="white", show="*")
    password_entry.pack(pady=(0, 15))

    login_status = ctk.CTkLabel(login_frame, text="", font=ctk.CTkFont(size=13, weight="bold"), text_color="red")
    login_status.pack(pady=(0, 10))


    login_button = ctk.CTkButton(login_frame, text="Login", command=lambda: login(cookie), width=400, height=50, corner_radius=10,
                                 font=ctk.CTkFont(size=16, weight="bold"))
    login_button.pack()


    # --- home frame ---
    home_frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#1a1a1a")
    home_frame.place(relwidth=1, relheight=1)

    title_label = ctk.CTkLabel(home_frame, text="nSEA", font=ctk.CTkFont(size=40, weight="bold"))
    title_label.pack(pady=(30, 5))

    subtitle_label = ctk.CTkLabel(home_frame, text="ez exams now heheha", font=ctk.CTkFont(size=15, weight="bold"), text_color="#aaaaaa")
    subtitle_label.pack(pady=(0, 25))

    entry = ctk.CTkEntry(home_frame, width=400, height=50, placeholder_text="Paste Moodle exam URL here", corner_radius=10,
                         font=ctk.CTkFont(size=14, weight="bold"),
                         fg_color="#2a2a2a", border_width=2, text_color="white")
    entry.pack(pady=(0, 15))

    button = ctk.CTkButton(home_frame, text="Generate Key", command=enter, width=400, height=50, corner_radius=10,
                           font=ctk.CTkFont(size=16, weight="bold"))
    button.pack(pady=(0, 15))

    output_label = ctk.CTkEntry(home_frame, width=400, height=50, corner_radius=10,
                                placeholder_text="Output will appear here",
                                font=ctk.CTkFont(size=14, weight="bold"),
                                fg_color="#2a2a2a", border_width=2,
                                text_color="white")
    output_label.configure(state="readonly")
    output_label.pack(pady=(0, 10))

    status_label = ctk.CTkLabel(home_frame, text="", font=ctk.CTkFont(size=13, weight="bold"), text_color="gray")
    status_label.pack()

    show_frame(login_frame)
    
    root.mainloop()