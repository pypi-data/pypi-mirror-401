from setuptools import setup, find_packages
import os

# Read requirements
with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# Read README for long description
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "Nutaan ERP AI Agent SDK - Autonomous AI agent for ERPNext/Frappe automation"

setup(
    name="nutaan_erp",
    version="1.0.3",
    description="Nutaan ERP AI Agent SDK - Autonomous AI agent for ERPNext/Frappe with 14 built-in tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nutaan AI (Tecosys)",
    author_email="hara@nutaan.com",
    url="https://github.com/tecosys/nutaan-erp",
    project_urls={
        "Bug Tracker": "https://github.com/tecosys/nutaan-erp/issues",
        "Documentation": "https://github.com/tecosys/nutaan-erp",
        "Source Code": "https://github.com/tecosys/nutaan-erp",
    },
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    python_requires=">=3.8",
    keywords="ai agent erp erpnext frappe automation langchain gemini",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)
