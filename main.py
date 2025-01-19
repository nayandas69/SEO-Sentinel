import os
import re
import json
import logging
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from jinja2 import Template
from tqdm import tqdm

# ---------------------------------
# Glow-up Info - Version & Updates 🌟
# ---------------------------------
CURRENT_VERSION = "1.0.0-beta"
UPDATE_URL = "https://api.github.com/repos/nayandas69/SEO-Sentinel/releases/latest"
DISCORD_INVITE = "https://discord.gg/skHyssu"
GITHUB_REPO_URL = "https://github.com/nayandas69/SEO-Sentinel"
AUTHOR_WEBSITE = "https://socialportal.nayanchandradas.com"
AUTHOR_EMAIL = "nayanchandradas@hotmail.com"

# ---------------------------------
# Default Config - Cause Defaults Slap 🛠️
# ---------------------------------
DEFAULT_CONFIG = {
    "report_directory": "reports",
    "log_directory": "logs",
}

REPORT_DIR = DEFAULT_CONFIG["report_directory"]
LOG_DIR = DEFAULT_CONFIG["log_directory"]

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "seo_sentinel.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ---------------------------------
# Helper Functions - Stay Sharp 🧠
# ---------------------------------

def log_message(message, level="info"):
    """
    Drop logs like they’re hot. Console + File.
    """
    print(message)
    getattr(logging, level.lower(), logging.info)(message)

def check_internet_connection():
    """
    Test the vibes of your Wi-Fi. No net, no game.
    """
    try:
        requests.head("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def check_for_updates():
    """
    Check if a glow-up is available for this tool. 🚀
    """
    if not check_internet_connection():
        log_message("Bro, you’re offline. Can’t check updates like this. 🙃", "error")
        return

    log_message(f"Current version: {CURRENT_VERSION}")
    log_message("Scouting for updates... 🧐")
    try:
        response = requests.get(UPDATE_URL)
        response.raise_for_status()
        data = response.json()

        latest_version = data.get("tag_name", "Unknown Version")
        if latest_version > CURRENT_VERSION:
            log_message(f"🎉 Fresh version drop: {latest_version}. Update now!")
            log_message(f"Git it here: {GITHUB_REPO_URL}")
        else:
            log_message("You’re riding the latest wave. 🏄")
            log_message(f"Got ideas? Slide into our Discord: {DISCORD_INVITE}")
    except requests.RequestException as e:
        log_message(f"Couldn’t check updates. Error: {e}.", "error")

# ---------------------------------
# Web Crawling & SEO Analysis - Go Deep 🌐
# ---------------------------------

def crawl_website(base_url, max_pages=50):
    """
    Collect links from a website. Dive deep but not too deep.
    """
    visited_urls = set()
    urls_to_visit = {base_url}

    while urls_to_visit and len(visited_urls) < max_pages:
        current_url = urls_to_visit.pop()
        if current_url not in visited_urls:
            log_message(f"Crawling: {current_url} 🕸️")
            html_content = fetch_html_content(current_url)
            visited_urls.add(current_url)

            if html_content:
                soup = BeautifulSoup(html_content, "html.parser")
                for a_tag in soup.find_all("a", href=True):
                    absolute_url = urljoin(base_url, a_tag["href"])
                    if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
                        urls_to_visit.add(absolute_url)

    return visited_urls

def fetch_html_content(url):
    """
    Snag the HTML sauce from a URL. 🕵️‍♂️
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        log_message(f"Couldn’t fetch {url}: {e}.", "error")
        return None

def check_seo_issues(url):
    """
    Spy on SEO issues for a page. 🤓
    """
    issues = {"broken_links": [], "missing_metadata": [], "suggested_keywords": []}
    html_content = fetch_html_content(url)
    if not html_content:
        return issues

    soup = BeautifulSoup(html_content, "html.parser")

    # Check for broken links
    for a_tag in soup.find_all("a", href=True):
        link = urljoin(url, a_tag["href"])
        try:
            response = requests.head(link, timeout=5)
            if response.status_code >= 400:
                issues["broken_links"].append(link)
        except requests.RequestException:
            issues["broken_links"].append(link)

    # Check for missing metadata
    if not soup.find("title"):
        issues["missing_metadata"].append("Missing <title> tag. 🚩")
    if not soup.find("meta", attrs={"name": "description"}):
        issues["missing_metadata"].append("Missing meta description. 😥")

    return issues

def generate_report(results, base_url):
    """
    Cook up a sweet HTML report. 🔥
    """
    template = Template("""
    <html>
    <head>
        <title>SEO Sentinel Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        </style>
    </head>
    <body>
        <h1>SEO Sentinel Report</h1>
        <p>Website: {{ base_url }}</p>
        <p>Date: {{ date }}</p>
        <table>
            <thead>
                <tr>
                    <th>Page URL</th>
                    <th>SEO Issues</th>
                </tr>
            </thead>
            <tbody>
                {% for url, issues in results.items() %}
                <tr>
                    <td>{{ url }}</td>
                    <td>
                        <ul>
                            {% for category, items in issues.items() %}
                            <li>{{ category }}:
                                <ul>
                                    {% for item in items %}
                                    <li>{{ item }}</li>
                                    {% endfor %}
                                </ul>
                            </li>
                            {% endfor %}
                        </ul>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """)
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = template.render(results=results, base_url=base_url, date=date_now)

    path = os.path.join(REPORT_DIR, f"seo_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.html")

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

    return path

# ---------------------------------
# CLI Magic - User-friendly AF 🪄
# ---------------------------------

def main():
    """
    Run the CLI, serving vibes and purpose. Keep it simple. 🌈
    """
    print("=" * 60)
    print("✨ SEO Sentinel - Automated SEO Tester ✨")
    print("Author: Nayan Das")
    print(f"Website: {AUTHOR_WEBSITE}")
    print(f"Email: {AUTHOR_EMAIL}")
    print(f"Discord: {DISCORD_INVITE}")
    print(f"Version: {CURRENT_VERSION}")
    print("=" * 60)

    while True:
        print("\nPick Your Poison")
        print("1. Analyze Website SEO 🕵️")
        print("2. Check for Updates 🚀")
        print("3. Exit 😢")

        choice = input("\nYour choice, boss: ").strip()
        if choice == "1":
            base_url = input("Drop the URL to analyze: ").strip()
            log_message(f"Analyzing {base_url}. Hold tight! 🎯")
            crawled_urls = crawl_website(base_url)
            log_message(f"Found {len(crawled_urls)} pages. That’s a lotta links! 🔗")

            results = {}
            for url in tqdm(crawled_urls, desc="Digging for SEO gold"):
                results[url] = check_seo_issues(url)

            report_path = generate_report(results, base_url)
            log_message(f"Boom 💥 Report ready: {report_path}")
        elif choice == "2":
            check_for_updates()
        elif choice == "3":
            log_message("Peace out, see ya next time! ✌️")
            break
        else:
            log_message("Bruh, invalid choice. Try again. 🤷", "warning")

if __name__ == "__main__":
    main()
