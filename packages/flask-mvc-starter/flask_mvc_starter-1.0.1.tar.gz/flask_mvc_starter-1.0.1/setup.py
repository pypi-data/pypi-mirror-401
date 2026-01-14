from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="flask-mvc-starter",
    version="1.0.1",
    description="A simple Flask boilerplate with MVC architecture, JWT, caching, and Celery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rajnish Kumar",
    author_email="contact.rajnishk@gmail.com",
    url="https://github.com/0rajnishk/flask-mvc-starter",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "flask-mvc-starter=flask_mvc_starter.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
