from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent.resolve()

with open(here / "README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    "Flask>=2.0.0",
    "pymongo>=4.0.0",
    "psutil>=5.9.0",
    "pydantic>=2.0.0",
    "requests>=2.28.0",
    "python-dotenv>=0.20.0",
    "click>=8.1.0",
]

setup(
    name="autonomous-recovery-agent",
    version="1.0.0",
    author="Autonomous Recovery Team",
    author_email="support@autonomous-recovery.com",
    description="Autonomous monitoring and recovery agent for Flask + MongoDB applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/autonomous-recovery-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Recovery",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
        "web": [
            "flask>=2.0.0",
            "flask-cors>=3.0.0",
        ],
        "mongodb": [
            "pymongo>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "recovery-agent=autonomous_recovery.cli:main",
        ],
    },
    include_package_data=True,
)