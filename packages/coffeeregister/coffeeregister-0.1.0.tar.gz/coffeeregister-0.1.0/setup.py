from setuptools import setup, find_packages

setup(
    name="coffeeregister",
    version="0.1.0",
    author="quzaory",
    author_email="zHIjsBlKlHF7oCZ@proton.me",
    description="Coffee shop cash register",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["PySide6>=6.5.0"],
    entry_points={
        "console_scripts": [
            "coffee-cash=chill_coffee_cash.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
