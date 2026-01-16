
from setuptools import setup, find_packages

setup(
    name="MandreInApp",
    version="1.0.0",
    author="@meeowPlugins (Ported for MandreLib)",
    description="Simple In-App Notification library for MandreLib based plugins. Original by @meeowPlugins.",
    long_description="Original author: https://t.me/meeowPlugins. Ported to generic library for MandreLib.",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Android",
    ],
    python_requires='>=3.6',
)
