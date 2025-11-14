from setuptools import setup, find_packages

setup(
    name="letter_merge_cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "openpyxl",      # Required for reading Excel files
        "python-docx",   # Required if you're manipulating Word documents directly
        "mailmerge",     # Your main document generation engine
    ],
    entry_points={
        "console_scripts": [
            "letter-merge=letter_merge.cli:main"
        ]
    },
    author="Thomas Jacobs",
    description="A CLI tool to generate personalized letters from a Word template and Excel data",
    python_requires=">=3.7",
)
