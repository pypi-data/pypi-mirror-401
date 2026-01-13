from setuptools import setup, find_packages

# Read requirements from your SDK (usually requests and a few others)
# Do NOT include server dependencies like fastapi or sqlalchemy here.
requirements = [
    "requests>=2.25.0",
    "aiohttp>=3.8.0",  # <--- ADD THIS LINE
    "typing-extensions>=4.0.0; python_version < '3.10'",
]

setup(
    name="limesrail",
    version="0.1.0",
    description="The official Python SDK for Limesrail Observability",
    long_description=open("README.md").read() if open("README.md").read() else "",
    long_description_content_type="text/markdown",
    author="Limesrail Team",
    author_email="support@limesrail.com",
    url="https://github.com/Limesrail/limesrail",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)