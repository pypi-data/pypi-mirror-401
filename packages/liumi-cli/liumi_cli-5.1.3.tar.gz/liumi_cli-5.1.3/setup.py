from setuptools import setup, find_packages

setup(
    name="liumi-cli",
    version="5.1.3",
    author="Liumi Corporation",
    author_email="support@liumi.cloud",
    description="The Legendary AI DevOps Interface Utility",
    long_description="LIU is an AI-powered CLI that manages your code, writes commits, fixes bugs, and automates DevOps.",
    long_description_content_type='text/markdown',
    url="https://liumi.cloud/liu",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'liu=liumi_cli.main:entry', # Points to the entry() function in main.py
        ],
    },
    install_requires=[
        'typer',
        'rich',
        'pyfiglet',
        'requests',
        'google-genai',
        'PyGithub',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)