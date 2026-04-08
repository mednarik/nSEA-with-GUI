from main import *
    
credentials = load_credentials()
cookie = get_session_cookie(credentials[0], credentials[1])
print(cookie)