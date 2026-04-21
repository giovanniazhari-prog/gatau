import requests
import random
import string
import time

# ══════════════════════════════════════════
#  CONFIG — edit sesuai kebutuhan lo
# ══════════════════════════════════════════
REFERRAL_CODE = "TOONF5DF50"       # ref code lo
TOTAL_ACCOUNTS = 1000                 # berapa akun mau dibuat
DELAY_BETWEEN = 2                   # jeda antar request (detik)
EMAIL_DOMAIN = "gmail.com"          # domain email (bisa ganti)

SUPABASE_URL = "https://yazaxejajnwrgrlhdddf.supabase.co/auth/v1/signup"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlhemF4ZWpham53cmdybGhkZGRmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNDAzOTEsImV4cCI6MjA5MTcxNjM5MX0.vEdH1-WQZnKUSY-Tzg8Po7uTaSgYwq_pQV18eZrQOQc"

HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Authorization": f"Bearer {ANON_KEY}",
    "apikey": ANON_KEY,
    "X-Client-Info": "supabase-js-web/2.104.0",
    "X-Supabase-Api-Version": "2024-01-01",
}

# ══════════════════════════════════════════
#  HELPER
# ══════════════════════════════════════════
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
        "data": {
            "username": username,
            "referral_code": REFERRAL_CODE
        },
        "gotrue_meta_security": {},
        "code_challenge": None,
        "code_challenge_method": None
    }

    try:
        res = requests.post(SUPABASE_URL, json=payload, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            data = res.json()
            user_id = data.get("user", {}).get("id", "-")
            print(f"  ✅ SUKSES | email: {email} | username: {username} | id: {user_id}")
            return True
        else:
            err = res.json().get("msg") or res.json().get("error_description") or res.text
            print(f"  ❌ GAGAL  | email: {email} | {res.status_code} - {err}")
            return False
    except Exception as e:
        print(f"  ⚠️  ERROR  | email: {email} | {e}")
        return False

# ══════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════
def main():
    print(f"🚀 ToonEarn Reff Bot")
    print(f"   Ref Code  : {REFERRAL_CODE}")
    print(f"   Target    : {TOTAL_ACCOUNTS} akun")
    print(f"   Delay     : {DELAY_BETWEEN}s\n")

    sukses = 0
    gagal = 0

    for i in range(1, TOTAL_ACCOUNTS + 1):
        print(f"[{i}/{TOTAL_ACCOUNTS}] Mendaftar...")
        email, username, password = generate_account()

        if register(email, username, password):
            sukses += 1
        else:
            gagal += 1

        if i < TOTAL_ACCOUNTS:
            time.sleep(DELAY_BETWEEN)

    print(f"\n{'═'*40}")
    print(f"  Selesai! Sukses: {sukses} | Gagal: {gagal}")
    print(f"{'═'*40}")

if __name__ == "__main__":
    main()
          
