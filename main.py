# ---------------------------------
# Imports - The Magic Wand 🪄
# ---------------------------------

import os
import re
import json
import logging
import threading
from collections import Counter
from datetime import datetime
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
from jinja2 import Template

# ---------------------------------
# Constants - The Backbone of Order 📜
# ---------------------------------
CURRENT_VERSION = "1.0.0"
DISCORD_INVITE = "https://discord.gg/skHyssu"
GITHUB_REPO_URL = "https://github.com/nayandas69/SEO-Sentinel"
AUTHOR_NAME = "Nayan Das"
AUTHOR_WEBSITE = "https://socialportal.nayanchandradas.com"
AUTHOR_EMAIL = "nayanchandradas@hotmail.com"

# ---------------------------------
# Configuration - The Blueprint for Success 📋
# ---------------------------------
DEFAULT_CONFIG = {
    "report_directory": "reports",
    "log_directory": "logs",
    "crawl_depth": 3,  # Default: Crawl 3 levels deep 🔍
    "max_pages": 100,  # Cap the crawl at 100 pages (let's not crash, mkay?).
}

REPORT_DIR = DEFAULT_CONFIG["report_directory"]
LOG_DIR = DEFAULT_CONFIG["log_directory"]

# 🔧 Auto-create directories if missing
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Logging setup – Keeping receipts like a pro 🧾
LOG_FILE = os.path.join(LOG_DIR, "seo_sentinel.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ---------------------------------
# Helper Functions - Utilities that *slap* 🛠️
# ---------------------------------

def log_message(message, level="info", verbose=False):
    """
    Logs messages. Console + Log file. Multi-tasking? We love that. 💼✨
    """
    if verbose:
        print(message)  # For all you visual learners 🖥️
    getattr(logging, level.lower(), logging.info)(message)  # Get that sweet log saved 📜

# ---------------------------------
# Utility Functions - The Swiss Army Knife 🛠️
# ---------------------------------
def fetch_html_content(url, timeout=5):
    """
    Snag the HTML sauce from the given URL. 🕸️
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        log_message(f"❌ Couldn't fetch {url}: {e}", "error")
        return None

# ---------------------------------
# Updates & Community Vibes 🚀💬
# ---------------------------------
def check_internet_connection():
    """
    *Vibe-check* your Wi-Fi. No net? No crawls. 🚫
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
    # First, let's vibe-check the internet connection 🌐
    if not check_internet_connection():
        print("Bruh, you’re offline. Can’t scout for updates like this. 🙃", "error")
        return

    # Flex the current version
    print(f"🤖 Current Version: {CURRENT_VERSION}")
    print("Scouting for updates... Hang tight! 🧐")

    try:
        # Hit the GitHub API to fetch the latest release info 🎯
        response = requests.get("https://api.github.com/repos/nayandas69/SEO-Sentinel/releases/latest")
        response.raise_for_status()
        data = response.json()

        # Grab the latest version from the API response
        latest_version = data.get("tag_name", "Unknown Version")

        if latest_version > CURRENT_VERSION:
            # 🎉 NEW VERSION ALERT! 🎉
            print(f"🎉 Glow-up Alert: Version {latest_version} just dropped! 🚀")
            print(f"✨ Get the update here: {GITHUB_REPO_URL}")

            # Tailored instructions for different setups
            print("\n💻 **If you're using the `.exe` build:**")
            print(f"👉 Download the latest version here: {GITHUB_REPO_URL}/releases\n")

            print("🐍 **If you're using `pip` (Python fam):**")
            print("👉 Run this in your terminal to upgrade:")
            print("```bash\npip install --upgrade seo-sentinel\n```")

            # Plug your Discord for bonus community vibes 💬
            print("\n🔥 Also, join our Discord server to vibe with the community & test new features!")
            print(f"👉 Discord Link: {DISCORD_INVITE}")

        else:
            # No updates? No worries! We keep it 💯
            print("You’re already riding the latest wave. 🏄✨")
            print("BUT, we’re working on 🔥 new features 🔥 to make SEO Sentinel even cooler. 😎")
            print("\n👉 Want early access to beta features? Join our Discord server and test with the fam:")
            print(f"👉 Discord Link: {DISCORD_INVITE}")

    except requests.RequestException as e:
        # API call failed? Ouch, but we stay calm 😌
        print(f"Couldn’t check for updates. Something broke: {e}.", "error")
        print("But hey, we’re still here for you. Keep vibing with SEO Sentinel! 🚀")

# -----------------------------------------
# Core Features - Crawling & Analysis 🌐🔎
# -----------------------------------------
def crawl_website(base_url, max_depth=DEFAULT_CONFIG["crawl_depth"], max_pages=60):
    """
    Deep-dive into a site. Collect pages like a pro. 🕵️‍♀️✨
    """
    if not urlparse(base_url).scheme:
        log_message(f"❌ Invalid URL: {base_url}. Crawling aborted.", "error")
        print(f"❌ Invalid URL: {base_url}. Crawling aborted.")
        return set()

    visited_urls = set()
    urls_to_visit = {base_url}
    depth_tracker = {base_url: 0}  # 🌟 Depth tracker for smart crawls

    while urls_to_visit and len(visited_urls) < max_pages:
        current_url = urls_to_visit.pop()
        current_depth = depth_tracker[current_url]

        if current_url not in visited_urls and current_depth <= max_depth:
            log_message(f"✨ Crawling: {current_url}")
            print(f"✨ Crawling: {current_url}")
            html_content = fetch_html_content(current_url)
            visited_urls.add(current_url)

            # 🌐 Dive deeper (if there's still content)
            if html_content:
                soup = BeautifulSoup(html_content, "html.parser")
                for a_tag in soup.find_all("a", href=True):
                    absolute_url = urljoin(base_url, a_tag["href"])
                    # Stay in the same domain 🌍
                    if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
                        urls_to_visit.add(absolute_url)
                        depth_tracker[absolute_url] = current_depth + 1

    if not visited_urls:
        log_message(f"❌ No pages crawled from {base_url}.", "warning")
        print(f"❌ No pages crawled from {base_url}. Check the URL and try again.")

    log_message(f"✅ Finished crawling. Total pages: {len(visited_urls)}")
    print(f"✅ Finished crawling. Total pages: {len(visited_urls)}")
    return visited_urls

def analyze_seo_issues(url, keywords=None):
    """
    Spy on a page for SEO drama. 🔍🤓
    """
    issues = {
        "broken_links": [],
        "missing_metadata": [],
        "keyword_density": {},
    }
    html_content = fetch_html_content(url)
    if not html_content:
        return issues

    soup = BeautifulSoup(html_content, "html.parser")

    # 1️⃣ Missing Metadata Check
    if not soup.find("title"):
        issues["missing_metadata"].append("Missing <title> tag 😬.")
    if not soup.find("meta", attrs={"name": "description"}):
        issues["missing_metadata"].append("Missing meta description 😥.")

    # 2️⃣ Broken Links Check
    for a_tag in soup.find_all("a", href=True):
        link = urljoin(url, a_tag["href"])
        try:
            response = requests.head(link, timeout=5)
            if response.status_code >= 400:
                issues["broken_links"].append(link)
        except requests.RequestException:
            issues["broken_links"].append(link)

    # 3️⃣ Keyword Density Analysis
    if keywords:
        page_text = soup.get_text()
        word_count = Counter(page_text.split())
        for keyword in keywords:
            issues["keyword_density"][keyword] = word_count.get(keyword.lower(), 0)

    return issues

# ---------------------------------
# Reporting - HTML📊✨
# ---------------------------------
def generate_report(results, base_url):
    """
    Cook up an HTML report that slaps 🔥.
    """
    # HTML Template for the report with inline styling
    template = Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SEO Sentinel Report</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6;
                color: #333;
            }
            h1, h2 {
                color: #444;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f4f4f4;
                font-weight: bold;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            .summary {
                margin: 20px 0;
                padding: 10px;
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .summary p {
                margin: 5px 0;
            }
            footer {
                margin-top: 20px;
                font-size: 0.9em;
                color: #666;
                text-align: center;
            }
            footer a {
                color: #007BFF;
                text-decoration: none;
            }
            footer a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>SEO Sentinel Report</h1>
        <p>Website Analyzed: <strong>{{ base_url }}</strong></p>
        <p>Date Generated: <strong>{{ date }}</strong></p>
        
        <div class="summary">
            <h2>Report Summary</h2>
            <p>Total Pages Crawled: <strong>{{ total_pages }}</strong></p>
            <p>Total Issues Found: <strong>{{ total_issues }}</strong></p>
            <p>Broken Links: <strong>{{ broken_links }}</strong></p>
            <p>Pages with Missing Metadata: <strong>{{ missing_metadata }}</strong></p>
        </div>

        <h2>Detailed Analysis</h2>
        <table>
            <thead>
                <tr>
                    <th>Page URL</th>
                    <th>Broken Links</th>
                    <th>Missing Metadata</th>
                    <th>Keyword Density</th>
                </tr>
            </thead>
            <tbody>
                {% for url, issues in results.items() %}
                <tr>
                    <td>{{ url }}</td>
                    <td>
                        {% if issues.broken_links %}
                            <ul>
                                {% for link in issues.broken_links %}
                                <li>{{ link }}</li>
                                {% endfor %}
                            </ul>
                        {% else %}
                            None
                        {% endif %}
                    </td>
                    <td>
                        {% if issues.missing_metadata %}
                            <ul>
                                {% for metadata in issues.missing_metadata %}
                                <li>{{ metadata }}</li>
                                {% endfor %}
                            </ul>
                        {% else %}
                            None
                        {% endif %}
                    </td>
                    <td>
                        {% if issues.keyword_density %}
                            <ul>
                                {% for keyword, count in issues.keyword_density.items() %}
                                <li>{{ keyword }}: {{ count }}</li>
                                {% endfor %}
                            </ul>
                        {% else %}
                            Not analyzed
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <footer>
            <p>Generated by <a href="https://github.com/nayandas69" target="_blank" rel="noopener noreferrer">SEO Sentinel</a>. Stay optimized! 🚀</p>
        </footer>
    </body>
    </html>
    """)

    # Generate the report content
    total_pages = len(results)
    total_issues = sum(
        len(issues["broken_links"]) + len(issues["missing_metadata"])
        for issues in results.values()
    )
    broken_links = sum(len(issues["broken_links"]) for issues in results.values())
    missing_metadata = sum(len(issues["missing_metadata"]) for issues in results.values())

    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rendered_content = template.render(
        base_url=base_url,
        date=date_now,
        total_pages=total_pages,
        total_issues=total_issues,
        broken_links=broken_links,
        missing_metadata=missing_metadata,
        results=results,
    )

    # Save the report as an HTML file
    report_filename = f"seo_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    report_path = os.path.join(REPORT_DIR, report_filename)

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(rendered_content)

    return report_path

# ---------------------------------
# CLI Magic - *Command This* 🪄
# ---------------------------------
def main():
    """
    Run the CLI, serving vibes and results. Keep it simple. 🌈
    """
    print("=" * 60)
    print("✨ SEO Sentinel - Automated SEO Tester ✨")
    print(f"Version: {CURRENT_VERSION}")
    print(F"Author: {AUTHOR_NAME}")
    print(f"Author's Website: {AUTHOR_WEBSITE}")
    print(F"Author's Email: {AUTHOR_EMAIL}")
    print("=" * 60)

    while True:
        print("\nPick Your Poison:")
        print("1. Analyze Website SEO 🕵️")
        print("2. Check for Updates 🚀")
        print("3. Exit 😢")

        choice = input("\nYour choice, boss: ").strip()
        if choice == "1":
            base_url = input("URL to analyze: ").strip()
            # Validate the URL
            if not base_url:
                print("🚨 URL cannot be empty. Please enter a valid URL.")
                continue
            elif not urlparse(base_url).scheme:
                print("🚨 Invalid URL. Please ensure it starts with 'http://' or 'https://'.")
                continue

            log_message(f"Analyzing {base_url}... Hold tight! 🎯")
            print(f"Analyzing {base_url}... Hold tight! 🎯")
            crawled_urls = crawl_website(base_url)
            results = {}

            for url in tqdm(crawled_urls, desc="Digging for SEO gold..."):
                results[url] = analyze_seo_issues(url)

            report_path = generate_report(results, base_url)
            log_message(f"Report done. Check it: {report_path} 💾")
            print(f"Boom 💥 Report ready: {report_path} 💾")
        elif choice == "2":
            check_for_updates()
        elif choice == "3":
            print("Peace out, see ya next time! ✌️")
            break
        else:
            print("Bruh, invalid choice. Try again. 🤷", "warning")

if __name__ == "__main__":
    main()
