# SEO Sentinel

SEO Sentinel is a lightweight, powerful automated SEO auditing tool. It crawls websites, identifies broken links, missing metadata, keyword density issues, and generates beautiful reports. Designed for simplicity, speed, and precision.

> Make your websites shine in search engines effortlessly!

![Build](https://img.shields.io/github/actions/workflow/status/nayandas69/SEO-Sentinel/publish.yml?branch=main)
![PyPI](https://img.shields.io/pypi/v/seo-sentinel)
![Python Version](https://img.shields.io/pypi/pyversions/seo-sentinel)
![License](https://img.shields.io/github/license/nayandas69/SEO-Sentinel?style=flat-square&color=blue&logo=github&logoColor=white)

## Features

- [x] Full website crawling up to customizable depth.
- [x] Detects broken links, missing title/meta tags.
- [x] Keyword density analysis.
- [x] Generates detailed HTML SEO reports.
- [x] Check for updates easily via CLI.

## Getting Started

### Clone & Run Locally

```bash
# Clone the repository
git clone https://github.com/nayandas69/SEO-Sentinel
cd SEO-Sentinel

# Create a virtual environment
python3 -m venv venv

# Activate the environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Run the project
python3 seose.py
```

### Install via PyPI

```bash
pip install seo-sentinel
```

Then run via:

```bash
seo-sentinel
```

> [!NOTE]
> Always make sure your internet connection is active while using SEO Sentinel for crawling and update checking.

> [!IMPORTANT]
> Make sure your URLs include `http://` or `https://` otherwise they will be rejected.

> [!TIP]
> Generate reports regularly to monitor improvements after fixing SEO issues.

## TODO

- [ ] Add Multi-threaded Crawling
- [ ] Add Advanced Keyword Analysis
- [ ] Add Automatic Report Upload to Cloud
- [ ] Add Customizable Report Templates
- [ ] Add Support for More SEO Metrics
- [ ] Add Support for More Languages
- [ ] Add More Detailed Documentation
- [ ] Add More Tests

Made with ❤️ by [Nayan Das](https://nayandas69.github.io/link-in-bio)

Feel free to ⭐ star and fork the repo!

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

> Ready to optimize your website? Let's get started!

## Disclaimer

> [!IMPORTANT]
> SEO Sentinel is a helpful utility for SEO auditing but does not guarantee search engine ranking improvements. Please ensure your usage complies with the target site's policies.
> Always respect the `robots.txt` file of the websites you crawl.
> Use responsibly and ethically.
> The author is not responsible for any misuse or damage caused by the tool.
> Always test on your own sites or with permission from the site owner.