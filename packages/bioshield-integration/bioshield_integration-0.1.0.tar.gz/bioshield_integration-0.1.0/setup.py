from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bioshield-integration",
    version="0.1.0",
    author="Emerlad Compass",
    author_email="emerladcompass@gmail.com",
    description="Unified Intelligence Framework with Adaptive Learning & Real-Time Alerts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emerladcompass/BioShield-Integration",
    packages=find_packages(include=['src', 'src.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=["pyyaml>=6.0"],  # فقط pyyaml
    extras_require={
        "full": ["numpy", "scipy"],  # optional
    },
    entry_points={
        "console_scripts": [
            "bioshield=dashboard.dashboard:main_dashboard",
        ],
    },
)
