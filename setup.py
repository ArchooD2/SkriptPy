from setuptools import setup, find_packages

setup(
    name="skriptpy",
    version="0.1.0",
    author="ArchooD2",
    author_email="archoo@example.com",
    description="A bidirectional transpiler between Python and Skript",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ArchooD2/SkriptPy",
    packages=find_packages(),
    scripts=["skriptpy-transpile.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires=">=3.6",
    install_requires=[
        "difflib",
        "snaparg",
        "re",
        "os",
        "sys",
    ],
)
