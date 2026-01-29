"""
Setup configuration for Entropic Core
100% FREE & OPEN SOURCE
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="entropic-core",
    version="3.0.0",
    author="Entropic Core Team",
    author_email="info@entropic-core.com",
    description="Privacy-first entropy monitoring with active LLM intervention for multi-agent systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/entropic-core/entropic-core",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    keywords="ai agents multi-agent entropy regulation homeostasis machine-learning hallucination-detection privacy-first",
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "typing-extensions>=4.0.0",
        "requests>=2.25.0",
        "click>=8.0.0",
    ],
    extras_require={
        # All features are free, these are just optional dependencies
        "analytics": [
            "scipy>=1.7.0",
            "scikit-learn>=1.0.0",
        ],
        "visualization": [
            "flask>=2.0.0",
            "flask-cors>=3.0.0",
            "plotly>=5.0.0",
            "pandas>=1.3.0",
        ],
        "reports": [
            "reportlab>=3.6.0",
        ],
        "streaming": [
            "websockets>=10.0",
            "aiohttp>=3.8.0",
        ],
        "full": [
            "scipy>=1.7.0",
            "scikit-learn>=1.0.0",
            "flask>=2.0.0",
            "flask-cors>=3.0.0",
            "plotly>=5.0.0",
            "pandas>=1.3.0",
            "reportlab>=3.6.0",
            "websockets>=10.0",
            "aiohttp>=3.8.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "pytest-asyncio>=0.20.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "entropic-core=entropic_core.cli:main",
            "entropic-quickstart=entropic_core.quickstart:main",
            "entropic-setup=entropic_core.discovery.setup_wizard:main",
            "entropic-discover=entropic_core.discovery.llm_discoverer:main",
            "entropic-dashboard=entropic_core.visualization.dashboard:main",
            "entropic-diagnose=entropic_core.cli:diagnose",
            "entropic-fix=entropic_core.cli:fix",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/entropic-core/entropic-core/issues",
        "Source": "https://github.com/entropic-core/entropic-core",
        "Documentation": "https://entropic-core.readthedocs.io",
        "Discord": "https://discord.gg/entropic-core",
        "Privacy Policy": "https://github.com/entropic-core/entropic-core/blob/main/PRIVACY.md",
    },
)
