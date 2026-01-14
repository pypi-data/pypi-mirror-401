from setuptools import setup

setup(
    name="shellcoderunner-aes",
    version="1.1.0",
    py_modules=["shellcoderunneraes"],
    install_requires=["pycryptodome"],
    entry_points={
        "console_scripts": [
            "shellcoderunneraes=shellcoderunneraes:main"
        ]
    },
    author="PaiN05",
    description="AES-based shellcode loader generator for Windows security research",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
    ],
)
