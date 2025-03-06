import webbrowser
import time
import random
import requests
import subprocess

class FakeActivity:
    """
    Generates fake user activity to blend exfiltration traffic with normal browsing, streaming, and downloads.
    """

    def __init__(self):
        self.websites = [
            "https://www.wikipedia.org",
            "https://www.bbc.com/news",
            "https://www.reddit.com",
            "https://www.nytimes.com",
            "https://www.youtube.com"
        ]
        self.download_urls = [
            "https://speed.hetzner.de/100MB.bin",
            "https://download.thinkbroadband.com/100MB.zip"
        ]

    def simulate_web_browsing(self):
        """ Opens random websites in the default web browser. """
        site = random.choice(self.websites)
        print(f"🌍 Browsing: {site}")
        webbrowser.open(site)
        time.sleep(random.randint(5, 15))  # Stay on site for a few seconds

    def simulate_video_streaming(self):
        """ Opens a YouTube video in the browser to mimic streaming behavior. """
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Random video
        print(f"📺 Streaming Video: {video_url}")
        webbrowser.open(video_url)
        time.sleep(random.randint(30, 90))  # Simulate watching video for some time

    def simulate_file_download(self):
        """ Downloads a file from a trusted source to mimic software updates. """
        url = random.choice(self.download_urls)
        print(f"⬇️ Downloading: {url}")
        response = requests.get(url, stream=True, verify=False)
        for chunk in response.iter_content(chunk_size=1024 * 1024):  # Simulate data transfer
            time.sleep(0.5)  # Simulate download delay

    def simulate_email_checking(self):
        """ Mimics checking an email inbox by connecting to an IMAP server. """
        print("📧 Checking Email...")
        try:
            subprocess.run(["ping", "-c", "1", "imap.gmail.com"], stdout=subprocess.DEVNULL)
        except Exception:
            pass  # Ignore errors (use real IMAP connection in a real test)

    def generate_decoy_traffic(self):
        """ Randomly triggers different types of decoy activities. """
        actions = [
            self.simulate_web_browsing,
            self.simulate_video_streaming,
            self.simulate_file_download,
            self.simulate_email_checking
        ]
        action = random.choice(actions)
        action()  # Execute the chosen activity
