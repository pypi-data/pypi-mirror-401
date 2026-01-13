from setuptools import setup, find_packages

setup(
    name="telegram_async",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "rich"
    ],
)
