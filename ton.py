import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random
import string
import time

# HTTP session with retry/backoff for resilient connections
def make_session():
    s = requests.Session()
    retry = Retry(
        total=4,
        backoff_factor=2,
        status_forcelist=[408, 429, 500, 502, 503, 504],
        allowed_methods=['POST'],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
    s.mount('https://', adapter)
    s.mount('http://', adapter)
    return s

SESSION = make_session()

# ══════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════
REFERRAL_CODE = "TOONF5DF50"
TOTAL_ACCOUNTS = 1000
DELAY_BETWEEN = 2
EMAIL_DOMAIN = "gmail.com"

SUPABASE_URL = "https://yazaxejajnwrgrlhdddf.supabase.co/auth/v1/signup"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlhemF4ZWpham53cmdybGhkZGRmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNDAzOTEsImV4cCI6MjA5MTcxNjM5MX0.vEdH1-WQZnKUSY-Tzg8Po7uTaSgYwq_pQV18eZrQOQc"

HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Authorization": f"Bearer {ANON_KEY}",
    "apikey": ANON_KEY,
    "X-Client-Info": "supabase-js-web/2.104.0",
    "X-Supabase-Api-Version": "2024-01-01",
}

def rand_str(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_account():
    base = rand_str(8)
    email = f"{base}@{EMAIL_DOMAIN}"
    username = rand_str(10)
    password = rand_str(12)
    return email, username, password

def register(email, username, password):
    payload = {
        "email": email,
        "password": password,
        "data": {"username": username, "referral_code": REFERRAL_CODE},
        "gotrue_meta_security": {},
        "code_challenge": None,
        "code_challenge_method": None,
    }
    try:
        res = SESSION.post(SUPABASE_URL, json=payload, headers=HEADERS, timeout=(10, 60))
        if res.status_code == 200:
            data = res.json()
            user_id = data.get("user", {}).get("id", "-")
            print(f"  [OK] email: {email} | username: {username} | id: {user_id}", flush=True)
            return True
        else:
            try:
                j = res.json()
                err = j.get("msg") or j.get("error_description") or j.get("error") or res.text
            except Exception:
                err = res.text
            print(f"  [FAIL] email: {email} | {res.status_code} - {err}", flush=True)
            return False
    except Exception as e:
        print(f"  [ERR] email: {email} | {type(e).__name__}: {e}", flush=True)
        return False

def main():
    print(f"ToonEarn Reff Bot", flush=True)
    print(f"   Ref Code  : {REFERRAL_CODE}", flush=True)
    print(f"   Target    : {TOTAL_ACCOUNTS} akun", flush=True)
    print(f"   Delay     : {DELAY_BETWEEN}s\n", flush=True)
    sukses = 0
    gagal = 0
    for i in range(1, TOTAL_ACCOUNTS + 1):
        print(f"[{i}/{TOTAL_ACCOUNTS}] Mendaftar...", flush=True)
        email, username, password = generate_account()
        if register(email, username, password):
            sukses += 1
        else:
            gagal += 1
        if i < TOTAL_ACCOUNTS:
            time.sleep(DELAY_BETWEEN)
    print(f"\nSelesai! Sukses: {sukses} | Gagal: {gagal}", flush=True)

if __name__ == "__main__":
    main()
