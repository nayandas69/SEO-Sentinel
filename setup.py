from setuptools import setup

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="seo-sentinel",
    version="1.0.0",
    author="Nayan Das",
    author_email="nayanchandradas@hotmail.com",
    description="SEO-Sentinel is a Python package that helps you to automate SEO testing and analytics. It crawls the website and generates a report with SEO metrics. ⚙️",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nayandas69/SEO-Sentinel",
    py_modules=["main"],  # Specify the standalone Python module
    include_package_data=True,
    install_requires=[
        "beautifulsoup4>=4.12.2",
        "requests>=2.31.0",
        "jinja2>=3.1.2",
        "tqdm>=4.64.1",
    ],
    entry_points={
        "console_scripts": [
            "seo-sentinel=main:main",  # Entry point to your main function
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    keywords="SEO-Sentinel, seo-sentinel, SEO testing, web crawling, automation, analytics",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/nayandas69/SEO-Sentinel/issues",
        "Documentation": "https://github.com/nayandas69/SEO-Sentinel#readme",
        "Source Code": "https://github.com/nayandas69/SEO-Sentinel",
        "Discord": "https://discord.gg/skHyssu",
    },
)
