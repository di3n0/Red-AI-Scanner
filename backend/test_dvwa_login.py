import requests
from bs4 import BeautifulSoup

def login_dvwa(url, username, password):
    session = requests.Session()
    login_url = f"{url.rstrip('/')}/login.php"
    
    # 1. Get CSRF token
    try:
        r = session.get(login_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        user_token = soup.find('input', {'name': 'user_token'}).get('value')
    except Exception as e:
        print(f"[-] Failed to get CSRF token: {e}")
        return None

    # 2. Login
    data = {
        'username': username,
        'password': password,
        'Login': 'Login',
        'user_token': user_token
    }
    
    r = session.post(login_url, data=data, allow_redirects=False)
    
    if r.status_code == 302 and 'index.php' in r.headers.get('Location', ''):
        print(f"[+] Login successful. Location: {r.headers['Location']}")
        print(f"[+] Cookies: {session.cookies.get_dict()}")
        return session.cookies.get_dict()
    else:
        print(f"[-] Login failed. Status: {r.status_code}")
        return None

if __name__ == "__main__":
    login_dvwa("http://localhost:80", "admin", "password")
