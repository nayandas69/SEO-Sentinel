from setuptools import setup

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="seo_sentinel",
    version="1.0.1",
    author="nayandas69",
    author_email="nayanchandradas@hotmail.com",
    description="SEO-Sentinel automates SEO testing by crawling websites and generating detailed SEO reports.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nayandas69/SEO-Sentinel",
    py_modules=["seose"],
    include_package_data=True,
    install_requires=[
        "beautifulsoup4>=4.12.2",
        "requests>=2.31.0",
        "jinja2>=3.1.2",
        "tqdm>=4.64.1",
    ],
    entry_points={
        "console_scripts": [
            "seo-sentinel=seose:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    python_requires=">=3.6",
    keywords="SEO, SEO Testing, SEO Automation, Web Crawling, SEO Report, SEO Sentinel",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/nayandas69/SEO-Sentinel/issues",
        "Documentation": "https://github.com/nayandas69/SEO-Sentinel#readme",
        "Source Code": "https://github.com/nayandas69/SEO-Sentinel",
        "Discord": "https://discord.gg/skHyssu",
    },
)
