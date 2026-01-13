from setuptools import setup, find_packages

setup(
    name="eric-slides-neeraj",  # <--- CHANGE THIS to something unique!
    version="2.0.2",
    description="A terminal-based presentation tool with syntax highlighting",
    author="Neeraj Narwariya",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'eric=eric:start_cli',  # This lets people just type 'eric' in terminal
        ],
    },
)