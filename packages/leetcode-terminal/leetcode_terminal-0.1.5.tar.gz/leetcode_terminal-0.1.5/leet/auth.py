import json
import os
from rich.console import Console
from rich.prompt import Prompt
import requests

console = Console()

SESSION_FILE = "session.json"


class LeetAuth:
    def __init__(self):
        self.session = requests.Session()
        self.load_session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/121.0.0.0 Safari/537.36"
            ),
            "Referer": "https://leetcode.com",
            "Origin": "https://leetcode.com",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
        })

    def load_session(self):
        if not os.path.exists(SESSION_FILE):
            return

        try:
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)

            cookie = data.get("LEETCODE_SESSION", "")
            csrftoken = data.get("csrftoken", "")

            if cookie:
                self.session.cookies.set("LEETCODE_SESSION", cookie, domain="leetcode.com")
            if csrftoken:
                self.session.cookies.set("csrftoken", csrftoken, domain="leetcode.com")

        except Exception:
            pass

    def save_session(self, cookie, csrftoken):
        with open(SESSION_FILE, "w") as f:
            json.dump({
                "LEETCODE_SESSION": cookie,
                "csrftoken": csrftoken
            }, f, indent=2)

    def login(self):
        console.print("🔑 [bold yellow]LeetCode Login[/bold yellow] — paste LEETCODE_SESSION cookie")

        cookie = Prompt.ask("LEETCODE_SESSION", password=True)

        csrftoken = "dummycsrf123456789"

        self.session.cookies.set("LEETCODE_SESSION", cookie, domain="leetcode.com")
        self.session.cookies.set("csrftoken", csrftoken, domain="leetcode.com")

        resp = self.session.get("https://leetcode.com/api/problems/all/")

        if resp.status_code == 200:
            console.print("✅ [green]Login successful![/green]")
            self.save_session(cookie, csrftoken)
        else:
            console.print(f"❌ [red]Login failed — Status {resp.status_code}[/red]")

    def logout(self):
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)

        console.print("Logged out.")


    def get_session(self):
        return self.session
