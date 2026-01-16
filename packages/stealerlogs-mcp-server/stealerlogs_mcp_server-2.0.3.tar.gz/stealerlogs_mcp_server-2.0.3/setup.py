from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="stealerlogs-mcp-server",
    version="1.0.0",
    author="Stealerlo.gs",
    author_email="support@stealerlo.gs",
    description="Model Context Protocol server for Stealerlo.gs API - Integrate stealerlog search with AI assistants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cryphorix/stealerlo.gs",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "mcp>=0.9.0",
        "httpx>=0.25.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "stealerlogs-mcp=stealerlo_mcp.server:main",
            "stealerlo-mcp=stealerlo_mcp.server:main",
        ],
    },
    include_package_data=True,
)

